from enum import Enum
from math import inf, radians

from bpy.types import Object
from mathutils import Euler, Matrix, Vector


class BOUNDBOX_IDX(Enum):
    ''' Front options. '''
    FRONT_4 = (0, 1, 4, 5)
    FRONT_2 = (0, 5)
    FRONT_1 = (0,)
    FRONT__BOTLEFT  = 0
    FRONT__TOPLEFT  = 1
    FRONT__BOTRIGHT = 4
    FRONT__TOPRIGHT = 5

    ''' Back options. '''  # NOTE. Y axis is inverted... rotate 180º if wished
    BACK_4 = (7, 6, 3, 2)
    BACK_2 = (7, 2)
    BACK_1 = (7,)
    BACK__BOTLEFT  = 7
    BACK__TOPLEFT  = 6
    BACK__BOTRIGHT = 3
    BACK__TOPRIGHT = 2

    ''' Right options. '''
    RIGHT_4 = (4, 5, 7, 6)
    RIGHT_2 = (4, 6)
    RIGHT_1 = (4,)
    RIGHT__BOTLEFT  = 4
    RIGHT__TOPLEFT  = 5
    RIGHT__BOTRIGHT = 7
    RIGHT__TOPRIGHT = 6

    ''' Left options. ''' # NOTE. Y axis is inverted... rotate 180º if wished
    LEFT_4 = (3, 2, 0, 1)
    LEFT_2 = (3, 1)
    LEFT_1 = (3,)
    LEFT__BOTLEFT  = 3
    LEFT__TOPLEFT  = 2
    LEFT__BOTRIGHT = 0
    LEFT__TOPRIGHT = 1

    ''' Top options. '''
    TOP_4 = (1, 2, 5, 6)
    TOP_2 = (1, 6)
    TOP_1 = (1,)
    TOP__BOTLEFT  = 1
    TOP__TOPLEFT  = 2
    TOP__BOTRIGHT = 5
    TOP__TOPRIGHT = 6

    ''' Bottom options. ''' # NOTE. Y axis is inverted... rotate 180º if wished (for "correct" visual depth dir in Y axis)
    BOTTOM_4 = (3, 0, 7, 4)
    BOTTOM_2 = (3, 4)
    BOTTOM_1 = (3,)
    BOTTOM__BOTLEFT  = 3 # This should be 4.
    BOTTOM__TOPLEFT  = 0 # This should be 7.
    BOTTOM__BOTRIGHT = 7 # This should be 0.
    BOTTOM__TOPRIGHT = 4 # This should be 3.

    def __call__(self): return self.value


class BOUNDBOX_NORM(Enum):
    BOTTOM= ( 0,  0,  1)
    TOP   = ( 0,  0, -1)
    BACK  = ( 0,  1,  0)
    FRONT = ( 0, -1,  0)
    LEFT  = ( 1,  0,  0)
    RIGHT = (-1,  0,  0)
    
    def __call__(self): return self.value
    

class BOUNDBOX_PAIRPTS_DIR(Enum):
    BACK   = ((  1,      1,     -1 ), ( -1,      1,      1 ))
    FRONT  = (( -1,     -1,     -1 ), (  1,     -1,      1 ))
    LEFT   = (( -1,      1,     -1 ), ( -1,     -1,      1 ))
    RIGHT  = ((  1,     -1,     -1 ), (  1,      1,      1 ))
    BOTTOM = (( -1,      1,     -1 ), (  1,     -1,     -1 ))
    TOP    = (( -1,     -1,     -1 ), (  1,      1,      1 ))
    
    FRONT__BOTLEFT  = (-1, -1, -1)
    FRONT__TOPLEFT  = (-1, -1,  1)
    FRONT__BOTRIGHT = ( 1, -1, -1)
    FRONT__TOPRIGHT = ( 1, -1,  1)
    
    ''' SQUEME
    0 : ( -1,     -1,     -1 )
    1 : ( -1,     -1,      1 )
    2 : ( -1,      1,      1 )
    3 : ( -1,      1,     -1 )
    4 : (  1,     -1,     -1 )
    5 : (  1,     -1,      1 )
    6 : (  1,      1,      1 )
    7 : (  1,      1,     -1 )
    '''
    
    def __call__(self): return self.value


def get_bbox_points_from_view(target: Object, view: str = 'FRONT', num: int = 2) -> set:
    bbox = target.bound_box
    return [tuple(bbox[idx]) for idx in getattr(BOUNDBOX_IDX, view+('_%i'%num), BOUNDBOX_IDX.FRONT_1)()]


def get_rot_matrix_from_view_preset(view: str = 'FRONT') -> Matrix:
    if view == 'FRONT':
        mat_rot = Matrix.Rotation(radians(-90), 4, 'X')
    elif view == 'BOTTOM':
        mat_rot = Matrix.Rotation(radians(180), 4, 'X')
    elif view == 'TOP':
        mat_rot = Matrix.Identity(4)
    else:
        if view == 'LEFT':
            #mat_rot = Matrix.Rotation(radians(90), 4, 'X') @ Matrix.Rotation(radians(-90), 4, 'Z') # WRONG! Use .rotate instead!
            euler = Euler(Vector((radians(180), radians(90), radians(-90))))
        elif view == 'RIGHT':
            #mat_rot = Matrix.Rotation(radians(90), 4, 'X') @ Matrix.Rotation(radians(90), 4, 'Z') # WRONG! Use .rotate instead!
            euler = Euler(Vector((radians(180), radians(-90), radians(90))))
        elif view == 'BACK':
            #mat_rot = Matrix.Rotation(radians(90), 4, 'X') @ Matrix.Rotation(radians(180), 4, 'Y') # WRONG! Use .rotate instead!
            euler = Euler(Vector((radians(90), 0, radians(180))))

        mat_rot = Matrix.Identity(3)
        mat_rot.rotate(euler)
        mat_rot.resize_4x4()
    
    return mat_rot


def get_view_matrix_from_view_preset(target: Object, view: str = 'FRONT') -> Matrix:
    A, B = get_bbox_points_from_view(target, view, 2)
    v_trans = -1*(Matrix.Translation((Vector(A)+Vector(B))/2)@target.matrix_world).to_translation()

    # NOTE: HACK: To fix depth bug if scale is different.
    for i, axis in enumerate(getattr(BOUNDBOX_NORM, view, BOUNDBOX_NORM.FRONT)()):
        if axis != 0:
            v_trans[i] *= target.scale[i]

    return get_rot_matrix_from_view_preset(view) @ Matrix.Translation(v_trans)


def get_multi_view_matrix_from_view_preset(targets, view: str = 'FRONT') -> Matrix:
    axis_idx = 0
    # NOTE: HACK: To fix depth bug if scale is different.
    for i, axis in enumerate(getattr(BOUNDBOX_NORM, view, BOUNDBOX_NORM.FRONT)()):
        if axis != 0:
            axis_idx = i # v_trans[i] *= target.scale[i]

    dir_A, dir_B = getattr(BOUNDBOX_PAIRPTS_DIR, view, BOUNDBOX_PAIRPTS_DIR.FRONT)()
    A = Vector((inf, inf, inf)) if dir_A[axis_idx] <= 0 else Vector((-inf, -inf, -inf))
    B = Vector((inf, inf, inf)) if dir_B[axis_idx] <= 0 else Vector((-inf, -inf, -inf)) # TODO: Should not be inverted??

    # To calc max dimensions in opposite to depth dir axis.
    depth_dir = getattr(BOUNDBOX_NORM, view, BOUNDBOX_NORM.FRONT)() # BOUNDBOX_PLANE.FRONT (XZ)
    dim_axis = (idx for idx, x in enumerate(depth_dir) if x == 0)
    dim_plane = Vector((0, 0))

    A = Vector((0, 0, 0))
    B = Vector((0, 0, 0))
    #v_trans = Vector((0, 0, 0))

    #mid_points = []
    A_points = []
    B_points = []

    axis_scale = 1.0
    for target in targets:
        axis_scale = max(axis_scale, target.scale[axis_idx])

        # NOTE: check each point with prev target, take the greater value if is 1, lower otherwise.
        pts = get_bbox_points_from_view(target, view, 2)

        a = (Matrix.Translation(Vector(pts[0]))@target.matrix_world).to_translation()
        b = (Matrix.Translation(Vector(pts[1]))@target.matrix_world).to_translation()

        for i, x in enumerate(a):
            #if abs(x) > abs(A[i]):
            #    A[i] = x
            if dir_A[i] >= 0:
                A[i] = max(A[i], x)
            else:
                A[i] = min(A[i], x)

        for j, y in enumerate(b):
            if dir_B[j] >= 0:
                B[j] = max(B[j], y)
            else:
                B[j] = min(B[j], y)
        
        #print("\n")
        #print(target.name)
        #print("A:", A, "  \ta:", a)
        #print("B:", B, "  \tb:", b)


    for i, j in enumerate(dim_axis):
        dim_plane[i] = max(abs(B[j] - A[j]), 0.00001)

    v_trans = (A+B)/2
    v_trans *= -1
    v_trans[axis_idx] *= axis_scale

    #print("TRANSLATION:", v_trans*-1)
    #print("PLANE DIMENSIONS:", dim_plane)

    return get_rot_matrix_from_view_preset(view) @ Matrix.Translation(v_trans), dim_plane


def get_ortho_projection_matrix_from_view_preset(target: Object, view: str = 'FRONT', width: int = 256, height: int = 256) -> Matrix:
    dims = target.dimensions
    depth_dir = getattr(BOUNDBOX_NORM, view, BOUNDBOX_NORM.FRONT)() # BOUNDBOX_PLANE.FRONT (XZ)
    dim_plane = Vector((dims[idx] for idx, x in enumerate(depth_dir) if x == 0))

    mat = Matrix.Identity(4) # Matrix.OrthoProjection(axis, 4)

    # HACK.
    frame_scale_factor = min(width, height) * 0.00667 / 256
    scale_factor = min(1/dim_plane.x, 1/dim_plane.y) * 0.00667 # Magic value.
    # border_threshold = 0.0035 # 0.004 for full.
    mat[0][0] = width  * scale_factor # width  * border_threshold # 1 / width
    mat[1][1] = height * scale_factor # height * border_threshold # 1 / height

    Zfar = 1000.0
    Znear = 0.01
    # HACK. Positive will show geometry as black silhouette.
    mat[2][2] = -( 2 / (Zfar - Znear) )          # -0.002
    mat[2][3] = -( (Zfar+Znear) / (Zfar-Znear) ) # -1.0002

    return mat


def get_multi_ortho_projection_matrix_from_view_preset(targets, view: str = 'FRONT', dim_plane: Vector = Vector((1, 1)), width: int = 256, height: int = 256) -> Matrix:
    '''
    dims = Vector((0, 0, 0))
    for target in targets:
        for i in range(0, 3):
            dims[i] = max(dims[i], target.dimensions[i])
        print("\n")
        print(target.name)
        print("TARGET DIMS:", target.dimensions)
        print("DIMS:", dims)
    '''

    #depth_dir = getattr(BOUNDBOX_NORM, view, BOUNDBOX_NORM.FRONT)() # BOUNDBOX_PLANE.FRONT (XZ)
    #dim_plane = Vector((dims[idx] for idx, x in enumerate(depth_dir) if x == 0))

    mat = Matrix.Identity(4) # Matrix.OrthoProjection(axis, 4)

    # HACK.
    frame_scale_factor = min(width, height) * 0.00667 / 256
    scale_factor = min(1/dim_plane.x, 1/dim_plane.y) * 0.00667 # Magic value.
    # border_threshold = 0.0035 # 0.004 for full.
    mat[0][0] = width  * scale_factor # width  * border_threshold # 1 / width
    mat[1][1] = height * scale_factor # height * border_threshold # 1 / height

    Zfar = 1000.0
    Znear = 0.01
    # HACK. Positive will show geometry as black silhouette.
    mat[2][2] = -( 2 / (Zfar - Znear) )          # -0.002
    mat[2][3] = -( (Zfar+Znear) / (Zfar-Znear) ) # -1.0002

    return mat


def get_magic_matrices_from_view_and_fixed_dimensions(target: Object, multi_object: bool, view: str = 'FRONT', width: int = 256, height: int = 256) -> (Matrix, Matrix):
    if not multi_object:
        return get_view_matrix_from_view_preset(target, view), get_ortho_projection_matrix_from_view_preset(target, view, width, height)
    else:
        view_matrix, dims = get_multi_view_matrix_from_view_preset(target, view)
        return view_matrix, get_multi_ortho_projection_matrix_from_view_preset(target, view, dims, width, height)
