from pydantic import BaseModel, Field


class CategoryAddSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(max_length=2048, default=None)
    
class CategoryUpdateSchema(CategoryAddSchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")
    
    class Config:
        extra = "forbid"
        
class CategoryPatchSchema(BaseModel):
    name: str | None = Field(max_length=255, default=None)
    description: str | None = Field(max_length=2048, default=None)
    is_deleted: bool | None = Field(description="Indicates if the record is deleted", 
                                    default=None)
    
    class Config:
        extra = "forbid"
    
class CategorySchema(CategoryAddSchema):
    category_id: int
    
class CategoryAdminSchema(CategorySchema):
    is_deleted: bool = Field(description="Indicates if the record is deleted")