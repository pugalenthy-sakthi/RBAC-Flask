from sqlalchemy import Column,String,Text,ForeignKey,Enum,Table,Integer,DateTime,func,Boolean
from sqlalchemy.orm import relationship
from models.base import Base
from config import bcrypt
from enum import Enum as pyenum

  
  
class APIMethods(pyenum):
  
  get_method = 'GET'
  put_method = 'PUT'
  post_method = 'POST'
  delete_method = 'DELETE'

policy_api_association = Table(
  'policy_api_table',
  Base.metadata,
  Column('policy_id',Integer,ForeignKey('policy_table.id')),
  Column('api_id',Integer,ForeignKey('api_table.id'))
)

policy_user_association = Table(
  'policy_user_table',
  Base.metadata,
  Column('user_id',Integer,ForeignKey('user_table.id')),
  Column('policy_id',Integer,ForeignKey('policy_table.id'))
)

class User(Base):
  
  __tablename__ = 'user_table'
  
  name = Column(String(50),nullable=False)
  password = Column(Text,nullable=False)
  email = Column(String(80),nullable=False,unique=True)
  isdev = Column(Boolean,default=False)

  policy_list = relationship('Policy',secondary=policy_user_association,back_populates='user_list')
  activities = relationship('Activity',uselist=True, back_populates='user')
  
  def __init__(self,name,password,email) -> None:
    
    self.name = name
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    self.email = email
    
class Activity(Base):
    
    __tablename__ = 'user_activity_table'
    
    user_id = Column(Integer,ForeignKey('user_table.id'),nullable=False)
    
    login_at = Column(DateTime(timezone=True),default=func.now())
    
    logout_at = Column(DateTime(timezone=True))
    
    session_id = Column(String(50),nullable=False)
    
    def __init__(self,user):
        self.user = user
    
    user = relationship('User', back_populates='activities')
  
  
class API(Base):
  
  __tablename__ = 'api_table'
  
  api_name = Column(String(40),nullable=False,unique=True)
  api_url = Column(Text,nullable=False)
  method = Column(Enum(APIMethods),nullable=False)

  policy_list = relationship('Policy',secondary=policy_api_association,back_populates='api_list')
  

class Policy(Base):
  
  __tablename__ = 'policy_table'
  
  policy_name = Column(String(100),nullable=False)
  
  api_list = relationship('API',secondary=policy_api_association,back_populates='policy_list')
  user_list = relationship('User',secondary=policy_user_association,back_populates='policy_list')
  
  