from PIL import Image
import cv2
from datetime import datetime 
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from IPython.display import display
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class Art:
    
    def __init__(self):
        self.palette =  {
                'sky blue': (113, 213, 248),
                'ultramarine': (60, 124, 246),
                'medium blue': (15, 72, 175),
                'dark blue': (25, 42, 114),
                'violet': (33, 19, 70),
                'teal': (14, 67, 73),
                'green': (15, 66, 35),
                'leaf green': (88, 135, 31),
                'light green': (154, 193, 45),
                'yellow': (255, 252, 35),
                'orange': (230, 156, 23),
                'dark orange': (235, 105, 21),
                'vermillion': (216, 68, 14),
                'red': (205, 19, 14),
                'fuchsia': (157, 52, 105),
                'purple': (107, 32, 86),
                'dark purple': (84, 20, 57),
                'dark grey': (110, 110, 110),
                'light grey': (220, 220, 220),
                'pale grey': (240, 240, 240)
                }
        self.channels = ['red', 'green', 'blue']
        self.cmaps = {'red': 'Reds',
                    'green': 'Greens',
                    'blue': 'Blues'
                    }
        self.color_list = np.array([tuple(x) for x in self.palette.values()], dtype=np.uint8)
        self.data_path = os.getcwd() + "\\data\\"
        self.image_path = os.getcwd() + "\\images\\"

    def set_cmaps(self, cmap):
        self.cmaps = cmap
    
    def set_data_path(self, data_path):
        self.data_path = data_path
        print("data_path set to {}".format(data_path))

    def set_image_path(self, image_path):
        self.image_path = image_path
        print("image_path set to {}".format(image_path))
    
    def set_channels(self, color_channels):
        self.channels = color_channels
    
    def set_palette(self, palette):
        self.palette = palette
        self.color_list = np.array([tuple(x) for x in palette.values()], dtype=np.uint8)
            
    def get_dims(self, img):
        """   
        Parameters:
        img (np.ndarray): array representation of an image
        
        Returns: tuple of dimensions (height, width)
        """
        return img.shape[0:2]
    
    def resize(self, img, new_dims):
        try:
            resized_img = cv2.resize(img, new_dims)
            return resized_img
        except:
            raise ValueError("Could not resize image!")

    def show_image(self, img):
      plt.imshow(img)

    def get_color_channel(self, img, color):
        channels = self.channels

        if color not in channels:
            raise ValueError("'{}' not a valid color".format(color))

        elif color == 'red':
            return img[:, :, 0]

        elif color == 'green':
            return img[:, :, 0]

        elif color == 'blue':
            return img[:,:,2]
    
    def show_channel(self, img, channel):
        channels = self.channels

        if channel not in channels:
            raise ValueError("'{}' not a valid color".format(channel))

        cmaps = self.cmaps
        color = cmaps[channel]

        img = self.get_color_channel(img, channel)
        plt.imshow(img, cmap=color)
    
    def show_rgb_channels(self, img):
        img = img.astype('uint8')
        
        fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1)
        fig.set_figheight(15)
        fig.set_figwidth(15)
        
        ax1.imshow(self.get_color_channel(img, 'red'), cmap='Reds')
        ax1.set_axis_off()
        
        ax2.imshow(self.get_color_channel(img, 'green'), cmap='Greens')
        ax2.set_axis_off()
        
        ax3.imshow(self.get_color_channel(img, 'blue'), cmap='Blues')
        ax3.set_axis_off()
        
        fig.set_axis_off()
        plt.show()

    def get_dominant_color(self, pil_img, palette_size=20, comp_time=False):
        # https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
        start = datetime.now()
        img = pil_img.copy()
         # Reduce colors (uses k-means internally)
        img.thumbnail((100, 100))
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)
        # Find the color that occurs most often
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        palette_index = color_counts[0][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]

        if comp_time == True:
            print("Elapsed time:{}".format(datetime.now() - start))

        return dominant_color

    def color_distance(self, color_1, color_2):
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
    
    def display_color(self, color_list, **params):
        """
        plt
        Parameters:
        color_list (tuple): tuple of ints for r,g,b values
        shape (tuple): optional parameter to reshape output
        """

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

    def palette_distance(self, input_color):
        palette = self.palette
        # 444 from pythagorean
        dists = 444 * np.ones(len(palette))
        
        for count, color in enumerate(palette.items()):
            dists[count] = self.color_distance(input_color, color[1])
        return dists
    
    def closest_on_palette(self, input_color):
        palette = self.palette
        dists = self.palette_distance(input_color)
        min_index = np.argmin(dists)
        return list(palette.keys())[min_index]
        
    def make_color_list(self, save=False, filename='all_colors.txt'):
        # makes a list of tuples for quicker compute
        all_colors = -1 * np.ones((256**3), dtype=object)
        pos = 0
        
        for i in range(0, 256):
            for j in range(0,256):
                for k in range(0, 256):  
                    all_colors[pos] = (i, j, k)
                    pos += 1

        if save == True:
            with open(self.data_path + filename, 'w') as outfile:
                outfile.write(str(all_colors))

        return all_colors 
    
    def make_color_map(self, filename='', save=False):
        color_list = self.color_list
        path = self.data_path

        closest_color = {}
        start = datetime.now()
        for counter, color in enumerate(color_list):
            if counter % 10e3 == 0:
                print("{}: {} elapsed".format(counter, datetime.now() - start))
                
            closest_color[color] = self.closest_on_palette(color)
        
        if save == True and filename != '':
            with open(path + filename, 'w') as outfile:
                outfile.write(str(closest_color))
                print("Saved {} to {}".format(filename, path))

        return closest_color
    