from typing import Optional
from app.api.plot import api_router
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    pass

app.include_router(api_router, prefix='/plot')

@app.get("/")
async def read_root():
    return {"Hello": "World"}


