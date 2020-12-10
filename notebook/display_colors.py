import numpy as np
from skimage import io
import matplotlib.pyplot as plt

def display_color(color_list, **kwargs):
    palette = np.array(vals, dtype=np.uint8)
    indices = np.array(list(range(0, len(palette)))).reshape(1, len(palette))

    
    io.imshow(palette[indices])
    plt.axis('off'); 