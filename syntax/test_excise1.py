from typing import Optional, List

import uvicorn
from fastapi import FastAPI, Query, Path, Body

from enum import Enum

from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item2(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="这是描述", max_length=30, example="这个是什么效果")
    price: float = Field(..., gt=0, description="价格必须大于0")
    tax: Optional[float] = None
    sellarea: List[str] = []
    image: Optional[Image] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "DEMO",
                "description": "DEMO",
                "price": 20,
                "tax": 0.5,
            }
        }


@app.put("/items/{itemid}")
def update_items(itemid: int, item: Item2 = Body(..., embed=True)):
    results = {"itemid": itemid, "item": item}
    return results
