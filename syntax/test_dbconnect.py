from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Query, Path, Body, Header, Cookie, Depends, HTTPException

from enum import Enum

from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import create_engine, Column, INTEGER, String, VARCHAR, text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from starlette import status

# app = FastAPI()
# db connect config
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_DB = 'test_db'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

# 创建对象的基类
Base = declarative_base()

# 初始化数据库连接
engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(bind=engine)


class DBUser(Base):
    __tablename__ = 'test_user'

    id = Column(INTEGER, primary_key=True, comment='编号')
    username = Column(String(100))
    password = Column(String(100))
    sex = Column(VARCHAR(10), server_default=text("''"), comment='性别')
    login_time = Column(INTEGER, server_default=text("'0'"), comment='登陆时间，主要为了登陆JWT校验使用')
    create_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    @classmethod
    def add(cls, db: Session, data):
        db.add(data)
        db.commit()

    @classmethod
    def get_by_username(cls, db: Session, username):
        data = db.query(cls).filter_by(username=username).first()

        return data

    @classmethod
    def update(cls, db: Session, username, sex):
        db.query(cls).filter_by(username=username).update({cls.sex: sex})
        db.commit()

#创建新的数据表test_user
# Base.metadata.create_all(engine)

#

#获取session，然后把对象添加到session
session = SessionLocal()

print(DBUser.get_by_username(session, username='test_yxx'))

# new_user = DBUser(id=8, username='test_yxx', password='test_123')
#
# DBUser.add(session, new_user)
# session.add(new_user)
# session.commit()
# session.close()

# @app.post("/register", response_model=User)
# async def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     password = get_password_hash(form_data.password)
#
#     db_user = DBUser.get_by_username(db, form_data.username)
#     if db_user:
#         return db_user
#
#     db_user = DBUser(username=form_data.username, password=password)
#     DBUser.add(db, db_user)
#
#     return db_user
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
