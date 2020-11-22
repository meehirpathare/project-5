class Art:
    
    def __init__(self, img):
        self.img = img
        self.palette = color_dict = {
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
        self.dims = get_dims(self.img)

    
    def get_dims(self, rgb = False):
        if rgb == True:
            return img.shape
        else:
            return img.shape[0:2]
    
    def resize(img, width, height):
        self.img = cv2.resize(img, (width, height))
        self.dims = resized_img
        
    