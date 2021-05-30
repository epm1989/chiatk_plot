from typing import Optional
from fastapi import APIRouter
from app.controllers.plot import PlotController


api_router = APIRouter()


@api_router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@api_router.get("/stop/{pid}")
async def stop(pid: int):
    result, message = await PlotController.stop(pid)

    return {"result": result, 'message': message}


@api_router.get("/all")
async def read_item():
    result = await PlotController.all()
    print(result)
    return {"result": result}


@api_router.get("/refresh")
async def refresh():
    if PlotController.refresh():
        return {"result": True}
    return {"result": False}


@api_router.get("/queue/create")
async def queue():
    plot = PlotController()
    queue, running, waiting = await plot.queue()
    if queue:
        return {"result": True, 'running': running, 'waiting': waiting}
    return {"result": False}


@api_router.get("/queue/status")
async def queue():
    running, waiting = await PlotController().queue_status()
    return {"result": True, 'running': running, 'waiting': waiting}


@api_router.get("/start")
async def start():
    plot = PlotController()
    result, message = await plot.start()
    return {"result": result, 'message': message}