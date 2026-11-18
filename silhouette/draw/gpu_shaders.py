import bpy
from gpu.types import GPUShaderCreateInfo, GPUStageInterfaceInfo
from gpu.shader import from_builtin, create_from_info

from . shaders.silueta import *


def _create_silueta_shader(frag_source):
    iface = GPUStageInterfaceInfo("silhouette_iface")
    iface.smooth('VEC2', "texCoord_interp")

    info = GPUShaderCreateInfo()
    info.push_constant('MAT4', "ModelViewProjectionMatrix")
    info.push_constant('FLOAT', "alpha")
    info.push_constant('FLOAT', "use_transp")
    info.push_constant('VEC3', "co")
    info.push_constant('VEC3', "bco")
    info.sampler(0, 'FLOAT_2D', "image")
    info.vertex_in(0, 'VEC2', "pos")
    info.vertex_in(1, 'VEC2', "texCoord")
    info.vertex_out(iface)
    info.fragment_out(0, 'VEC4', "fragColor")
    info.vertex_source(vert_shader)
    info.fragment_source(frag_source)
    return create_from_info(info)


# En modo background no hay contexto GPU, asi que no creamos nada.
if bpy.app.background:
    shader_2d_image = shader_2d_color_unif = shader_silueta = None
else:
    shader_2d_image = from_builtin('IMAGE')
    shader_2d_color_unif = from_builtin('UNIFORM_COLOR')
    shader_silueta = _create_silueta_shader(frag_shader)
