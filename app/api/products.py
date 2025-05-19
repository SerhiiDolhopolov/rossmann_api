from fastapi import APIRouter, Depends, HTTPException, Query
from rossmann_oltp_models import Product, Category

from app.oltp_db import get_db
from app.schemas import ProductSchema, ProductAdminSchema, ProductAddSchema, ProductUpdateSchema, ProductPatchSchema
from app.config import TAG_ADMIN


TAG_PRODUCTS = 'products 📦'
TAG_ADMIN_PRODUCTS = 'admin:products 📦'

router = APIRouter(prefix="/products", tags=[TAG_PRODUCTS])
router_admin = APIRouter(prefix="/products", tags=[TAG_ADMIN, TAG_ADMIN_PRODUCTS])


@router.get('/', summary='Return products, which are not deleted.', response_model=list[ProductSchema])
async def get_products(skip: int = Query(0, ge=0),
                       limit: int = Query(100, gt=0, le=100),
                       db = Depends(get_db)):
    return db.query(Product) \
             .filter(Product.is_deleted == False) \
             .offset(skip) \
             .limit(limit) \
             .all()

@router_admin.get('/all', summary='Return all products, include deleted.', response_model=list[ProductAdminSchema])
async def get_all_products(skip: int = Query(0, ge=0),
                           limit: int = Query(100, gt=0, le=100),
                           db = Depends(get_db)):
    return db.query(Product) \
             .offset(skip) \
             .limit(limit) \
             .all()

@router.get('/{product_id:int}', response_model=ProductAdminSchema)
async def get_product(product_id: int, db = Depends(get_db)):
    product = db.query(Product) \
                .filter(Product.product_id == product_id) \
                .first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router_admin.post('/', response_model=ProductAdminSchema)
async def add_product(product: ProductAddSchema, db = Depends(get_db)):
    if db.query(Category) \
         .filter(Category.category_id == product.category_id) \
         .first() is None:
        raise HTTPException(status_code=404, detail="Category not found")
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router_admin.put('/{product_id:int}', response_model=ProductAdminSchema)
async def replace_product(product_id: int, product: ProductUpdateSchema, db = Depends(get_db)):
    return await update_product_method(product_id=product_id, product=product, db=db)

@router_admin.patch('/{product_id:int}', response_model=ProductAdminSchema)
async def update_product(product_id: int, product: ProductPatchSchema, db = Depends(get_db)):
    return await update_product_method(product_id=product_id, product=product, db=db)

async def update_product_method(product_id: int, product, db):
    existing_product = db.query(Product) \
                         .filter(Product.product_id == product_id) \
                         .first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.category_id is not None:
        if db.query(Category) \
            .filter(Category.category_id == product.category_id) \
            .first() is None:
            raise HTTPException(status_code=404, detail="Category not found")

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(existing_product, key, value)

    db.commit()
    db.refresh(existing_product)
    return existing_product