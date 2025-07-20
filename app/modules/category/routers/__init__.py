from fastapi import APIRouter

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[],
)

from .category_create import category_create  # noqa: F401, E402
from .category_list import category_list  # noqa: F401, E402
from .category_retrieve import category_get_by_id  # noqa: F401, E402
