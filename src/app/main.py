from fastapi import FastAPI

from .router import router

engine = FastAPI()
engine.include_router(router)
