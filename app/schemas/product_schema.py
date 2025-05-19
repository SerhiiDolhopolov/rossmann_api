from pydantic import Field, BaseModel


class ProductAddSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(max_length=2048, default=None)
    barcode: str = Field(max_length=12)
    category_id: int
    image_url: str | None = Field(max_length=255, default=None)
    
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
    
    class Config:
        extra = "forbid"
    
class ProductSchema(ProductAddSchema):
    product_id: int
    
class ProductAdminSchema(ProductSchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")