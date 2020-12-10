from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

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