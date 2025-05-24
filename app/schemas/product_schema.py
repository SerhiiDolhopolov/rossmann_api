from pydantic import Field, BaseModel, field_validator
from app.config import S3_PUBLIC_URL


class ProductAddSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(max_length=2048, default=None)
    barcode: str = Field(max_length=12)
    category_id: int
    image_url: str | None = Field(max_length=255, default=None)
    
    @field_validator("image_url", mode="before")
    def image_url_validator(cls, value: str | None) -> str | None:
        return add_image_url_prefix(value)

class ProductUpdateSchema(ProductAddSchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")
    
    class Config:
        extra = "forbid"
    
class ProductPatchSchema(BaseModel):
    name: str | None = Field(max_length=255, default=None)
    description: str | None = Field(max_length=2048, default=None)
    barcode: str | None = Field(max_length=12, default=None)
    category_id: int | None = Field(default=None)
    image_url: str | None = Field(max_length=255, default=None)
    is_deleted: bool | None = Field(description="Indicates if the record is deleted",
                                    default=None)
    
    @field_validator("image_url", mode="before")
    def image_url_validator(cls, v: str | None) -> str | None:
        return add_image_url_prefix(v)

    class Config:
        extra = "forbid"
    
class ProductSchema(ProductAddSchema):
    product_id: int
    
class ProductAdminSchema(ProductSchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")

def add_image_url_prefix(value: str | None) -> str | None:
    if value is None or value.startswith(S3_PUBLIC_URL):
        return value
    return f"{S3_PUBLIC_URL}/{value}"