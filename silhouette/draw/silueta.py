from gpu_extras.batch import batch_for_shader

from . gpu_shaders import shader_silueta
from . geo import get_silu_verts, silu_uvs
from . gpu_fun import SetDepth, RstDepth, SetBlend, RstBlend


def update_silueta_uniforms(shader, style):
    shader.bind()
    shader.uniform_float("use_transp", 0.0 if style.show_background else 1.0)
    shader.uniform_float("alpha", style.opacity)
    shader.uniform_float("co", style.color)
    shader.uniform_float("bco", style.bg_color)


def Draw_Silueta(texture, x, y, w, h, style, shader = shader_silueta):
    bat = batch_for_shader(shader, 'TRI_STRIP', { "pos" : get_silu_verts(x,y,w,h), "texCoord": silu_uvs },)

    if not style.show_in_front:
        SetDepth()
    SetBlend()

    update_silueta_uniforms(shader, style)
    shader.uniform_sampler("image", texture)
    bat.draw(shader)

    if not style.show_in_front:
        RstDepth()
    RstBlend()
