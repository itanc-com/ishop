from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.common.enums import UserRole, UserStatus


class UserBase(BaseModel):
    first_name: str | None = Field(None, max_length=255, description="User's first name")
    last_name: str | None = Field(None, max_length=255, description="User's last name")
    email: EmailStr = Field(..., description="User's unique email address")
    picture: str | None = Field(None, description="URL or path to user's profile picture")
    role: UserRole = Field(default=UserRole.USER, description="Role of the user")
    status: UserStatus = Field(default=UserStatus.DEACTIVE, description="Current user status")
    phone: str | None = Field(None, description="User's phone number")
    address: str | None = Field(None, description="User's physical address")

    model_config = {"use_enum_values": True}


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)
    picture: str | None = None
    role: UserRole | None = None
    status: UserStatus | None = None
    phone: str | None = None
    address: str | None = None


class UserRead(UserBase):
    id: int
    date_created: datetime
    date_modified: datetime

    model_config = {"from_attributes": True, "use_enum_values": True}
