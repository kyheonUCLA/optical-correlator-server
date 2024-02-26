import numpy as np

def slit_x(slit_width, slit_height, n=1, slit_space=0):
  # Step  1: Create a  1600x1600 array filled with zeros
  array = np.zeros((1600,  1600))
  
  # Step  2: Calculate the total space needed for all slits including spaces
  totalslit_space = (n -  1) * slit_space
  totalslit_width = n * slit_width
  
  # Step  3: Calculate the starting x position for the first slit
  startX = (1600 - totalslit_width - totalslit_space) //  2
  if startX <  0:
    raise ValueError('The specified number of slits and spaces cannot fit within the array dimensions.')
  
  # Step  4: Loop through each slit and create them
  for i in range(n):
    # Calculate the y position for the current slit
    startY = (1600 - slit_height) //  2
    
    # Ensure the slit fits within the array boundaries
    startY = max(startY,  0)
    endY = min(startY + slit_height,  1600)
    
    # Fill the slit area with ones (or another value)
    array[startY:endY, startX + i * (slit_width + slit_space):startX + i * (slit_width + slit_space) + slit_width] =  1
  
  return array

def slit_y(slit_width, slit_height, n=1, slit_space=0):
  array = np.zeros((1600,  1600))
  
  total_slit_space = (n -  1) * slit_space
  total_slit_height = n * slit_height
  
  start_y = (1600 - total_slit_height - total_slit_space) //  2
  if start_y <  0:
      raise ValueError('The specified number of slits and spaces cannot fit within the array dimensions.')
  
  # Step  4: Loop through each slit and create them
  for i in range(n):
    start_x = (1600 - slit_width) //  2
    start_x = max(start_x,  0)
    end_x = min(start_x + slit_width,  1600)
    array[start_y + i * (slit_height + slit_space):start_y + i * (slit_height + slit_space) + slit_height, start_x:end_x] =  1
  
  return array

def slit_r(r1, r2=0):
  array = np.zeros((1600,  1600))
  ri = min(r1, r2)
  ro = max(r1, r2)

  y, x = np.ogrid[-800:800, -800:800]
  mask_i = x*x + y*y >= ri*ri
  mask_o = x*x + y*y > ro*ro

  array[mask_i] =  1
  array[mask_o] = 0
  
  return array

