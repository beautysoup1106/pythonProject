from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Query, Path, Body, Header, Cookie, Depends, HTTPException

from enum import Enum

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, HttpUrl

def verify_token(token: str = Header(...)):
    if token != "jintianxingqiyi":
        raise HTTPException(status_code=400, detail="Token head is invalid")


app = FastAPI(dependencies=[Depends(verify_token)])

fake_item_db = [{"city": "beijing"}, {"city": "shanghai"}, {"city": "baoji"}]


@app.get("/item/")
def read_item(city: str):
    for item in fake_item_db:
        if item['city'] == city:
            return item
    return {"msg": "not excit"}


def verify_key(key: str = Header(...)):
    if key != "key":
        raise HTTPException(status_code=400, detail="Key header invaild")
    return key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
def read_items():
    return fake_item_db


def query_extractor(desc: Optional[str] = None):
    return desc


def query__extractor(
        desc: str = Depends(query_extractor),
        name: Optional[str] = '',
):
    if not desc:
        return name
    return desc


@app.get("/items1/")
def read_item(query__extractor: str = Depends(query__extractor)):
    return query__extractor


class CommonQueryParams:

    def __init__(self, desc: str, skip: int = 0, limit: int = 100):
        self.desc = desc
        self.skip = skip
        self.limit = limit


@app.get("/items/")
def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.desc:
        response.update({"desc": commons.desc})
    items = fake_item_db[commons.skip:commons.skip + commons.limit]
    response.update({"items": items})
    return response
