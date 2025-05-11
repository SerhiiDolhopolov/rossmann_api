from fastapi import APIRouter, Depends, HTTPException
from rossmann_oltp.models import Product, CityProduct

from app.oltp_db import get_db
from app.schemas import ProductSchema, ProductAdminSchema, ProductAddSchema, ProductPatchSchema


router = APIRouter(prefix="/products", tags=["products 📦"])


@router.get('', summary='Return products, which are not deleted.', response_model=list[ProductSchema])
async def get_products(db = Depends(get_db)):
    return db.query(Product).filter(Product.is_deleted == False).all()

@router.get('/all', summary='Return all products, include deleted.', response_model=list[ProductAdminSchema])
async def get_all_products(db = Depends(get_db)):
    return db.query(Product).all()

@router.get('/{product_id}', response_model=ProductAdminSchema)
async def get_product(product_id: int, db = Depends(get_db)):
    product = db.query(Product) \
                .filter(Product.product_id == product_id) \
                .first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



# @router.get('/city/{city_id}', summary='Return products by city id.', response_model=list[ProductSchema])
# async def get_products_by_city(city_id: int, db = Depends(get_db)):
#     products = db.query(Product, CityProduct) \
#                  .join(CityProduct, Product.product_id == CityProduct.product_id) \
#                  .filter(CityProduct.city_id == city_id,
#                          Product.is_deleted == False,
#                          CityProduct.is_deleted == False) \
#                  .all()

#     if not products:
#         raise HTTPException(status_code=404, detail="Products not found")

#     return products