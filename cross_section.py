import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from utils import color_space, color_space_lightness, color_space_dir, color_space_name

x_min = min(color_space['X'])
x_max = max(color_space['X'])
y_min = min(color_space['Y'])
y_max = max(color_space['Y'])
z_min = min(color_space['Z'])
z_max = max(color_space['Z'])

def cross_section_x(x, interval=0.05, show=True, save=None):
  index = color_space.index[(x-interval < color_space['X']) & (color_space['X'] < x+interval)]
  plt.scatter(x=color_space.iloc[index]['Y'], y=color_space.iloc[index]['Z'], c=color_space.iloc[index]['hexcode'])
  plt.title('cross section of X=%.2f' %x)
  plt.xlabel("Y")
  plt.ylabel("Z")
  plt.xlim([y_min, y_max])
  plt.ylim([z_min, z_max])
  if show:
    plt.show()
  if save:
    plt.savefig(save + os.sep + 'X=%.2f.png'%x)
  plt.clf()

def cross_section_y(y, interval=0.05, show=True, save=None):
  index = color_space.index[(y-interval < color_space['Y']) & (color_space['Y'] < y+interval)]
  plt.scatter(x=color_space.iloc[index]['X'], y=color_space.iloc[index]['Z'], c=color_space.iloc[index]['hexcode'])
  plt.title('cross section of Y=%.2f' %y)
  plt.xlabel("X")
  plt.ylabel("Z")
  plt.xlim([x_min, x_max])
  plt.ylim([z_min, z_max])
  if show:
    plt.show()
  if save:
    plt.savefig(save + os.sep + 'Y=%.2f.png'%y)
  plt.clf()

def cross_section_z(z, interval=0.05, show=True, save=None):
  index = color_space.index[(z-interval < color_space['Z']) & (color_space['Z'] < z+interval)]
  plt.scatter(x=color_space.iloc[index]['X'], y=color_space.iloc[index]['Y'], c=color_space.iloc[index]['hexcode'])
  plt.title('cross section of Z=%.2f' %z)
  plt.xlabel("X")
  plt.ylabel("Y")
  plt.xlim([x_min, x_max])
  plt.ylim([y_min, y_max])
  if show:
    plt.show()
  if save:
    plt.savefig(save + os.sep + 'Z=%.2f.png'%z)
  plt.clf()

def cross_section_lightness(lightness, interval=0.05, show=True, save=None):
  # lightness: 0~1
  # before execute this function, you first have to execute "utils.set_lightness()", make a csv file of the color space with lightness axis, and type the path of the csv file in utils.color_space_lightness.
  index = color_space.index[(lightness-interval < color_space_lightness['L']) & (color_space_lightness['L'] < lightness+interval)]
  plt.scatter(x=color_space_lightness.iloc[index]['X'], y=color_space_lightness.iloc[index]['Y'], c=color_space.iloc[index]['hexcode'])
  plt.title('cross section of lightness=%.2f' %lightness)
  plt.xlabel("X")
  plt.ylabel("Y")
  plt.xlim([min(color_space_lightness['X']), max(color_space_lightness['X'])])
  plt.ylim([min(color_space_lightness['Y']), max(color_space_lightness['Y'])])
  if show:
    plt.show()
  if save:
    plt.savefig(save + os.sep + 'L=%.2f.png'%l)
  plt.clf()


if __name__=='__main__':
  save_dir = color_space_dir + os.sep + color_space_name + os.sep + 'cross section'
  if not os.path.exists(save_dir):
    os.makedirs(save_dir)

  for x in np.arange(x_min + (x_max-x_min)/10, x_max, (x_max-x_min)/10):
    cross_section_x(x=x, show=False, save=save_dir)
    
  for y in np.arange(y_min + (y_max-y_min)/10, y_max, (y_max-y_min)/10):
    cross_section_y(y=y, show=False, save=save_dir)
    
  for z in np.arange(z_min + (z_max-z_min)/10, z_max, (z_max-z_min)/10):
    cross_section_z(z=z, show=False, save=save_dir)
    
  for l in np.arange(0.1,1,0.1):
    cross_section_lightness(lightness=l, show=False, save=save_dir)