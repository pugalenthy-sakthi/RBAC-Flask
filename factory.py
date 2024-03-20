from flask import Flask
from config import db,bcrypt,cache,jwt,Config

def create_app():
  
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  bcrypt.init_app(app)
  cache.init_app(app)
  jwt.init_app(app)
  
  return app
  
  