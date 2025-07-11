from datetime import datetime

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    parent_id: int = Field(0, description="Parent category ID", examples=[1], ge=0)
    title: str = Field(..., description="Category title", examples=["Electronics"])


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    parent_id: int | None = Field(None, description="Parent category ID", examples=[1], ge=0)
    title: str | None = Field(None, description="Category title", examples=["Electronics"])


class CategoryRead(CategoryBase):
    id: int = Field(..., description="Category ID", examples=[1])
    date_created: datetime = Field(
        ...,
        description="Timestamp when the category was created",
        examples=["2023-01-01T00:00:00"],
    )
    date_modified: datetime = Field(
        ...,
        description="Timestamp when the category was last modified",
        examples=["2023-01-01T00:00:00"],
    )

    class Config:
        from_attributes = True
