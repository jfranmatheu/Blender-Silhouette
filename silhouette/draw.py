import bgl
from bgl import (
    glEnable, glDisable, GL_BLEND, GL_DEPTH_TEST,
    glBlendFunc, GL_SRC_COLOR, GL_ONE_MINUS_CONSTANT_ALPHA,
    glActiveTexture, glBindTexture, GL_TEXTURE0, GL_TEXTURE_2D
)
from gpu_extras.batch import batch_for_shader


def get_verts(x, y, w, h):
    return (
        (x,     h + y),
        (x,         y),
        (x + w,     y),
        (x + w, h + y)
    )

def draw_silhouette(
     p: 'Vector',
     s: 'Vector',
     i: int,
     co: 'Color',
     bgco: 'Color',
     alpha: float = 1.0,
     use_transparent_bg: bool = False,
     use_depth: bool = False):
    if not use_depth:
        glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    bat = batch_for_shader(shader, 'TRI_FAN', { "pos" : vertices, "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) },)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, image)
    shader.bind()
    shader.uniform_float("alpha", alpha)
    shader.uniform_float("col", co)
    shader.uniform_float("bgcol", bgco)
    bat.draw(shader)
    glDisable(GL_BLEND)
