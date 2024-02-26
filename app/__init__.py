from flask import Flask
from config import Config
from flask_cors import CORS

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)
  CORS(app)

  from app.api import api_bp
  app.register_blueprint(api_bp, url_prefix='/api')

  from app.resources import resources_bp
  app.register_blueprint(resources_bp, url_prefix='/resources')

  return app

