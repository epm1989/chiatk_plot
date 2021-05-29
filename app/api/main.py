from typing import Optional
from app.api.plot import api_router
from fastapi import FastAPI
from app.models import run, close

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await run(generate_schemas=True)


@app.on_event("shutdown")
async def shutdown_event():
    await close()


app.include_router(api_router, prefix='/plot')


@app.get("/")
async def read_root():
    return {"Hello": "World"}


