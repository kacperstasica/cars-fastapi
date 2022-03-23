from fastapi import APIRouter

from routes import cars, reviews

router = APIRouter()
router.include_router(
    cars.router,
    prefix="/cars",
    tags=["cars"],
    responses={404: {"description": "Not found"}}
)
router.include_router(
    reviews.router,
    tags=["rate"],
    responses={404: {"description": "Not found"}}
)
