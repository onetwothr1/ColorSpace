# ColorSpace

**Perceptually uniform color space made by MLP.**  
**Euclidean distance in this space will be perceptually uniform.**

Previously suggested color spaces were hand-crafted. We tried a new approach with machine learning. Here, we provide two selected example models we made as shown below. You can see them in 3D interactive way by download and open "colorspace1 3D.html" and "colorspace2 3D.html" in "color space" folder. In the following description, the second model will be mainly described. Since neural network models depend on its random initial parameters and training procedure, one can surely make a better color space.

![colorspace 3d](https://user-images.githubusercontent.com/83393021/174807890-2840555a-28ec-4d33-83ec-30436699e70f.png)
<br><br><br>
## distance
![d drawio](https://user-images.githubusercontent.com/83393021/174701615-1591a72e-10c5-4348-8db0-d5610f90e75f.png)
  
CIE2000 Delta-E, currently one of the most widely used color difference metric, is not perfect. Two color pairs above have same RGB euclidean distance and look same to human eye, but the metric's difference is very huge. In our color space, there isn't much difference in the Euclidean distances of two color pairs. 
  
<br>

## color gradient
<center><img src="https://user-images.githubusercontent.com/83393021/174808343-9a43edfa-0ac1-4e12-a7bd-cf34bc787079.png" width="800" height="320"/></center>
<center><img src="https://user-images.githubusercontent.com/83393021/174808259-bdacf258-72c0-4859-b080-7e63ff1a8606.png" width="800" height="320"/></center>
<center><img src="https://user-images.githubusercontent.com/83393021/174808265-cd011df9-708c-4695-ac8d-5352acba6388.png" width="800" height="320"/></center>
You can see more gradients in "gradient" folder of each color space.  
  
<br><br>

## cross section

![crosssection drawio (1)](https://user-images.githubusercontent.com/83393021/174812073-d3f5b894-7e88-42e2-861a-9332172ec8b4.png) 
  
<br>

## color palette generation
With our model, it is easier to generate palettes of evenly distinct colors. We used force vector algorithm from [IWantHue](https://medialab.github.io/iwanthue/) ([code](https://medialab.github.io/iwanthue/js/libs/chroma.palette-gen.js)). You can also see the result in 3D.

ex) Generate a palette of 20 colors.

![palette generation](https://user-images.githubusercontent.com/83393021/174799508-213833fb-2469-4bb1-a1c8-15f509ec946f.png)

![color palette 20](https://user-images.githubusercontent.com/83393021/174799754-4cb6921d-879d-4a53-bedb-2e91ec4659b5.png)
 
  
<br>

## data
Data is collected from https://colors-82cc6.web.app/. Data is a array-like container of (answer, color1, color2).

```
ex) [[3, (50,120,38), (85,200,5)],
     [0, (220,52,135), (200,83,121)],
      ... ]
``` 
  
<br>

## training

![probelm setting](https://user-images.githubusercontent.com/83393021/174812328-4716fef3-f298-431d-a41d-55165209125e.png)
  
The training goal is to make the Euclidean distance of the color pair in the desired color space follow the human eye response (percieved difference from 0 to 5). You can use L1 or L2 losses. 
  
<br>

## model architecture

![block architecture](https://user-images.githubusercontent.com/83393021/174702057-bee28b38-cdc6-4202-af31-c52289f1556c.png)  
**Architecure of one block.** Since MLP often transform the color space (cube shape in initial RGB space) into a line or plane, we need to reduce the dimension back to three and ensure the space keeps its three-dimensional convex form. Thus we use an unit of a block, which has the batchnormalization layer to make the X,Y,Z coordinates spread. Due to the batchnormalization, we have to use the whole batch per one epoch. In addition, to convert a RGB color to our space, you can't just pass the value to the model. You have to calculate for evey possible colors in advance at once, save the result (into csv), and search the mapping from the csv.

![overall architecture](https://user-images.githubusercontent.com/83393021/174702077-dc1d0427-297b-49c2-a48f-ca598402d1d1.png)  
**Overall architecture of a model.** The model is linked in a row with several consecutive blocks.  
  
Our models both have hidden dimension of 100, 10 blocks and use Softplus as an activation function. We tried many but Softplus works best. 
  
<br>

## code
* model.py : MLP model definition
* train.py : Train the MLP model
* colorspace_to_csv.py : After training, you choose a model, convert its colorspace into csv file. Since MLP does not have an inverse function and the model has batchnromalization layer, it is impossible to convert only one color point from one space to another. We have to calculate the mapped points for entire color range in advance and sava the result to csv file.
* utils.py : Functions for color jobs including color conversion, inversion, get distance, set new axis (lightness).
* gradient.py : Plot the color gradient.
* 3d_visualization.py: Show the color space in 3D interactive tool. After run this .py file, open a downloaded .html file.
* palette_generator.py: Randomly generates distinct color palettes in our color space. You can also see the result in 3D visualization.
* cross_section.py : Plot the cross section of color space in different axes.      
<br><br>
 **Use**  
1. Make the model and train. Train process saves the plot of the color space and the parameter at every 200 epochs in "model/{modelname}" directory.  
2. Select one model and pass the path of checkpoint to colorspace_to_csv.py. It saves the color space in a csv file.  
3. In utils.py, set right name and csv file path of the model you want to use at the top of the code. If you want to set the color space with a new lightness axis, which connects two points, black and white, use utils.set_lightness() and set its csv file path to color_space_lightness.  
4. Use the color space; get distanve between two colors, show 3D visualization, generate color palette, etc. 
  
<br>

## directory tree

```bash
├── model    # for model training step
│   ├── modelname1
│       ├──parameter/
│       ├──image/
│       ├──train history/
│   ├── modelname2
│       ...
├── color space   # for actual use after selecting a model
│   ├── colorspacename1
│       ├──cross section/
│       ├──gradient/
│       ├──colorspacename1 3D.html
│       ├──colorspacename1 interval 5.csv
│       ├──colorspacename1 interval 15.csv
│       ├──colorspacename1 lightness.csv
│       ├──colorspacename1 3D.html
│       ├──...
│   ├── colorspacename2
│       ...
└── model.py
└── train.py
└── ...
``` 
  
<br>

## Acknowledgement
2022-1 College of Liberal Studies, Seoul National University.  
Creative and Interdisciplinary Seminar: Digital Humanities (Professor Javier Cha)

Final project by Team Incógnito.  
Teammates: Boseol Mun (@healthykim), Tanya Khagay, Jinhyeong Kim
