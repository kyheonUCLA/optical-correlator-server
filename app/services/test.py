import matplotlib
matplotlib.use('Agg') 
from matplotlib import pyplot as plt
from scipy.fft import fftshift
from model import create_card_model
from fourier import diffraction, amplitude
from optics import slit_y, slit_x
from plots import plot_kspace, plot_diffraction, get_raw_plot_array, create_color_map
import numpy as np
import pint
u = pint.UnitRegistry()
from matplotlib.colors import LinearSegmentedColormap

image_name = 'slit.png'
im = np.uint8(slit_x(12, 1000, n=2, slit_space=50) * 255)
lam = 660*u.nm
A, x, y = amplitude(im, (2*u.mm, 2*u.mm))
I, kx, ky = diffraction(A, lam, x, y)

U = I(3*u.cm)

xv, yv = np.meshgrid(x, y)
kxv, kyv = np.meshgrid(kx, ky)

cmap = create_color_map(lam.magnitude)

f, a = plt.subplots()
plot_diffraction(U, x, y, cmap, f, a)

image_array = get_raw_plot_array(f, a)
diff_model = create_card_model(image_array, 'diffraction.gltf')  




# plt.show()