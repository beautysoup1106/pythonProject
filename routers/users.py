import uvicorn
from fastapi import FastAPI, Depends, HTTPException, APIRouter

from models.crud import *
from models.database import *
from models.schemas import *

userRoute = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 创建新用户
@userRoute.post("/users/", tags=["users"], response_model=Users)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_create = get_user_email(db, user.email)
    if not db_create:
        return db_create_user(db=db, user=user)

    raise HTTPException(status_code=200, detail="账号不能重复")


# 依据user_id查询item
@userRoute.post("/user/item/{user_id}", response_model=List[Items])
def get_user_items(user_id: int, db: Session = Depends(get_db)):
    return get_user_item(db=db, userid=user_id)

#通过用户id查询用户信息
@userRoute.get("/user/{user_id}", response_model=Users)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户查找不到")

    return db_user

# 根据user_id创建item信息
@userRoute.post("/users/{user_id}/items", response_model=Items)
def create_item_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return create_user_item(db=db, item=item, user_id=user_id)
