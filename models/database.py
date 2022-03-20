# db connect config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
