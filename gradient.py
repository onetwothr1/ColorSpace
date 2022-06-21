import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from utils import rgb2xyz, xyz2rgb, color_space_name, color_space_dir

def gradient(start_rgb:tuple, end_rgb:tuple, num=15, imagesize=(10,4), show=True, save=False, savename=None):
  # show gradient in equal distance
  x_s, y_s, z_s = rgb2xyz(start_rgb)
  x_e, y_e, z_e = rgb2xyz(end_rgb)
  x_interval = (x_e - x_s) / (num-1)
  y_interval = (y_e - y_s) / (num-1)
  z_interval = (z_e - z_s) / (num-1)

  colors = []
  for i in range(num):
    _x = x_s + x_interval * i
    _y = y_s + y_interval * i
    _z = z_s + z_interval * i
    hexcode = xyz2rgb(_x, _y, _z)
    colors.append(hexcode)
  
  # show
  fig = plt.figure(figsize=imagesize) # image width, height
  fig.subplots_adjust(wspace=0)
  for i in range(num):
    ax = fig.add_subplot(1,num, i+1)
    ax.axis('off')
    ax.add_patch(
        patches.Rectangle(
            (0,0), 1, 1,
            facecolor=colors[i],
            fill=True
        )
    )
  plt.axis('off')

  if show:
    plt.show()

  if save:
    if not os.path.exists(color_space_dir + os.sep + color_space_name + os.sep + 'gradient'):
        os.makedirs(color_space_dir + os.sep + color_space_name + os.sep + 'gradient')
    plt.savefig(color_space_dir + os.sep + color_space_name + os.sep + 'gradient' + os.sep + f'gradient {savename}.png')
  plt.clf()


color_pair = [
              [(0,0,0), (255,255,255)], # white to black

              [(0,0,0), (255,0,0)], # white to R,G,B
              [(0,0,0), (0,255,0)],
              [(0,0,0), (0,0,255)],

              [(255,255,255), (255,0,0)], # black to R,G,B
              [(255,255,255), (0,255,0)],
              [(255,255,255), (0,0,255)],

              [(255,0,0), (0,255,0)], # R <-> G <-> B
              [(0,255,0), (0,0,255)],
              [(0,0,255), (255,0,0)],

              [(255,255,0), (255,0,0)], # R <-> magenta, yellow
              [(255,0,255,), (255,0,0)],
              [(255,255,0), (0,255,0)], # G <-> cyan, yellow
              [(0,255,255), (0,255,0)],
              [(255,0,255), (0,0,255)], # B <-> magent, cyan
              [(0,255,255), (0,0,255)],

              [(255,255,0), (255,0,255)], # magenta <-> cyan <-> yellow
              [(255,0, 255), (0,255,255)],
              [(0,255,255), (255,255,0)],

              [(255,0,0), (0,255,255)], # complementary colors
              [(0,255,0), (255,0,255)],
              [(0,0,255), (255,255,0)],
]

if __name__=='__main__':
  for i, (color1, color2) in enumerate(color_pair):
    gradient(color1, color2, show=False, save=True, savename=i)