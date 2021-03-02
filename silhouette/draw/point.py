from gpu_extras.batch import batch_for_shader as bat

from . gpu_shaders import shader_2d_pt
from . gl_fun import SetPoint, RstPoint
from . geo import GeoPOINT


def dimm_point(_c,_r,_co,s=shader_2d_pt):SetPoint(_r*2);b=bat(s,'POINTS',GeoPOINT(_c));s.bind();s.uniform_float('co',_co);b.draw(s);RstPoint()
