from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Query, Path, Body, Header, Cookie, Depends, HTTPException

from enum import Enum

from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, HttpUrl
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users = {
    "monday": {
        "username": "monday",
        "fullname": "mondayisgoodday",
        "email": "monday@monday.com",
        "hashed_password": "monday",
        "disabled": True
    }
}

fake_item_db = [{"city": "beijing"}, {"city": "shanghai"}, {"city": "tianjin"}]

app = FastAPI()


def fake_hash_password(password: str):
    return password


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users, token)
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication",
            headers={"WWW-Authentication": "Bearer"},
        )
    return user


@app.post("/login")
def login(form_fata: OAuth2PasswordRequestForm = Depends()):
    # 校验密码¶
    # 目前我们已经从数据库中获取了用户数据，但尚未校验密码。

    # 让我们首先将这些数据放入 Pydantic UserInDB 模型中。
    # 永远不要保存明文密码，因此，我们将使用（伪）哈希密码系统。

    # 如果密码不匹配，我们将返回同一个错误。
    user_dict = fake_users.get(form_fata.username)
    print(user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="用户名错误")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_fata.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="密码错误")
    return {"access_token": user.username, "token_type": "bearer"}


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="已经删除")
    return current_user


@app.get("/user/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    print(current_user)
    return current_user


@app.get("/items/")
def read_items():
    return fake_item_db


@app.get("/item")
def read_item(city: str, token: str = Depends(oauth2_scheme)):
    for item in fake_item_db:
        if item["city"] == city:
            return item
    return {"msg": "not exist"}
