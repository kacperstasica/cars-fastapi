import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.responses import RedirectResponse

from routers import cars, reviews
from src import models
from src.database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(cars.router)
app.include_router(reviews.router)
# stop redirecting paths without trailing slash to slash (we want response 404 instead of 307)
app.router.redirect_slashes = False


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/health")
async def health():
    return {"status": status.HTTP_200_OK}


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    # entrypoint for starting the app as python script - `python main.py` will start the worker
    uvicorn.run(app, host="0.0.0.0", port=8000)
