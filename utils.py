import math
import numpy as np
import pandas as pd
import os
from PIL import ImageColor
import colorsys

#### edit this ####
color_space_dir = 'color space'
color_space_name = 'colorspace2' ## type the name of the color space
color_space = pd.read_csv('color space/colorspace2/colorspace2 interval 5.csv') ## type the path of the csv file
color_space_15 = pd.read_csv('color space/colorspace2/colorspace2 interval 15.csv') ## type the path of the csv file
color_space_lightness = pd.read_csv('color space/colorspace2/colorspace2 lightness.csv') ## type the path of the csv file

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def rgb2xyz(rgb: tuple):
  # due to the sampling rate (5), the r,g,b values shoud be multiple of 5.
  index = color_space.index[color_space['hexcode']==rgb2hex(*rgb)]
  return (*color_space['X'][index].values, *color_space['Y'][index].values, *color_space['Z'][index].values)

def euclidean(x, y):
  return math.sqrt(sum([(a-b)**2 for a, b in zip(x, y)]))

def distance(rgb1:tuple, rgb2:tuple):
  xyz1 = rgb2xyz(rgb1)
  xyz2 = rgb2xyz(rgb2)
  return euclidean(xyz1, xyz2)

def nearestXYZ(x,y,z, verbose=True):
  # find the nearest point in the space

  interval = 0.1
  index = color_space.index[(x-interval < color_space['X']) & (color_space['X'] < x+interval) &
                  (y-interval < color_space['Y']) & (color_space['Y'] < y+interval) & 
                  (z-interval < color_space['Z']) & (color_space['Z'] < z+interval)]
  if len(index)==0:
    interval *= 2
    index = color_space.index[(x-interval < color_space['X']) & (color_space['X'] < x+interval) &
                  (y-interval < color_space['Y']) & (color_space['Y'] < y+interval) & 
                  (z-interval < color_space['Z']) & (color_space['Z'] < z+interval)]
    if len(index)==0:
      if verbose:
        print(f"the x,y,z coordinate {x, y, z} doesn't exist in the color space")
      return None

  min_idx = index[np.argmin([euclidean((_x, _y, _z), (x,y,z)) for _x, _y, _z, in zip(color_space['X'][index], color_space['Y'][index], color_space['Z'][index])])]
  return (color_space['X'][min_idx], color_space['Y'][min_idx], color_space['Z'][min_idx])

def xyz2rgb(x,y,z, verbose=True):
  # find the nearest point in the space and rgb2xyz it to RGB hexcode

  interval = 0.1
  index = color_space.index[(x-interval < color_space['X']) & (color_space['X'] < x+interval) &
                  (y-interval < color_space['Y']) & (color_space['Y'] < y+interval) & 
                  (z-interval < color_space['Z']) & (color_space['Z'] < z+interval)]
  if len(index)==0:
    interval *= 2
    index = color_space.index[(x-interval < color_space['X']) & (color_space['X'] < x+interval) &
                  (y-interval < color_space['Y']) & (color_space['Y'] < y+interval) & 
                  (z-interval < color_space['Z']) & (color_space['Z'] < z+interval)]
    if len(index)==0:
      if verbose:
        print(f"the x,y,z coordinate {x, y, z} doesn't exist in the color space")
      return None

  min_idx = index[np.argmin([euclidean((_x, _y, _z), (x,y,z)) for _x, _y, _z, in zip(color_space['X'][index], color_space['Y'][index], color_space['Z'][index])])]
  return color_space['hexcode'][min_idx]

def luminosity(r,g,b):
  return math.sqrt( .241 * r + .691 * g + .068 * b )

def hex2rgb(hex):
  return ImageColor.getcolor(hex, "RGB")

def sort_color(hex_list: list, by='hue'):
  if by=='hue':
    hex_list.sort(key=lambda hex: colorsys.rgb_to_hls(*hex2rgb(hex)))
  elif by=='luminosity':
    hex_list.sort(key=lambda hex: luminosity(*hex2rgb(hex)))
  return hex_list

def set_lightness():
  # create a new coordination dataframe by 'lightness' axis which connects two points, white and black.
  white = color_space[color_space['hexcode']=='#ffffff']
  black = color_space[color_space['hexcode']=='#000000']

  white_x = white['X'].values[0]
  white_y = white['Y'].values[0]
  white_z = white['Z'].values[0]

  black_x = black['X'].values[0]
  black_y = black['Y'].values[0]
  black_z = black['Z'].values[0]

  dx = black_x-white_x
  dy = black_y-white_y
  dz = black_z-white_z

  lightness = []
  for _, data in color_space.iterrows():
    x = data['X']
    y = data['Y']
    z = data['Z']
    l = ( (x-white_x)*dx + (y-white_y)*dy + (z-white_z)*dz ) / (dx**2 + dy**2 + dz**2)
    lightness.append(l)

  lightness_df = pd.DataFrame()
  lightness_df['L'] = lightness

  scale_x = math.sqrt(dx**2 + dy**2 + dz**2) / dx
  scale_y = math.sqrt(dx**2 + dy**2 + dz**2) / dy
  lightness_df['X'] = color_space['X'].apply(lambda x: x*scale_x)
  lightness_df['Y'] = color_space['Y'].apply(lambda y: y*scale_y)
  lightness_df['hexcode'] = color_space['hexcode']

  lightness_df.to_csv(color_space_dir + os.sep + color_space_name + os.sep + f'{color_space_name} lightness.csv', index=False)

  global color_space_lightness
  color_space_lightness = lightness_df