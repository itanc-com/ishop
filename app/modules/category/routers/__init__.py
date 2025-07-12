from fastapi import APIRouter

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[],
)

from .category_create import category_create  # noqa: F401, E402
from .category_retrieve import get_category_by_id  # noqa: F401, E402
