from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    parent_id: int | None = Field(None, description="Parent category ID", examples=[1])
    title: str = Field(..., description="Category title", examples=["Electronics"])


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int = Field(..., description="Category ID", examples=[1])
    parent_id: int | None = Field(None, description="Parent category ID", examples=[1])
    title: str = Field(..., description="Category title", examples=["Electronics"])

    class Config:
        from_attributes = True
