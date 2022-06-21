import matplotlib.pyplot as plt
import matplotlib.patches as patches
from plotly.offline import plot, iplot, init_notebook_mode
import plotly.graph_objs as go
from utils import *
import random

def palette_generator(num, repulsion=0.5, exponent=4, max_step=50, threshold=0.05, show_history=False, show_palette=False, show_3D=False, show_3D_begin=False):
    '''
    Algorithm follows code from IWantHue (https://medialab.github.io/iwanthue/js/libs/chroma.palette-gen.js)
    '''
    # num: number of colors
    # repulsion: the force of repulsion. big repulsion makes the points to move far away
    # exponent: if you set exponent bigger, closer points will have higher repulsion
    # step: after this step, iteration stops.
    # threhold: If the mean distance does not increase by more than (1 + threshold), iteration stops.
    #
    # return: list of RGB hexcodes

    # randomly generate colors in RGB space and convert them to color space
    colors = []
    rgb = []
    for i in range(num):
        random_rgb = [random.randint(0,51) * 5, random.randint(0,51) * 5, random.randint(0,51) * 5]
        rgb.append(random_rgb)
        colors.append(rgb2xyz(random_rgb))

    if show_3D_begin:
        print("inital random colors")
        show_3d(np.array(colors), [rgb2hex(r,g,b) for r,g,b in rgb])

    iter = 0
    distance_mean_list = []
    if show_history:
        distance_min_list = []
        distance_max_list = []
        magnitude_mean_list = []
        magnitude_min_list = []
        magnitude_max_list = []
        exceed_points = []

    while True:
        iter += 1

        ## Initialize Vector
        vectors = [[0,0,0] for i in range(num)]
        
        ## Compute Force
        distance_list = []
        for i in range(num):
            color1 = colors[i]
            for j in range(i):
                color2 = colors[j]
                dx, dy, dz = [a-b for a, b in zip(color1, color2)]
                d = euclidean(color1, color2)
                distance_list.append(d)
                if d==0:
                    continue
                force = repulsion / (d**exponent)
                
                vectors[i][0] += dx * force
                vectors[i][1] += dy * force
                vectors[i][2] += dz * force

                vectors[j][0] -= dx * force
                vectors[j][1] -= dy * force
                vectors[j][2] -= dz * force
            
        mean_distance = sum(distance_list)/ (num * (num - 1) / 3)
        distance_mean_list.append(mean_distance)
        if show_history:
            distance_min_list.append(min(distance_list))
            distance_max_list.append(max(distance_list))

        ## Apply Force
        magnitude_list = []
        exceed_count = 0 # count if the force vector make a point to exceed the color space.
        for i in range(num):
            color = colors[i]

            magnitude = math.sqrt(sum([x**2 for x in vectors[i]]))
            magnitude_list.append(magnitude)

            scale = 1.0
            candidate_color = color[0] + vectors[i][0] * scale, color[1] + vectors[i][1] * scale, color[2] + vectors[i][2] * scale

            # if the force vector make a point to exceed the color space, half down the force vector and try again for several times.
            halving_cnt = 0
            nearest = nearestXYZ(*candidate_color, verbose=False)
            while nearest==None and halving_cnt<=20:
                scale *= 0.5
                candidate_color = color[0] + vectors[i][0] * scale, color[1] + vectors[i][1] * scale, color[2] + vectors[i][2] * scale
                nearest = nearestXYZ(*candidate_color, verbose=False)
                halving_cnt += 1
            if nearest != None:
                colors[i] = nearest
            else:
                exceed_count += 1

        if show_history:
            exceed_points.append(exceed_count)
            magnitude_mean_list.append(sum(magnitude_list)/ num)
            magnitude_min_list.append(min(magnitude_list))
            magnitude_max_list.append(max(magnitude_list))

        ## check the stop condition
        if iter>2 and distance_mean_list[-1] < distance_mean_list[-2] * (1+threshold):
            break
        if iter==max_step:
            break
        
    ### Visualization ###
    colors_hex = [xyz2rgb(*color) for color in colors]

    if show_3D:
        print("color palette result")
        show_3d(np.array(colors), colors_hex)

    if show_palette:
        print("sorted in hue")
        show_color_code(colors_hex, sort='hue')
        print("sorted in luminosity")
        show_color_code(colors_hex, sort='luminosity')

    if show_history:
        print('distancing history')
        fig = plt.figure(figsize=(14,5))
        ax1 = fig.add_subplot(1,3,1)
        ax1.plot(magnitude_mean_list, label='mean magnitude')
        ax1.plot(magnitude_min_list, label='min magnitude')
        ax1.plot(magnitude_max_list, label='max magnitude')
        ax1.legend()
        ax2 = fig.add_subplot(1,3,2)
        ax2.plot(distance_mean_list, label='mean distance')
        ax2.plot(distance_min_list, label='min distance')
        ax2.plot(distance_max_list, label='max distance')
        ax2.legend()
        ax3 = fig.add_subplot(1,3,3)
        ax3.plot(exceed_points, label='num exceeded points')
        ax3.legend()
        plt.show()

    return colors_hex

def show_color_code(color_code, num_row=10, width=15, height_scale=0.2, sort='hue'):
    color_code = sort_color(color_code, by=sort)

    fig = plt.figure(figsize=(width, len(color_code) * height_scale))
    plt.axis('off')
    
    for i, color in enumerate(color_code):
        ax = fig.add_subplot(len(color_code)//num_row+1, num_row, i+1)
        ax.axis('off')

        ax.add_patch(
            patches.Rectangle(
            (0,0),
            1,
            1,
            facecolor = color,
            fill=True
            ) )
    plt.axis('off')
    plt.show()

def show_3d(color_code_xyz, color_code_hex):
    # visualize picked colors among entire color space
    data = go.Scatter3d(
        x=color_space_15['X'],
        y=color_space_15['Y'],
        z=color_space_15['Z'],
        text=color_space_15['hexcode'],
        mode='markers',
        marker=dict(
            size=3,
            color=color_space_15['hexcode'],
            opacity= 0.15
        )
    )
    
    layout = go.Layout(
        width=750,
        height=750,
    )
    
    fig = go.Figure(data=[data], layout=layout)
    
    fig.add_trace(
        go.Scatter3d(x=color_code_xyz[:,0],
                    y=color_code_xyz[:,1],
                    z=color_code_xyz[:,2],
                    text = color_code_hex,
                    mode='markers',
                    marker=dict(size=5,
                                color=color_code_hex,
                                opacity=1)
                    )
    )
    
    # fig.show(renderer="colab") # if the environment is colab. else just "fig.show()"
    fig.show()


if __name__=='__main__':
    palette_generator(num=20, show_history=False, show_palette=True, show_3D=True, show_3D_begin=True)