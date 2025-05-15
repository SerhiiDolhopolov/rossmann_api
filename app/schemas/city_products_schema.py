from pydantic import Field, BaseModel
from app.schemas.product_schema import ProductSchema, ProductAddSchema


class CityProductSchema(BaseModel):
    product: ProductSchema
    price: float
    
    model_config = {"from_attributes": True}