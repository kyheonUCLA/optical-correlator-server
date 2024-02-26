from flask import request, send_file, send_from_directory
from app.resources import resources_bp as bp
import os

@bp.route('images/<path:filename>')
def serve_image(filename):
  static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static')
  return send_from_directory(os.path.join(static_path, 'images'), filename)

@bp.route('models/<path:filename>')
def serve_model(filename):
  static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static')
  return send_from_directory(os.path.join(static_path, '3d'), filename)

