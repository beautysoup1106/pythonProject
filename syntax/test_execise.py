from typing import Optional, List

import uvicorn
from fastapi import FastAPI, Query, Path, Body

from enum import Enum

from pydantic import BaseModel, Field


app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="这是描述", max_length=30)
    price: float = Field(..., gt=0, description="价格必须大于0")
    tax: Optional[float] = None


@app.put("/items/{itemid}")
async def update_items(itemid: int, item: Item = Body(..., embed=True)):
    results = {"itemid": itemid, "item": item}
    return results

class Item1(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="这是描述", max_length=30)
    price: float = Field(..., gt=0, description="价格必须大于0")
    tax: Optional[float] = None

class user(BaseModel):
    username: str
    year: str


@app.put("/items")
async def update_item(item: Optional[Item1], user: user, sell: str = Body(...)):
    result = {}
    if item.tax is not None:
        total = item.price * item.tax
        result["price"] = total
        result["name"] = item.name
        result["user"] = user
        result["sell"] = sell
        return result
    result['price'] = item.price
    result['name'] = item.name
    result['user'] = user
    result["sell"] = sell
    return result


@app.get("/items/")
def read_items(*, id: int = Query(..., ge=5, ), q: str):
    results = {"item_id": id}
    if q:
        results.update({"q": q})
    return results


def read_item(
        q: Optional[str] = Query(None, alias="item-query"),
        id: int = Path(..., title="id"),
):
    results = {"item_id": id}
    if q:
        results.update({"q": q})
    return results


# 当你在使用 Query 且需要声明一个值是必需的时，可以将 ... 用作第一个参数值
def read(pw: str = Query(..., min_length=2, max_length=10)):
    results = {"items": [{"oneid": "shanghai"}, {"two": "beijing"}]}
    if pw:
        results.update({"pw": pw})
    return results


@app.get("/items/")
def read(pw: Optional[List[str]] = Query(None)):
    results = {"items": [{"oneid": "shanghai"}, {"two": "beijing"}]}
    if pw:
        results.update({"password": pw})
    return results


def update_items(m: Optional[str] = Query(None, max_length=10, min_length=2, regex='^name')):
    results = {"items": [{"oneid": "shanghai"}, {"two": "beijing"}]}
    if m:
        results.update({"shanghai": m})
    return results


# class Item(BaseModel):
#     name: str
#     desc: Optional[str] = None
#     price: float


@app.post("/items/")
def create_items(item: Item):
    if item.price > 100:
        return "太贵了"
    return item


data = ['北京', '上海', '深圳']


@app.get("/items/")
def read_items(start: int = 0, end: Optional[int] = None):
    if end:
        return data[start:end]
    return data[start:-1]


class ModelName(str, Enum):
    beijing = "1"
    shanghai = "2"


@app.get("/{name}")
def read_root(name: ModelName):
    if name == ModelName.beijing:
        return "北京欢迎您"
    if name == ModelName.shanghai:
        return "你好上海"


@app.get("/one")
def test():
    return {"welcome to shanxi"}


@app.get("/item/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/create")
def post():
    return "post"