import gpu
from gpu_extras.batch import batch_for_shader

def vertices(x,y,w,h):
    return ((x,y),(x+w,y),(x,y+h),(x+w,y+h))

indices = (
    (0, 1, 2), (2, 1, 3))

shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

def draw_rect(p, s, co):
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices(*p,*s)}, indices=indices)
    shader.bind()
    shader.uniform_float("color", co)
    batch.draw(shader)
