

def point_inside_rect(px, py, x, y, w, h):
    return x < px < x + w and y < py < y + h

def swap(value_1, value_2):
    temp = value_1
    value_1 = value_2
    value_2 = temp
    return value_1, value_2
