from flask import Flask
from config import db,bcrypt,cache,jwt,Config
from views import auth_route,dev_route,policy_route,service_route,user_route

def create_app():
  
  app = Flask(__name__)
  app.config.from_object(Config)
  app.register_blueprint(auth_route.auth_route)
  app.register_blueprint(dev_route.dev_route)
  app.register_blueprint(policy_route.policy_route)
  app.register_blueprint(service_route.service_route)
  app.register_blueprint(user_route.user_route)
  db.init_app(app)
  bcrypt.init_app(app)
  cache.init_app(app)
  jwt.init_app(app)
  
  return app
  
  