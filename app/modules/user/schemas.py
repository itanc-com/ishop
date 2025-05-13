from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .models import UserRole, UserStatus


class UserInsert(BaseModel):
    first_name: str = Field(min_length=1, max_length=255, description="User's first name")
    last_name: str = Field(min_length=1, max_length=255, description="User's last name")
    email: EmailStr = Field(description="User's email address")
    password: str = Field(min_length=8, max_length=255, description="User's hashed password")
    picture: Optional[str] = Field(default=None, description="Path to user's profile picture")
    role: UserRole = Field(default=UserRole.USER, description="User role (0=user, 1=admin)")
    status: UserStatus = Field(default=UserStatus.DEACTIVE, description="User status")
    phone: Optional[str] = Field(default=None, pattern=r"^\+[0-9]{10,15}$", description="User's phone number")
    address: Optional[str] = Field(default=None, description="User's address")

    class Config:
        use_enum_values = True


class UserView(BaseModel):
    id: int = Field(gt=0, description="User ID")
    first_name: str = Field(min_length=1, max_length=255, description="User's first name")
    last_name: str = Field(min_length=1, max_length=255, description="User's last name")
    email: EmailStr
    picture: Optional[str] = Field(default=None, description="Path to user's profile picture")
    role: UserRole = Field(default=UserRole.USER, description="User role (0=user, 1=admin)")
    status: UserStatus = Field(default=UserStatus.DEACTIVE, description="User status")
    phone: Optional[str] = Field(pattern=r"^\+[0-9]{10,15}$", description="User's phone number")
    address: Optional[str] = Field(default=None, description="User's address")

    class Config:
        use_enum_values = True
