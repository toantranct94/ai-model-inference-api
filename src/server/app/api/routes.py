from fastapi import APIRouter

from .endpoints import health_router, inference_router


router = APIRouter()

router.include_router(
    health_router,
    tags=['health'],
)


router.include_router(
    inference_router,
    tags=['inference'],
    prefix='/inference',
)
