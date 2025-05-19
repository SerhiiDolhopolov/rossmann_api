import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import TAG_ADMIN
from app.api.categories import TAG_CATEGORIES, TAG_ADMIN_CATEGORIES
from app.api.categories import router as categories_router
from app.api.categories import router_admin as categories_router_admin
from app.api.products import TAG_PRODUCTS, TAG_ADMIN_PRODUCTS
from app.api.products import router as products_router
from app.api.products import router_admin as products_router_admin
from app.api.city_products import TAG_CITY_PRODUCTS, TAG_ADMIN_CITY_PRODUCTS
from app.api.city_products import router as city_products_router
from app.api.city_products import router_admin as city_products_router_admin
from app.api.users_count import TAG_ADMIN_USERS_COUNT
from app.api.users_count import router_admin as users_count_router
from app.api.users import TAG_USERS
from app.api.users import router as users_router

from app.kafka.producer import init_producer, close_producer 


openapi_tags = [
    {"name": TAG_CATEGORIES },
    {"name": TAG_PRODUCTS },
    {"name": TAG_CITY_PRODUCTS },
    {"name": TAG_USERS },
    {"name": TAG_ADMIN },
    {"name": TAG_ADMIN_CATEGORIES },
    {"name": TAG_ADMIN_PRODUCTS },
    {"name": TAG_ADMIN_CITY_PRODUCTS},
    {"name": TAG_ADMIN_USERS_COUNT },
    
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_producer()
    yield
    await close_producer()
    
app = FastAPI(lifespan=lifespan, openapi_tags=openapi_tags)

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(city_products_router)
app.include_router(users_router)

app.include_router(categories_router_admin)
app.include_router(products_router_admin)
app.include_router(city_products_router_admin)
app.include_router(users_count_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)