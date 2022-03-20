import sys
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config(".env")

PROJECT_NAME = config(
    "Cars API", default="FastAPI application"
)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=[""]
)

DATABASE_URL = config("DATABASE_URL")

MODELS_FOR_MAKE_ENDPOINT = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json'
