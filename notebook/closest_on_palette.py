
def closest_on_palette(input_color, palette):
    dists = []
    for color in palette.values():
        val = color_distance(input_color, color)
        dists.append(val)

    d = dists.index(min(dists)) 
    closest_color = list(color_dict.keys())[d]
    return closest_color