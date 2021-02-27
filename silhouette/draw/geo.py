def GeoPOINT(c):return {"p": [(c.x, c.y)]}

def get_silu_verts(x, y, w, h):
    return (
        (x,     h + y),
        (x,         y),
        (x + w,     y),
        (x + w, h + y)
    )
