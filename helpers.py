from matplotlib import pyplot as plt 
from PIL import Image
import cv2
from datetime import datetime 
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import os
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

def display_color(color_list, return_vals=False,**params):
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
    
    if return_vals == True:
        return palette[indices]

def palette_distance(input_color, palette):
    dists = 444 * np.ones(len(palette))
    
    for count, color in enumerate(palette.items()):
        dists[count] = color_distance(input_color, color[1])
    return dists

def closest_on_palette(input_color, palette):
    dists = palette_distance(input_color, palette)
    min_index = np.argmin(dists)
    return list(palette.keys())[min_index]

def make_color_list(filepath):
    all_colors = -1 * np.ones((256**3), dtype=object)
    pos = 0
    
    for i in range(0, 256):
        for j in range(0,256):
            for k in range(0, 256):  
                all_colors[pos] = (i, j, k)
                pos += 1
    return all_colors 

def make_color_map(color_list, palette, filename, return_vals=True):
    closest_color = {}
    
    start = datetime.now()
    for counter, color in enumerate(color_list):
        if counter % 10e4 == 0:
            print("{}: {} elapsed".format(counter, datetime.now() - start))
            with open(filename, 'w') as outfile:
                outfile.write(str(closest_color))
            
        closest_color[color] = closest_on_palette(color, palette)
    
    if return_vals == True:
        return closest_color
   
def get_channel(img, color):
    #working in rgb
    channels = ['red', 'green', 'blue']

    if color not in channels:
        raise ValueError("'{}' not a valid color".format(color))

    elif color == 'red':
        return img[:, :, 0]

    elif color == 'green':
        return img[:, :, 0]

    elif color == 'blue':
        return img[:,:,2]

def get_dominant_color(img_file, palette_size=20, comp_time=False):
    pil_img = Image.open(img_file)

    start = datetime.now()
    # Resize image to speed up processing
    img = pil_img.copy()
 
    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = np.array(palette[palette_index*3:palette_index*3+3]).reshape(1, 1, 3)
   
    if comp_time == True:
        print("Elapsed time:{}".format(datetime.now() - start))

    return dominant_color