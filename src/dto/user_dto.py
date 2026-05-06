import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserCreateDto(BaseModel):
    email: EmailStr = Field(default="admin01@admin.com")
    password: str = Field(example="password")
    full_name: Optional[str] = Field(default=None, example="User 01", max_length=50)
    avatar: Optional[str] = None

    @validator('password')
    def validate_password(cls, value: str) -> str:
        password_pattern = re.compile(
            r"^(?=.*[A-Z])(?=.*\d)(?=.*[*#?.\-@_&%$≠()])[a-zA-Z0-9*#?.\-@_&%$≠()]{8,20}$"
        )
        if not re.match(password_pattern, value):
            raise ValueError(
                "Password must be 8-20 characters long, contain at least one uppercase letter, "
                "one number, and one special character from the set: *#?.-@_&%$≠()."
            )
        return value

    
