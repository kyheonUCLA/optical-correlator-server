import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  # PLOTTING_BACKEND = os.environ['MPLBACKEND'] = 'Agg'
