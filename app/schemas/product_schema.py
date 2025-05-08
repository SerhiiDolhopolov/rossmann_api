from pydantic import Field, BaseModel

from app.schemas import IsDeletedModel


class ProductAddSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(max_length=2048)
    barcode: str = Field(max_length=12)
    category_id: int
    image_url: str | None = Field(max_length=255)
    
class ProductSchema(ProductAddSchema, IsDeletedModel):
    product_id: int
    
class CityProductSchema(ProductSchema):
    city_id: int
    country_name: str = Field(max_length=255)
    city_name: str = Field(max_length=255)
    price: float = Field(gt=0.0)
    discount: float = Field(ge=0.0, le=1.0)