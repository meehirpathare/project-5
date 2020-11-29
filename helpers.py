from matplotlib import pyplot as plt 
from PIL import Image
import cv2
from datetime import datetime 
import numpy as np
from skimage import io
import matplotlib.pyplot as plt

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

def get_dims(img):
    """   
    Parameters:
    img (np.ndarray): array representation of an image
    
    Returns: tuple of dimensions (height, width)
    """
    return img.shape[0:2]

def color_distance(color_1, color_2):
    r1, g1, b1 = color_1[0], color_1[1], color_1[2]
    color1_rgb = sRGBColor(r1, g1, b1)

    r2, g2, b2 = color_2[0], color_2[1], color_2[2]
    color2_rgb = sRGBColor(r2, g2, b2)

    # Convert from RGB to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)

    # Convert from RGB to Lab Color Space
    color2_lab = convert_color(color2_rgb, LabColor)

    # Find the color difference
    delta_e = delta_e_cie2000(color1_lab, color2_lab)

    return delta_e

def closest_on_palette(input_color, palette):
    dists = []
    for color in palette.values():
        val = color_distance(input_color, color)
        dists.append(val)
        

    d = dists.index(min(dists)) 
    closest_color = list(palette.keys())[d]
    return closest_color
import math

def display_color(color_list,**params):
    """
    Parameters:
    color_list (tuple): tuple of ints for r,g,b values
    shape (tuple): optional parameter to reshape output
    """
    # default value unless new value declared
    attrs = dir(plt)
    
    if 'shape' in params.keys() and params['shape'][0] * params['shape'][1] == len(color_list): 
        shape = params['shape']
        params.pop('shape')
        
    else:
        shape = (1, len(color_list))
        
    args = params.copy()
    
    for key in params.keys():
        if key not in attrs:
            args.pop(key)
    
    palette = np.array(color_list, dtype=np.uint8)
    indices = np.array(list(range(0, len(palette)))).reshape(shape)
    
    plt.figure(**args)
    io.imshow(palette[indices])
    plt.axis('off')