from bgl import *
from gpu_extras.batch import batch_for_shader

from . gpu_shaders import shader_silueta, shader_live_silueta
from . geo import get_silu_verts


def Draw_Silueta(i, x, y, w, h, style):
    bat = batch_for_shader(shader_silueta, 'TRI_FAN', { "pos" : get_silu_verts(x,y,w,h), "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) },)

    if not style.show_in_front:
        glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)

    #glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, i)
    bat.draw(shader_silueta)

    if not style.show_in_front:
        glDisable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)

def Draw_Live_Silueta(i, x, y, w, h, style):
    bat = batch_for_shader(shader_live_silueta, 'TRI_FAN', { "pos" : get_silu_verts(x,y,w,h), "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) },)

    if not style.show_in_front:
        glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)

    #glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, i)
    bat.draw(shader_live_silueta)

    if not style.show_in_front:
        glDisable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)
