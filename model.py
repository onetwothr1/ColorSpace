import os
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import rgb2hex

model_dir = os.getcwd() + os.sep + 'model' + os.sep

device = torch.device('cuda')

interval = 15
color_sample = []
for r in range(0,270,interval):
    for g in range(0,270,interval):
        for b in range(0,270,interval):
            color_sample.append([r,g,b])
color_sample = torch.tensor(color_sample, dtype=torch.float32).cuda()

class ColorMLP(nn.Module):
    def __init__(self, model_name=None, hidden_dim=100, num_block=10, act=nn.Softplus()):
        super().__init__()
              
        self.act = act

        layers = []
        for _ in range(num_block):
          block = [nn.Linear(3, hidden_dim),
                  self.act,
                  nn.Linear(hidden_dim, 3),
                  nn.BatchNorm1d(3)]
          layers += block
        self.MLP = nn.Sequential(*layers).to(device)

        if model_name:
          self.model_name = model_name
          self.param_dir = model_dir + model_name + os.sep + 'parameter' + os.sep
          self.train_history_dir = model_dir + model_name + os.sep + 'train history' + os.sep
          self.image_dir = model_dir + model_name + os.sep + 'image' + os.sep
          if not os.path.exists(model_dir + model_name):
            os.makedirs(model_dir + model_name)
            os.makedirs(model_dir + model_name + os.sep + 'parameter')
            os.makedirs(model_dir + model_name + os.sep + 'train history')
            os.makedirs(model_dir + model_name + os.sep + 'image') 

    def forward(self, x):
        return self.MLP(x)

    def show_space(self, save=False, epoch=None):
        # show the color space by 3D plot with sample colors uniformly selected in RGB space.
        # show from 2 angles, front and back.
        mapped = self.forward(color_sample)
        mapped = mapped.cpu()
        mapped = mapped.detach().numpy()
        
        fig, ax = plt.subplots(ncols=2, figsize=(15, 6), subplot_kw={"projection":"3d"})

        for rgb, (x, y, z) in zip(color_sample, mapped):
          r, g, b = rgb
          ax[0].scatter([x],[y],[z], color=rgb2hex(int(r), int(g), int(b)))
          ax[1].view_init(30, 120)
          ax[1].scatter([x],[y],[z], color=rgb2hex(int(r), int(g), int(b)))
        plt.show()
        if save:
          plt.savefig(model_dir + self.image_dir + f'{self.model_name} epoch {epoch}.png')