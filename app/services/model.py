import pyvista as pv
import numpy as np
import os

def create_card_model(image_array: np.ndarray, filename: str):
  tex = pv.numpy_to_texture(image_array)

  box = pv.Box((-2, 2, -2, 2, -0.01, 0.01))
  box.texture_map_to_plane(inplace=True)

  pl = pv.Plotter()
  pl.add_mesh(box, texture=tex)

  model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/3d', filename)
  pl.export_gltf(model_path, inline_data=True)
  return model_path


def create_slit_model(slit_array: np.ndarray):
  tex = pv.numpy_to_texture(slit_array * 255)
  box = pv.Box((-1, 1, -1, 1, -0.01, 0.01))
  box.texture_map_to_plane(inplace=True)
  
  pl = pv.Plotter()
  pl.add_mesh(box, texture=tex)
  
  model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/3d', 'slit.gltf')

  pl.export_gltf(model_path, inline_data=True)
  return model_path
