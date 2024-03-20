from sqlalchemy import Column,String,Text,ForeignKey,Enum,Table,Integer
from sqlalchemy.orm import relationship
from models.base import Base
from config import bcrypt
from enum import Enum as pyenum


class RoleEnum(pyenum):
  
  user = 'User'
  admin = 'Admin'
  developer = 'Developer'
  
  
class APIMethods(pyenum):
  
  get_method = 'GET'
  put_method = 'PUT'
  post_method = 'POST'
  delete_method = 'DELETE'
  
  
user_role_association = Table(
  'user_role_table',
  Base.metadata,
  Column('user_id',Integer,ForeignKey('user_table.id')),
  Column('role_id',Integer,ForeignKey('role_table.id'))
)

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
  
  roles = relationship('Role',secondary=user_role_association,back_populates='users_list')
  policy_list = relationship('Policy',secondary=policy_user_association,back_populates='user_list')
  
  def __init__(self,name,password,email) -> None:
    
    self.name = name
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    self.email = email
    
class Role(Base):
  
  __tablename__ = 'role_table'
  
  role = Column(Enum(RoleEnum))
  
  users_list = relationship('User',secondary=user_role_association,back_populates='roles')
  

class Service(Base):
  
  __tablename__ = 'service_table'
  
  service_name = Column(String(40),nullable=False,unique=True)
  
class API(Base):
  
  __tablename__ = 'api_table'
  
  api_name = Column(String(40),nullable=False,unique=True)
  api_url = Column(Text,nullable=False)
  method = Column(Enum(APIMethods),nullable=False)
  service_id = Column(Integer,ForeignKey('service_table.id'))
  
  service = relationship('Service',backref='api_list')
  policy_list = relationship('Policy',secondary=policy_api_association,back_populates='api_list')
  

class Policy(Base):
  
  __tablename__ = 'policy_table'
  
  policy_name = Column(String(100),nullable=False)
  
  api_list = relationship('API',secondary=policy_api_association,back_populates='policy_list')
  user_list = relationship('User',secondary=policy_user_association,back_populates='policy_list')
  
  