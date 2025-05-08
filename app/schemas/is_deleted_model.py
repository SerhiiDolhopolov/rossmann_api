from typing import Optional
from pydantic import BaseModel, Field


class IsDeletedModel(BaseModel):
    is_deleted: Optional[bool] = Field(default=False,
                                       description="Indicates if the record is deleted")