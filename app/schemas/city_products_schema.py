from pydantic import Field, BaseModel
from app.schemas.product_schema import ProductSchema, ProductAdminSchema


class CityProductAddSchema(BaseModel):
    price: float = Field(ge=0)
    discount: float = Field(ge=0, le=1)


class CityProductUpdateSchema(CityProductAddSchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")

    class Config:
        extra = "forbid"


class CityProductPatchSchema(BaseModel):
    price: float | None = Field(default=None, ge=0)
    discount: float | None = Field(default=None, ge=0, le=1)
    is_deleted: bool | None = Field(
        default=None,
        description="Indicates if the record is deleted",
    )

    class Config:
        extra = "forbid"


class CityProductSchema(BaseModel):
    product: ProductSchema
    price: float = Field(ge=0)
    discount: float = Field(ge=0, le=1)


class CityProductAdminSchema(CityProductSchema):
    product: ProductAdminSchema
    is_deleted: bool = Field(description="Indicates if the record is deleted")