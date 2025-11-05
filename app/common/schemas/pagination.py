from pydantic import BaseModel, Field


class PaginationInfo(BaseModel):
    """
    Standard pagination information for list responses.
    Reusable across all modules (products, users, categories, orders, etc.).
    """

    page: int = Field(..., ge=1, description="Current page number", example=1)
    limit: int = Field(..., ge=1, le=100, description="Items per page", example=10)
    total_items: int = Field(..., ge=0, description="Total number of items", example=21)
    total_pages: int = Field(..., ge=0, description="Total number of pages", example=3)
    has_next: bool = Field(default=False, description="Whether there is a next page", example=True)
    has_prev: bool = Field(default=False, description="Whether there is a previous page", example=False)
