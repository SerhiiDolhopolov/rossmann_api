from datetime import datetime

from pydantic import Field, BaseModel, EmailStr


class UserAddSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(max_length=100)
    
class UserPatchSchema(BaseModel):
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
    email: EmailStr | None = Field(max_length=100, default=None)
    password: str | None = Field(max_length=100, default=None)
    
class UserSchema(BaseModel):
    user_id: int
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    registration_datetime_utc: datetime
    
