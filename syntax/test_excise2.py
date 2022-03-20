from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Query, Path, Body, Header, Cookie

from enum import Enum

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "one": {"name": "香蕉", "price": 50.2}
}


@app.put("/items/", response_model=Item)
def update_item(name: str, item: Item):
    stored_item_data = items[name]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    update_item = stored_item_model.copy(update=update_data)
    items[name] = jsonable_encoder(update_item)
    return update_item


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: str):
    return items[item_id]


# @app.get("/items")
# def read_items(name: Optional[str] = Cookie(None),
#                token: Optional[str] = Header(None)):
#     if token is None or name != "456":
#         return '无权限'
#     if name is None or token != "123":
#         return '认证失败'

    # print(ads_id)
    # return {"ads_id": ads_id}


# def read_item(user_agent: Optional[str] = Header(None)):
#     return {"user-agent": user_agent}


# @app.put("/items/{item_id}")
# async def read_items(
#         item_id: UUID,
#         start_time: Optional[datetime] = Body(None),
#         end_time: Optional[datetime] = Body(None),
#         after: Optional[timedelta] = Body(None)
# ):
#     start_process = start_time
#     duration = end_time - start_process
#     return {
#         "id": item_id,
#         "start_time": start_time,
#         "end_time": end_time,
#         "after": after,
#         "start_process": start_process,
#         "duration": duration
#
#     }