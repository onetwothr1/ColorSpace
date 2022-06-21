import os
import torch
import torch.nn as nn
import pandas as pd
from utils import color_space_dir, rgb2hex
from model import ColorMLP


def save_colorspace(param, hidden_dim, num_block, act, name):
  # save the color space into csv file.
  # columns: X, Y, Z, rgb hexcode

  # Since MLP does not have an inverse function and the model has batchnormalization layer, we have to calculate for entire color range and save the result in table in advance.
  # However, calculating for every possible RGB color takes huge amount of resource, we set a sample rate of 5 and 15.
  # Sampling rate of 15 is only used for 3D visualization and sampling rate of 5 is used for any other usage.

  if not os.path.exists(color_space_dir + os.sep + name):
    os.makedirs(color_space_dir + os.sep + name)

  model = ColorMLP(hidden_dim=hidden_dim, num_block=num_block, act=act)
  model.load_state_dict(torch.load(param))

  for interval in [5, 15]:
    color_sample = []
    for r in range(0,256,interval):
      for g in range(0,256,interval):
        for b in range(0,256,interval):
          color_sample.append([r,g,b])
    color_sample = torch.tensor(color_sample, dtype=torch.float32).cuda()

    mapped = model(color_sample)
    mapped = mapped.cpu().detach().numpy()
    
    color = []
    for r,g,b in color_sample.cpu().detach().numpy():
      color.append(rgb2hex(int(r), int(g), int(b)))

    df = pd.DataFrame({'X': mapped[:,0], 'Y': mapped[:,1], 'Z': mapped[:,2], 'hexcode': color})
    df.to_csv(color_space_dir + os.sep + name + os.sep + f'{name} interval {interval}.csv', index=False)