from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
async def home():
    return {'localhost:8000/docs'}

###################################################################
from typing import Dict
from fastapi import HTTPException

items: Dict[str, Item] = {}

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.name] = item
    return item

@app.get("/items/all", response_model=Dict[str, Item])
async def read_all_items():
    return items

@app.get("/items/{item_name}", response_model=Item)
async def read_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_name]

@app.put("/items/{item_name}", response_model=Item)
async def update_item(item_name: str, item: Item):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_name] = item
    return item

@app.delete("/items/{item_name}", response_model=Item)
async def delete_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items.pop(item_name)

###################################################################
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)