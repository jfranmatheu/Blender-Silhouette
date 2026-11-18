# Orden pensado para TRI_STRIP (TRI_FAN ya no existe en Vulkan/Metal).
def get_silu_verts(x, y, w, h):
    return (
        (x,     h + y),
        (x,         y),
        (x + w, h + y),
        (x + w,     y)
    )

silu_uvs = ((0, 1), (0, 0), (1, 1), (1, 0))
