from datetime import datetime
from pydantic import Field, BaseModel, EmailStr


class UserAddSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(max_length=100)


class UserPatchSchema(BaseModel):
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    password: str | None = Field(default=None, max_length=100)


class UserSchema(BaseModel):
    user_id: int = Field(ge=1)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    registration_datetime_utc: datetime

