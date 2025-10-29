from fastapi import FastAPI

from .router import create_router
from .service import Service
from .utils import getConfiguredStorage

storage = getConfiguredStorage()
service = Service(storage)

engine = FastAPI()
engine.include_router(create_router(service))
