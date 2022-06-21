import os
from plotly.offline import plot, iplot, init_notebook_mode
import plotly.graph_objs as go
from utils import rgb2hex, color_space_15, color_space_name

init_notebook_mode(connected=True) # if you use notebook


data = go.Scatter3d(
    x=color_space_15['X'],
    y=color_space_15['Y'],
    z=color_space_15['Z'],
    text=color_space_15['hexcode'],
    mode='markers',
    marker=dict(
        size=3,
        color=color_space_15['hexcode'],
        opacity= 1.0
    )
)

layout = go.Layout(
    width=750,
    height=750,
)

fig = go.Figure(data=[data], layout=layout)

# fig.show()
# fig.show(renderer="colab") # for colab environment

# save it to html file
plot(fig, filename='color space' + os.sep + color_space_name + os.sep + f'{color_space_name} 3D.html', auto_open=False)