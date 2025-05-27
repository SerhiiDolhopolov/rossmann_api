from pydantic import Field, BaseModel, field_validator
from app.config import S3_PUBLIC_URL


class ProductAddSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=2048)
    barcode: str = Field(max_length=12)
    category_id: int
    image_url: str | None = Field(default=None, max_length=255)

    @field_validator("image_url", mode="before")
    def image_url_validator(cls, value: str | None) -> str | None:
        return add_image_url_prefix(value)


class ProductUpdateSchema(ProductAddSchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")

    class Config:
        extra = "forbid"


class ProductPatchSchema(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=2048)
    barcode: str | None = Field(default=None, max_length=12)
    category_id: int | None = Field(default=None)
    image_url: str | None = Field(default=None, max_length=255)
    is_deleted: bool | None = Field(
        default=None,
        description="Indicates if the record is deleted",
    )

    @field_validator("image_url", mode="before")
    def image_url_validator(cls, v: str | None) -> str | None:
        return add_image_url_prefix(v)

    class Config:
        extra = "forbid"


class ProductSchema(ProductAddSchema):
    product_id: int = Field(ge=1)


class ProductAdminSchema(ProductSchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")


def add_image_url_prefix(value: str | None) -> str | None:
    if value is None or value.startswith(S3_PUBLIC_URL):
        return value
    return f"{S3_PUBLIC_URL}/{value}"