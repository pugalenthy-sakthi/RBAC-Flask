from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_bcrypt import Bcrypt
import redis


load_dotenv()

class Config:
  
  PORT = os.getenv('PORT')
  SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_DB_URL')
  JWT_SECRET_KEY = os.getenv('APP_JWT_SECRET')
  JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
  JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES'))
  
  CACHE_TYPE = os.getenv('FLASK_CACHE_TYPE')
  CACHE_REDIS_HOST = os.getenv('FLASK_CACHE_REDIS_HOST')
  CACHE_REDIS_PORT = os.getenv('FLASK_CACHE_REDIS_PORT')
  CACHE_REDIS_DB = os.getenv('FLASK_CACHE_REDIS_DB')
  
db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()
bcrypt = Bcrypt()
redis_client = redis.Redis(host=Config.CACHE_REDIS_HOST,port=Config.CACHE_REDIS_PORT,db=Config.CACHE_REDIS_DB)
  
  