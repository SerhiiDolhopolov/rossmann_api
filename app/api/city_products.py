import json

from fastapi import APIRouter, Depends, HTTPException, Query
from rossmann_oltp_models import City, Product, CityProduct

from app.oltp_db import get_db
from app.redis import get_redis
from app.schemas import ProductSchema, ProductAdminSchema
from app.schemas import CityProductSchema, CityProductAdminSchema, CityProductAddSchema, CityProductUpdateSchema, CityProductPatchSchema
from app.config import TAG_ADMIN
from app.kafka.producer import upsert_product_to_local_db


TAG_CITY_PRODUCTS = 'city-products 📦'
TAG_ADMIN_CITY_PRODUCTS = 'admin:city-products 📦'

router = APIRouter(prefix="/city_products", tags=[TAG_CITY_PRODUCTS])
router_admin = APIRouter(prefix="/city_products", tags=[TAG_ADMIN, TAG_ADMIN_CITY_PRODUCTS])


def check_city(city_id: int, db) -> City:
    city = db.query(City) \
             .filter(City.city_id == city_id) \
             .first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
    
def check_product(product_id: int, db) -> Product:
    product = db.query(Product) \
                .filter(Product.product_id == product_id) \
                .first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get('/{city_id:int}', 
            summary='Return products, which are not deleted, by city id.', 
            response_model=list[CityProductSchema])
async def get_products_by_city(city_id: int, 
                               skip: int = Query(0, ge=0),
                               limit: int = Query(100, gt=0, le=100),
                               db = Depends(get_db)):
    check_city(city_id, db)
    query = db.query(Product, CityProduct) \
              .join(CityProduct, Product.product_id == CityProduct.product_id) \
              .filter(CityProduct.city_id == city_id,
                      Product.is_deleted == False,
                      CityProduct.is_deleted == False) \
              .offset(skip) \
              .limit(limit) \
              .all()
                 
    if not query:
        raise HTTPException(status_code=404, detail="Products not found")
    
    result = [CityProductSchema(product=ProductSchema.model_validate(product, from_attributes=True),
                                price=city_product.price,
                                discount=city_product.discount
                               ) for product, city_product in query]
        
    return result

@router.get('/{city_id:int}/menu',
            summary='Return products, which are not deleted, by city id and page.',
            response_model=list[CityProductSchema])
async def get_products_page_by_city(city_id: int,
                                    page: int = Query(1, ge=1),
                                    page_size: int = Query(4, ge=1),
                                    db = Depends(get_db),
                                    redis = Depends(get_redis)):
    redis_key = f'city_products:city_{city_id}:page_{page}:p_size_{page_size}'
    expire_time = 60
    redis_request = redis.get(redis_key)
    if redis_request:
        redis_json = json.loads(redis_request)
        if redis_json:
            print('From Redis')
            redis.expire(redis_key, expire_time)
            return redis_json
    
    products = await get_products_by_city(city_id=city_id,
                                          skip=(page - 1) * page_size,
                                          limit=page_size,
                                          db=db)
    products_data = [product.model_dump() for product in products]
    redis.set(redis_key, json.dumps(products_data), ex=expire_time)
    print('From DB')
    return products
    

@router_admin.get('/all/{city_id:int}', 
                  summary='Return all products, include deleted, by city id.', 
                  response_model=list[CityProductAdminSchema])
async def get_all_products_by_city(city_id, 
                                   skip: int = Query(0, ge=0),
                                   limit: int = Query(100, gt=0, le=100),
                                   db = Depends(get_db)):
    check_city(city_id, db)
    query = db.query(Product, CityProduct) \
                 .join(CityProduct, Product.product_id == CityProduct.product_id) \
                 .filter(CityProduct.city_id == city_id) \
                 .offset(skip) \
                 .limit(limit) \
                 .all()
                 
    if not query:
        raise HTTPException(status_code=404, detail="Products not found")
    
    result = [CityProductAdminSchema(product=ProductAdminSchema.model_validate(product, from_attributes=True),
                                     price=city_product.price,
                                     discount=city_product.discount,
                                     is_deleted=city_product.is_deleted
                                     ) for product, city_product in query]
        
    return result

@router.get('/{city_id:int}/{product_id:int}', 
            summary='Return product by city id and product id.',
            response_model=CityProductAdminSchema)
async def get_product_by_city(city_id: int, 
                              product_id: int, 
                              db = Depends(get_db)):
    check_city(city_id, db)
    query = db.query(Product, CityProduct) \
              .join(CityProduct, Product.product_id == CityProduct.product_id) \
              .filter(CityProduct.city_id == city_id,
                      Product.product_id == product_id) \
              .first()
    if not query:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product, city_product = query
    
    result = CityProductAdminSchema(product=ProductAdminSchema.model_validate(product, from_attributes=True),
                                    price=city_product.price,
                                    discount=city_product.discount,
                                    is_deleted=city_product.is_deleted
                                   )
    return result

@router_admin.post('/{city_id:int}/{product_id:int}',
                   summary='Add product to city.',
                   response_model=CityProductAdminSchema)
async def add_product_to_city(city_id: int,
                              product_id: int,
                              city_product: CityProductAddSchema,
                              db = Depends(get_db)):
        check_city(city_id, db)
        check_product(product_id, db)
        
        query = db.query(Product, CityProduct) \
                  .join(CityProduct, Product.product_id == CityProduct.product_id) \
                  .filter(CityProduct.city_id == city_id,
                          Product.product_id == product_id) \
                  .first()
        if query:
            raise HTTPException(status_code=400, detail="Product already exists in city")
        
        new_product = CityProduct(city_id=city_id,
                                  product_id=product_id,
                                  price=city_product.price,
                                  discount=city_product.discount)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        await upsert_product_to_local_db(product_id=new_product.product_id,
                                         name=new_product.product.name,
                                         description=new_product.product.description,
                                         barcode=new_product.product.barcode,
                                         category_id=new_product.product.category_id,
                                         price=new_product.price,
                                         discount=new_product.discount,
                                         is_deleted=new_product.is_deleted)
        
        result = CityProductAdminSchema(product=ProductAdminSchema.model_validate(new_product.product, from_attributes=True),
                                        price=new_product.price,
                                        discount=new_product.discount,
                                        is_deleted=new_product.is_deleted)
        
        return result

@router_admin.put('/{city_id:int}/{product_id:int}',
                   response_model=CityProductAdminSchema)
async def replace_product_in_city(city_id: int,
                                  product_id: int,
                                  city_product: CityProductUpdateSchema,
                                  db = Depends(get_db)):
    return await update_product_in_city_method(city_id=city_id,
                                               product_id=product_id,
                                               city_product=city_product,
                                               db=db)

@router_admin.patch('/{city_id:int}/{product_id:int}',
                   response_model=CityProductAdminSchema)
async def update_product_in_city(city_id: int,
                                 product_id: int,
                                 city_product: CityProductPatchSchema,
                                 db = Depends(get_db)):
    return await update_product_in_city_method(city_id=city_id,
                                               product_id=product_id,
                                               city_product=city_product,
                                               db=db)

async def update_product_in_city_method(city_id: int,
                                        product_id: int,
                                        city_product,
                                        db):
    check_city(city_id, db)
    check_product(product_id, db)
    existing_city_product = db.query(CityProduct) \
                              .filter(CityProduct.city_id == city_id,
                                      CityProduct.product_id == product_id) \
                              .first()
    if not existing_city_product:
        raise HTTPException(status_code=404, detail="City product not found")
    
    for key, value in city_product.model_dump(exclude_unset=True).items():
        setattr(existing_city_product, key, value)
        
    db.commit()
    db.refresh(existing_city_product)
    
    await upsert_product_to_local_db(product_id=existing_city_product.product_id,
                                     name=existing_city_product.product.name,
                                     description=existing_city_product.product.description,
                                     barcode=existing_city_product.product.barcode,
                                     category_id=existing_city_product.product.category_id,
                                     price=existing_city_product.price,
                                     discount=existing_city_product.discount,
                                     is_deleted=existing_city_product.is_deleted)
    
    return existing_city_product