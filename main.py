from fastapi.responses import JSONResponse
from fastapi import Depends
import asyncio
import aiohttp
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from feature_async_req import busines_loop_call

app = FastAPI()

# Assuming we're working with a simple item model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


# In-memory database for demonstration
items = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/", response_model=Item)
async def add_item(item: Item):
    items.append(item)
    return item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            return items.pop(index)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/", response_model=List[Item])
async def read_items(name: Optional[str] = Query(None, description="Filter items by name")):
    if name:
        return [item for item in items if name.lower() in item.name.lower()]
    return items


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


async def get_session():
    async with aiohttp.ClientSession() as session:
        yield session


@app.get("/combined-data")
async def get_combined_data(session: aiohttp.ClientSession = Depends(get_session)):
    from feature_async_req import business_get_combined_data
    try:
        return await business_get_combined_data(session)
    except Exception as e:
        return JSONResponse(content={"error": e})


@app.get("/combined-data-normal")
async def get_combined_data_normal():
    try:
        return busines_loop_call()
    except Exception as e:
        return JSONResponse(content={"error": e})
