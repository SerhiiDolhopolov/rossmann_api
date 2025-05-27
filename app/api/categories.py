from fastapi import APIRouter, Depends, HTTPException, Query, Request
from rossmann_oltp_models import Category

from app.oltp_db import get_db
from app.schemas import (
    CategorySchema,
    CategoryAdminSchema,
    CategoryAddSchema,
    CategoryUpdateSchema,
    CategoryPatchSchema,
)
from app.kafka.producer import get_kafka_producer, upsert_category_to_local_db
from app.config import TAG_ADMIN


TAG_CATEGORIES = "categories 📂"
TAG_ADMIN_CATEGORIES = "admin:categories 📂"

router = APIRouter(prefix="/categories", tags=[TAG_CATEGORIES])
router_admin = APIRouter(prefix="/categories", tags=[TAG_ADMIN, TAG_ADMIN_CATEGORIES])


@router.get(
    "/",
    summary="Return categories, which are not deleted.",
    response_model=list[CategorySchema],
)
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=100),
    db=Depends(get_db),
):
    return (
        db.query(Category)
        .filter(Category.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router_admin.get(
    "/all",
    summary="Return all categories, include deleted.",
    response_model=list[CategoryAdminSchema],
)
async def get_all_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=100),
    db=Depends(get_db),
):
    return db.query(Category).offset(skip).limit(limit).all()


@router.get("/<category_id:int>", response_model=CategoryAdminSchema)
async def get_category(category_id: int, db=Depends(get_db)):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router_admin.post("/", response_model=CategoryAdminSchema)
async def add_category(
    category: CategoryAddSchema, 
    db=Depends(get_db),
    producer=Depends(get_kafka_producer),
):
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    await upsert_category_to_local_db(
        producer=producer,
        category_id=new_category.category_id,
        name=new_category.name,
        description=new_category.description,
        is_deleted=new_category.is_deleted,
    )
    return new_category


@router_admin.put("/<category_id:int>", response_model=CategoryAdminSchema)
async def replace_category(
    category_id: int, 
    category: CategoryUpdateSchema, 
    db=Depends(get_db),
    producer=Depends(get_kafka_producer),
):
    return await update_category_method(
        category_id=category_id, 
        category=category, 
        db=db,
        producer=producer,
    )


@router_admin.patch("/<category_id:int>", response_model=CategoryAdminSchema)
async def update_category(
    category_id: int, 
    category: CategoryPatchSchema, 
    db=Depends(get_db),
    producer=Depends(get_kafka_producer),
):
    return await update_category_method(
        category_id=category_id, 
        category=category, 
        db=db,
        producer=producer,
    )


async def update_category_method(
    category_id: int, 
    category, 
    db,
    producer,
):
    existing_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(existing_category, key, value)

    db.commit()
    db.refresh(existing_category)

    await upsert_category_to_local_db(
        producer=producer,
        category_id=existing_category.category_id,
        name=existing_category.name,
        description=existing_category.description,
        is_deleted=existing_category.is_deleted,
    )

    return existing_category