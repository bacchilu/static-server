from fastapi import FastAPI

from app.router import router

engine = FastAPI()
engine.include_router(router)
