from pydantic import BaseModel, Field


class CategoryAddSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=2048)


class CategoryUpdateSchema(CategoryAddSchema):
    is_deleted: bool = Field(
        description="Indicates if the record is deleted",
    )

    class Config:
        extra = "forbid"


class CategoryPatchSchema(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(
        default=None,
        max_length=2048,
    )
    is_deleted: bool | None = Field(
        default=None,
        description="Indicates if the record is deleted",
    )

    class Config:
        extra = "forbid"
        

class CategorySchema(CategoryAddSchema):
    category_id: int = Field(ge=1)


class CategoryAdminSchema(CategorySchema):
    is_deleted: bool = Field(
        description="Indicates if the record is deleted",
    )