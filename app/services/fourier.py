import numpy as np
from scipy.fft import fft2
from scipy.fft import ifft2
from scipy.fft import fftfreq
import pint 

def amplitude(image_array: np.ndarray, physical_dims: tuple[pint.Quantity, pint.Quantity]):
  # normalizs the image from (0 - 255) greyscale to (0 - 1) light intensity
  U0 = np.float32(image_array / 255)
  
  # extracting width and height info of the actual input/filter
  w = physical_dims[0]
  h = physical_dims[1]

  # creates an array the same size as image, discretized between physical screen dimensions 
  size_x, size_y = U0.shape
  x = np.linspace(-w.magnitude, w.magnitude, size_x) * w.units
  y = np.linspace(-h.magnitude, h.magnitude, size_y) * h.units

  # uses 2D fourier transform to solve for initial amplitude
  A = fft2(U0)
  return A, x, y

def diffraction(A, wavelength: pint.Quantity, x: np.ndarray, y: np.ndarray):
  # creates discretized frequency domain analoge of x, y arrays
  kx = fftfreq(len(x), np.diff(x)[0]) * 2 * np.pi 
  ky = fftfreq(len(y), np.diff(y)[0]) * 2 * np.pi
  kxv, kyv = np.meshgrid(kx, ky)

  # wavenumber of monoenergetic beam
  k = 2 * np.pi / wavelength

  # creates function to solve helmholtz equation given ditance z 
  U = lambda z: ifft2( A*np.exp(1j*z*np.sqrt(k**2-kxv**2-kyv**2)) )
  return U, kx, ky

 