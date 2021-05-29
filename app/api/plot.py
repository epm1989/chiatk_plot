from typing import Optional
from fastapi import APIRouter


api_router = APIRouter()

@api_router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}