from pydantic import BaseModel, Field


class ProductInsert(BaseModel):
    category_id: int = Field(..., example=1)
    title: str = Field(..., max_length=255, example="Super Comfortable Chair")
    description: str = Field(..., example="A modern, ergonomic chair perfect for long working hours.")
    sku: str = Field(..., example="CHAIR-1234")
    price: float = Field(default=0.0, ge=0, example=99.99)
    is_available: bool = Field(default=False)
    is_visible: bool = Field(default=False)


class ProductUpdate(BaseModel):
    category_id: int = Field(..., example=1)
    # ...#complete this model


# double check this class
class ProductView(BaseModel):
    id: int = Field(..., example=1)
    category_id: int = Field(..., example=1)
    title: str = Field(..., max_length=255, example="Super Comfortable Chair")
    description: str = Field(..., example="A modern, ergonomic chair perfect for long working hours.")
    sku: str = Field(..., example="CHAIR-1234")
    price: float = Field(default=0.0, ge=0, example=99.99)
    is_available: bool = Field(default=False)
    is_visible: bool = Field(default=False)
