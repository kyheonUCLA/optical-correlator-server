from flask import request, send_file, after_this_request
from app.api import api_bp as bp
from app.services.model import create_card_model
from app.services.fourier import amplitude, diffraction
from app.services.plots import plot_diffraction, get_raw_plot_array, create_color_map
from app.services.optics import slit_x
import matplotlib
matplotlib.use('Agg') # change backend to be multi-core safe
from matplotlib import pyplot as plt
import PIL.Image, PIL.ImageOps
import numpy as np
import pint


# this works and i have no idea why
@bp.route('/output', methods=['POST'])
def upload_output():
  if 'file' not in request.files:
    return 'No file part'
  u = pint.UnitRegistry()
  image_file = request.files['file']
    
  im = np.array(PIL.Image.open(image_file))

  lam = 660*u.nm
  A, x, y = amplitude(im, (2*u.mm, 2*u.mm))
  solve, kx, ky = diffraction(A, lam, x, y)
  fig, ax = plt.subplots()
  cmap = create_color_map(lam.magnitude)
  plot_diffraction(solve(3*u.cm), x, y, cmap, fig, ax)

  image_array = get_raw_plot_array(fig, ax)
  model_path = create_card_model(image_array, 'diffraction.gltf')  

  @after_this_request
  def close_figures(response):
    plt.close(fig)
    return response
  
  return send_file(model_path)


@bp.route('/input', methods=['POST'])
def upload_input():

  if 'file' not in request.files:
    return 'No file part'

  image_file = request.files['file']
 
  im = PIL.Image.open(image_file)
  im = im.convert('L')
  im = PIL.ImageOps.fit(im, (1600, 1600))
  image_array = np.array(im, dtype=np.uint8)
  filepath = create_card_model(image_array, 'input.gltf')  
  
  return send_file(filepath)
  

@bp.route('/filter', methods=['POST'])
def upload_filter():
  if 'file' not in request.files:
    return 'No file part'
  image_file = request.files['file']
 
  im = PIL.Image.open(image_file)
  im = im.convert('L')
  im = PIL.ImageOps.fit(im, (1600, 1600))
  image_array = np.array(im, dtype=np.uint8)
  filepath = create_card_model(image_array, 'filter.gltf')  

  return send_file(filepath)
  

