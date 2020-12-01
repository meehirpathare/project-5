from matplotlib import pyplot as plt 
from PIL import Image
import cv2
from datetime import datetime 


from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

def get_dims(img, rgb = False):
    """   
    Parameters:
    img (np.ndarray): array representation of an image
    
    Returns: tuple of dimensions (height, width)
    """
    return img.shape[0:2]

def resize(img, width, height):
    """
    Parameters:
    img (np.ndarray): array representation of an image
    width (int): px width of resized image
    height (int): px height of resized image 

    Returns: ndarray representation of resized image
    """
    resized_img = cv2.resize(img, (width, height))
    return resized_img

def show_image(img):
    plt.imshow(img)

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
    
def show_channel(img, channel):
    channels = ['red', 'green', 'blue']

    if channel not in channels:
        raise ValueError("'{}' not a valid color".format(channel))

    cmaps = {'red': 'Reds',
        'green': 'Greens',
        'blue': 'Blues'}
    color = cmaps[channel]

    img = get_channel(img, channel)
    plt.imshow(img, cmap=color)

    return img

def show_all_channels(img):
    img = img.astype('uint8')
    
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1)
    fig.set_figheight(15)
    fig.set_figwidth(15)
    
    ax1.imshow(get_channel(img, 'red'), cmap='Reds')
    ax1.set_axis_off()
    
    ax2.imshow(get_channel(img, 'green'), cmap='Greens')
    ax2.set_axis_off()
    
    ax3.imshow(get_channel(img, 'blue'), cmap='Blues')
    ax3.set_axis_off()
    
    fig.set_axis_off()
    plt.show()

def get_dominant_color(pil_img, palette_size=20, comp_time=False):
    start = datetime.now()
    # Resize image to speed up processing
    img = pil_img.copy()
 
    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    if comp_time == True:
        print("Elapsed time:{}".format(datetime.now() - start))
    return dominant_color

def closest_on_palette(input_color, palette):
    dists = []
    for color in palette.values():
        val = color_distance(input_color, color)
        dists.append(val)
        

    d = dists.index(min(dists)) 
    closest_color = list(palette.keys())[d]
    return closest_color

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