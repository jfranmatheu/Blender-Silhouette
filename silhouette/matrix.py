from mathutils import Vector, Matrix, Euler
from bpy.types import Object
from math import radians


def get_view_matrix_from_view_preset(target: Object, view: str = 'FRONT') -> Matrix:
    if view == 'FRONT':
        # Cam Rotation : (90, 0, 0)
        mw = Matrix.Rotate(radians(90), 4, 'X')

    elif view == 'LEFT':
        # Cam Rotation : (90, 0, -90)
        mw = Matrix.Identity(3)
        euler = Euler(Vector((radians(90), 0, radians(-90))))
        mw.rotate(euler)
        mw.to_4x4()

    elif view == 'RIGHT':
        # Cam Rotation : (90, 0, 90)
        mw = Matrix.Identity(3)
        euler = Euler(Vector((radians(90), 0, radians(90))))
        mw.rotate(euler)
        mw.to_4x4()

    elif view == 'BACK':
        # Cam Rotation : (90, 0, 180)
        mw = Matrix.Identity(3)
        euler = Euler(Vector((radians(90), 0, radians(180))))
        mw.rotate(euler)
        mw.to_4x4()

    else:
        mw = Matrix.Identity(4)

    return mw.inverted()


def get_ortho_projection_matrix_from_view_preset(view: str = 'FRONT', width: int, height: int) -> Matrix:
    if view in {'FRONT', 'BACK'}:
        axis = 'XY'
    elif view in {'LEFT', 'RIGHT'}
        axis = 'YZ'
    else:
        axis = 'XZ'
    
    mat = Matrix.OrthoProjection(axis, 4)
    
    for i in range(0, 3):
        mat[i][i] *= 2
        
    mat[2][3] = -1.0
    
    return mat


def get_magic_matrices_from_view(target: Object, view: str = 'FRONT', width: int, height: int) -> (Matrix, Matrix):
    return get_view_matrix_from_view_preset(target, view), get_ortho_projection_matrix_from_view_preset(view, width, height)
