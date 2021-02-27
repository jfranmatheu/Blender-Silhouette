from gpu.types import GPUShader as Shader
from gpu.shader import from_builtin

from . shaders.point import *
from . shaders.silueta import *


shader_2d_image = from_builtin('2D_IMAGE')
shader_2d_color_unif = from_builtin('2D_UNIFORM_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_flat = from_builtin('2D_FLAT_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_smooth = from_builtin('2D_SMOOTH_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_3d_color_unif = from_builtin('3D_UNIFORM_COLOR') # 3D_FLAT_COLOR # 3D_SMOOTH_COLOR
#shader_2d_image_alpha = Shader(vertex_shader, frag_shader)
#shader_2d_image_alpha_2 = Shader(vertex_shader, frag_shader_2)
shader_2d_pt = Shader(POINT_VS, POINT_FS)
shader_silueta = Shader(vert_shader, frag_shader)
