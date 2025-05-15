from fastapi import APIRouter, Depends, HTTPException
from rossmann_oltp_models import Product, CityProduct, Category

from app.oltp_db import get_db
from app.schemas import CityProductSchema, ProductSchema
from app.config import TAG_ADMIN


router = APIRouter(prefix="/city_products", tags=["city-products 📦"])
router_admin = APIRouter(prefix="/city_products", tags=[TAG_ADMIN, "admin:city-products 📦"])


@router.get('/city/{city_id:int}', summary='Return products by city id.', response_model=list[CityProductSchema])
async def get_products_by_city(city_id: int, db = Depends(get_db)):
    products = db.query(Product, CityProduct) \
                 .join(CityProduct, Product.product_id == CityProduct.product_id) \
                 .filter(CityProduct.city_id == city_id,
                         Product.is_deleted == False,
                         CityProduct.is_deleted == False) \
                 .all()
    
    result = [CityProductSchema(product=ProductSchema.model_validate(product, from_attributes=True),
                                price=city_product.price
                               ) for product, city_product in products]
        
    
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")

    return result