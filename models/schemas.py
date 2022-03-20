from typing import Optional, List

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str]


class ItemCreate(ItemBase):
    pass


class Items(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class Users(UserBase):
    id: int
    is_active: bool
    items: List[Items] = []

    class Config:
        orm_mode = True
