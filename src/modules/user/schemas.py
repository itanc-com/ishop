from pydantic import BaseModel, Field

from src.modules.user.models import UserRole, UserStatus


class UserInsert(BaseModel):
    first_name: str = Field(..., examples="John", max_length=255)
    last_name: str = Field(..., examples="Doe", max_length=255)
    email: str = Field(..., examples="johndoe@gmail.com", max_length=255)
    password: str = Field(..., examples="hashed password", min_length=8)
    picture: str = Field(examples="/path/to/img.jpg", default=None)
    role: int = Field(examples="0 as user and 1 as admin", default=UserRole.USER)
    status: int = Field(examples="0 deactive, 1 active, 2 verified, 3 suspended", default=UserStatus.DEACTIVE)
    phone: str = Field(default=None, examples="+989121111111")
    address: str = Field(
        default=None,
        examples="Tehran, Tehran, No. 13, Bahar Shiraz St., Shariati St., 15658, P.O. Box: 11365-717",
    )


class UserView(BaseModel):
    id: int = Field(..., examples=1)
    first_name: str = Field(..., examples="John", max_length=255)
    last_name: str = Field(..., examples="Doe", max_length=255)
    email: str = Field(..., examples="johndoe@gmail.com", max_length=255)
    picture: str = Field(..., examples="/path/to/img")
    role: int = Field(..., examples="0 as user and 1 as admin")
    status: int = Field(..., examples="0 deactive, 1 active ...")
    phone: str = Field(..., examples="+989121111111")
    address: str = Field(
        ...,
        examples="Tehran, Tehran, No. 13, Bahar Shiraz St., Shariati St., 15658, P.O. Box: 11365-717",
    )
