import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

from routers import cars, reviews
from src import models
from src.database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(cars.router)
app.include_router(reviews.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
async def health():
    return {"status": status.HTTP_200_OK}


@app.get("/")
async def root():
    return RedirectResponse(url="/cars", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    # entrypoint for starting the app as python script - `python main.py` will start the worker
    uvicorn.run(app, host="0.0.0.0", port=8000)
