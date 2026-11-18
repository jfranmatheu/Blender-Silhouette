from gpu import *


def SetBlend():state.blend_set('ALPHA')
def RstBlend():state.blend_set('NONE')
def SetDepth(mode='LESS_EQUAL'):state.depth_test_set(mode);state.depth_mask_set(True)
def RstDepth():state.depth_mask_set(False);state.depth_test_set('NONE')
