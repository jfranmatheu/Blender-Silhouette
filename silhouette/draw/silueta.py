from bgl import *
from gpu_extras.batch import batch_for_shader

from . gpu_shaders import shader_silueta, shader_live_silueta
from . geo import get_silu_verts
from . gpu_fun import SetDepth, RstDepth


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

def Draw_Live_Silueta(i, x, y, w, h, style, shader = shader_live_silueta):
    if style.dirty:
        shader.bind()
        shader.uniform_float("use_transp", 1.0 if style.use_transparency else 0.0)
        shader.uniform_float("alpha", style.opacity)
        shader.uniform_float("co", style.color)
        shader.uniform_float("bco", style.bg_color)
        style.dirty = False

    bat = batch_for_shader(shader, 'TRI_FAN', { "pos" : get_silu_verts(x,y,w,h), "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) },)

    if not style.show_in_front:
        #glEnable(GL_DEPTH_TEST)
        SetDepth()
    glEnable(GL_BLEND)

    #glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, i)
    bat.draw(shader)

    if not style.show_in_front:
        #glDisable(GL_DEPTH_TEST)
        RstDepth()
    glDisable(GL_BLEND)
