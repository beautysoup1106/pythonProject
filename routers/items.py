from typing import List

from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from models.crud import get_item
from models.database import SessionLocal
from models.schemas import Items

itemRoute = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 查询item信息（查看具体接口实现函数，是否需要调用接口时传入参数）
@itemRoute.get("/items/", response_model=List[Items])
def read_items(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    items = get_item(db=db, skip=skip, limit=limit)
    return items
