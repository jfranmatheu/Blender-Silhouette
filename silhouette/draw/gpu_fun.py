from gpu import *


def SetPoint(ps):state.program_point_size_set(True);state.point_size_set(ps)
def RstPoint():state.program_point_size_set(False);state.point_size_set(1.0)
def SetBlend():state.blend_set('ALPHA')
def RstBlend():state.blend_set('NONE')
def SetDepth():state.depth_mask_set(False);state.depth_test_set('NONE') 
def RstDepth():state.depth_mask_set(True);state.depth_test_set('LESS_EQUAL')
