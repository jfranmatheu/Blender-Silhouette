from gpu_extras.presets import draw_texture_2d

def Draw_Texture(image, off_x, off_y, _width, _height):
    draw_texture_2d(image, (off_x, off_y), _width, _height)
