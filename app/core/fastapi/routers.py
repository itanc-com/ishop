from fastapi import APIRouter

from app.modules.auth.routers import router as auth_router
from app.modules.cart.routers import router as cart_router
from app.modules.category.routers import router as category_router
from app.modules.product.routers import router as products_router
from app.modules.user.routers import router as user_router

router_v1 = APIRouter(prefix="/v1")

"""Include to router all api rest routes with version prefix"""

router_v1.include_router(auth_router)
router_v1.include_router(cart_router)
router_v1.include_router(category_router)
router_v1.include_router(products_router)
router_v1.include_router(user_router)
