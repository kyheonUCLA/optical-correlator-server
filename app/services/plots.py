from matplotlib.colors import LinearSegmentedColormap
import PIL.Image
import io
import numpy as np
from scipy.fft import fftshift


def plot_kspace(A, kx, ky, color_map, fig, ax):
  kxv, kyv = np.meshgrid(kx, ky)
  ax.pcolormesh(fftshift(kxv.magnitude), fftshift(kyv.magnitude), np.abs(fftshift(A)), cmap=color_map)
  ax.set_xlabel('$y frequency$ [mm$^{-1}$]')
  ax.set_ylabel('$x frequency$ [mm$^{-1}$]')
  ax.set_title('Fourier Transform')
  ax.set_xlim([-100, 100])
  ax.set_ylim([-100, 100])
  # plot_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/3d', filename)
  return fig, ax

def plot_diffraction(U, x, y, color_map, fig, ax):
  xv, yv = np.meshgrid(x, y)
  ax.pcolormesh(xv, yv, np.abs(U), cmap=color_map)
  ax.set_xlabel('$x$ [mm]')
  ax.set_ylabel('$y$ [mm]')
  ax.set_title('Diffraction Pattern')
  fig.savefig('f.png')
  return fig, ax

def get_raw_plot_array(fig, ax):
  ax.axis('off')
  title = ax.get_title()
  ax.set_title('')
  buffer = io.BytesIO()
  fig.savefig(buffer, format='png', bbox_inches='tight', transparent=True, pad_inches=0)
  buffer.seek(0)  # Rewind the buffer to the beginning
  img = PIL.Image.open(buffer)
  # buffer.close()
  ax.axis('on')
  ax.set_title(title)
  return np.array(img, dtype=np.uint8)


# wavelength is in nm, gamma is an attenuation factor 
def wavelength_to_rgb(wavelength: float, gamma: float=0.8):
  if wavelength >= 380 and wavelength <= 440:
    attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
    R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
    G = 0.0
    B = (1.0 * attenuation) ** gamma
  elif wavelength >= 440 and wavelength <= 490:
    R = 0.0
    G = ((wavelength - 440) / (490 - 440)) ** gamma
    B = 1.0
  elif wavelength >= 490 and wavelength <= 510:
    R = 0.0
    G = 1.0
    B = (-(wavelength - 510) / (510 - 490)) ** gamma
  elif wavelength >= 510 and wavelength <= 580:
    R = ((wavelength - 510) / (580 - 510)) ** gamma
    G = 1.0
    B = 0.0
  elif wavelength >= 580 and wavelength <= 645:
    R = 1.0
    G = (-(wavelength - 645) / (645 - 580)) ** gamma
    B = 0.0
  elif wavelength >= 645 and wavelength <= 750:
    attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
    R = (1.0 * attenuation) ** gamma
    G = 0.0
    B = 0.0
  else:
    R = 0.0
    G = 0.0
    B = 0.0
  return (R,G,B)

def create_color_map(lam: int):
  return LinearSegmentedColormap.from_list('custom', [(0,0,0), wavelength_to_rgb(lam)], N=256)
