from fastapi import APIRouter, Depends, HTTPException
from rossmann_oltp.models import Category

from app.oltp_db import get_db
from app.schemas import CategorySchema, CategoryAdminSchema, CategoryAddSchema, CategoryPatchSchema


router = APIRouter(prefix="/categories", tags=["categories 📂"])


@router.get('', summary='Return categories, which are not deleted.', response_model=list[CategorySchema])
async def get_categories(db=Depends(get_db)):
    return db.query(Category).filter(Category.is_deleted == False).all()

@router.get('/all', summary='Return all categories, include deleted.', response_model=list[CategoryAdminSchema])
async def get_all_categories(db=Depends(get_db)):
    return db.query(Category).all()

@router.get('/{category_id}', response_model=CategoryAdminSchema)
async def get_category(category_id: int, db=Depends(get_db)):
    category = db.query(Category) \
                 .filter(Category.category_id == category_id) \
                 .first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post('/add', response_model=CategoryAdminSchema)
async def add_category(category: CategoryAddSchema, db=Depends(get_db)):
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.patch('/update/{category_id}', response_model=CategoryAdminSchema)
async def update_category(category_id: int, category: CategoryPatchSchema, db=Depends(get_db)):
    existing_category = db.query(Category) \
                          .filter(Category.category_id == category_id) \
                          .first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(existing_category, key, value)
    
    db.commit()
    db.refresh(existing_category)
    return existing_category
