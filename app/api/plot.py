from typing import Optional
from fastapi import APIRouter
from app.controllers.plot import PlotController


api_router = APIRouter()


@api_router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@api_router.get("/stop/{pid}")
async def stop(pid: int):
    result = await PlotController.stop(pid)

    return {"result": result}

@api_router.get("/all")
async def read_item():
    result = await PlotController.all()
    print(result)
    return {"item_id": 23, "q": 456}


@api_router.get("/queue")
async def queue():
    plot = PlotController()
    queue = await plot.queue()
    if queue:
        return {"result": True}
    return {"result": False}

@api_router.get("/create")
async def create():
    plot = PlotController()
    result = await plot.create()
    return {"result": result}