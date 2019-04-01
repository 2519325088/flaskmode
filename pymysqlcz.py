import sqlalchemy
#数据库部分
from sqlalchemy import create_engine

engine =create_engine("mysql+mysqlconnector://root:root@localhost/flaska",encoding='utf8', echo=True)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey
Base=declarative_base(bind=engine)
class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True,autoincrement=True,nullable=True,unique=True)
    username=Column(String(11),unique=True,nullable=True)
    passwd =Column(String(18),nullable=True)

class Splist(Base):
    __tablename__='splist'
    id=Column(Integer,primary_key=True,autoincrement=True,nullable=True,unique=True)
    spname=Column(String(150),nullable=True)
    nrtext= Column(String)
    userid=Column(Integer , ForeignKey('user.id'),nullable=True)

# from sqlalchemy.orm import sessionmaker
# Session=sessionmaker(bind=engine)()
#数据库导入结束