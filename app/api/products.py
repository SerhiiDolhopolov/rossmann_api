from fastapi import APIRouter, Depends, HTTPException
from rossmann_oltp.models import Product, CityProduct

from app.oltp_db import get_db
from app.schemas import ProductSchema


router = APIRouter(prefix="/products", tags=["products 📦"])


@router.get('', summary='Return products, which are not deleted.', response_model=list[ProductSchema])
async def get_products(db=Depends(get_db)):
    products = db.query(Product) \
                 .filter(Product.is_deleted == False) \
                 .all()

    return products

@router.get('/all', summary='Return all products.', response_model=list[ProductSchema])
async def get_all_products(db=Depends(get_db)):
    products = db.query(Product) \
                 .all()

    return products

@router.get('/city/{city_id}', summary='Return products by city id.', response_model=list[ProductSchema])
async def get_products_by_city(city_id: int, db=Depends(get_db)):
    products = db.query(Product, CityProduct) \
                 .join(CityProduct, Product.product_id == CityProduct.product_id) \
                 .filter(CityProduct.city_id == city_id,
                         Product.is_deleted == False,
                         CityProduct.is_deleted == False) \
                 .all()

    if not products:
        raise HTTPException(status_code=404, detail="Products not found")

    return products