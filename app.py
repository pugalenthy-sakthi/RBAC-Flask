
from factory import create_app
from config import db
from flask_migrate import Migrate
from models.models import *



app = create_app()
migrate = Migrate(app,db)


if __name__ == '__main__':
  
  app.run(debug=True,port=app.config['PORT'])