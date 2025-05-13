from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from .models import UserRole, UserStatus


class UserBase(BaseModel):
    first_name: str | None = Field(max_length=255, description="User's first name", examples=["John"])
    last_name: str | None = Field(max_length=255, description="User's last name", examples=["Doe"])
    email: EmailStr = Field(..., description="User's unique email address", examples=["john.doe@example.com"])
    picture: str | None = Field(
        description="URL or path to user's profile picture",
        examples=["https://example.com/photos/123.jpg"],
    )
    role: UserRole = Field(default=UserRole.USER, description="Role of the user, e.g. 0, 1 and etc", examples=[0])
    status: UserStatus = Field(
        default=UserStatus.DEACTIVE,
        description="Current status of the user account",
        examples=[0],
    )
    phone: str | None = Field(description="User's phone number", examples=["+1-555-555-0123"])
    address: str | None = Field(description="User's physical address", examples=["123 Main St, City, Country"])

    class Config:
        use_enum_values = True


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        description="User's account password (min 8 characters)",
        examples=["StrongP@ss123"],
    )


class UserUpdate(BaseModel):
    first_name: str | None = Field(description="Updated first name", examples=["Jane"])
    last_name: str | None = Field(description="Updated last name", examples=["Smith"])
    email: EmailStr | None = Field(description="Updated email", examples=["jane.smith@example.com"])
    password: str | None = Field(min_length=8, description="Updated password", examples=["NewP@ss456"])
    picture: str | None = Field(
        description="Updated profile picture URL",
        examples=["https://example.com/photos/456.jpg"],
    )
    role: UserRole | None = Field(description="Updated user role", examples=[1])
    status: UserStatus | None = Field(description="Updated user status", examples=[1])
    phone: str | None = Field(description="Updated phone number", examples=["+1-555-555-0456"])
    address: str | None = Field(description="Updated address", examples=["456 Oak Ave, City, Country"])


class UserRead(UserBase):
    id: int = Field(..., description="Unique ID of the user", examples=[1])
    date_created: datetime = Field(
        ...,
        description="Timestamp when the user was created",
        examples=["2023-01-01T00:00:00"],
    )
    date_modified: datetime = Field(
        ...,
        description="Timestamp when the user was last updated",
        examples=["2023-01-01T12:30:00"],
    )

    class Config:
        from_attributes = True
