from typing import Optional
from pydantic import BaseModel, Field

from app.schemas import IsDeletedModel

class CategoryAddSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=2048)
    
class CategoryPatchSchema(IsDeletedModel):
    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2048)
    
class CategorySchema(CategoryPatchSchema):
    category_id: int