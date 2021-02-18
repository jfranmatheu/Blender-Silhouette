

'''
TRANSFORMATION MATRIX:

[Transform_XAxis.x, Transform_YAxis.x, Transform_ZAxis.x, Translation.x]
[Transform_XAxis.y, Transform_YAxis.y, Transform_ZAxis.y, Translation.y]
[Transform_XAxis.z, Transform_YAxis.z, Transform_ZAxis.z, Translation.z]
[0,     0,      0,      1]
_____________________

Translation Matrix:

[1, 0, 0, Translation.x]
[0, 1, 0, Translation.y]
[0, 0, 1, Translation.z]
[0, 0, 0, 1]
_____________________

Scale Matrix:
[Scale.x,     0,       0, 0]
[0,      Scale.y,       0, 0]
[0,            0, Scale.z, 0]
[0, 0, 0, 1]
_____________________

Rotation Matrix X Axis:
[1, 0, 0, 0]
[0, cos, -sin, 0]
[0, sin,  cos, 0]
[0, 0, 0, 1]
_____________________

Rotation Matrix Y Axis:
[ cos, 0, sin, 0]
[0, 1, 0, 0]
[-sin, 0, cos, 0]
[0, 0, 0, 1]
_____________________

Rotation Matrix Z Axis:
[cos, -sin, 0, 0]
[sin,  cos, 0, 0]
[0, 0, 1, 0]
[0, 0, 0, 1]
_____________________
'''

'''
PROJECTION SPACE:

The scene is now in the most friendly space possible for a projection, the View Space.
All we have to do now is to project it onto the imaginary screen of the camera.
Before flattening the image, we still have to move into another, final space,
the Projection Space. This space is a cuboid which dimensions are between -1 and 1 for every axis.
This space is very handy for clipping (anything outside the 1:-1 range is outside the camera view area)
and simplifies the flattening operation (we just need to drop the z value to get a flat image).

To go from the View Space into the Projection Space we need another matrix, the View to Projection matrix,
and the values of this matrix depend on what type of projection we want to perform.
The two most used projections are the Orthographic Projection and the Perspective Projection.

___ORTOGRAPHIC PROJECTION___
To do the Orthographic projection we have to define the size of the area that the camera can see.
This is usually defined with a width and height values for the x and y axis, and a near and far z values for the z axis (Figure 9).

Given these values we can create the transformation matrix that remaps the box area into the cuboid.
The matrix that follows is transforms vectors from View Space into Ortho Projected Space and assumes a right handed coordinates system.

[1/width, 0, 0, 0]
[0, 1/height, 0, 0]
[0, 0, -(2/(Zfar-Znear)), -((Zfar+Znear)/(Zfar-Znear))]
[0, 0, 0, 1]

But for Blender.... Left handed coordinates system would be...

___PERSPECTIVE PROJECTION___
The other projection is the perspective projection.
The idea is similar to the orthographic projection,
but this time the view area is a frustum and therefore it's a bit more tricky to remap.
Unfortunately the matrix multiplication in this case is not enough,
because after multiplying by the matrix the result is not on the same projective space
(which means that the w component is not 1 for every vertex).
To complete the transformation we will need to divide every component of the vector by the w component itself.
Current graphics APIs do the division for you,
therefore you can simply multiply all your vertices by the perspective projection matrix and send the result to the GPU.

[tan-1(FOVx/2), 0, 0, 0]
[0, tan-1(FOVy/2), 0, 0]
[0, 0, -((Zfar+Znear)/Zfar-Znear), -(2*(Znear*Zfar)/(Zfar-Znear))]
[0, 0, -1, 0]

GPU takes care of dividing by w, clipping those vertices outside the cuboid area,
flattening the image dropping the z component, re-mapping everything from the -1 to 1 range into the 0 to 1 range
and then scale it to the viewport width and height, and rasterizing the triangles to the screen
(if you are doing the rasterization on the CPU you will have to take care of these steps yourself).
We can therefore take these last steps for granted if we render via OpenGL or DirectX,
so the perspective space is the last step of our chain of transformation.


FINALLY a model can be transformed for rendering chaining:
[View To Projection]x[World To View]x[Model to World] = [ModelViewProjectionMatrix].

'''
'''
[right.x, up.x, forward.x, position.x]
[] .y
[] .z
[0, 0, 0, 1]

_________________________________

Transformations
When rendering a scene in 3D space, there are usually 3 transformations that are applied to the 3D geometry in the scene:

World Transform: 
    The world transform (or sometimes referred to as the object transform or model matrix)
    will transform a models vertices (and normals) from object space
    (this is the space that the model was created in using a 3D content creation tool like 3D Studio Max or Maya) into world space.
    World space is the position, orientation (and sometimes scale) that positions the model in the correct place in the world.

View Transform:
    The world space vertex positions (and normals) need to be transformed into a space that is relative to the view of the camera.
    This is called “view space” (sometimes referred to “camera space”) and is the transformation that will be studied in this article.
    
Projection Transform:
    Vertices that have been transformed into view space need to be transformed by the projection transformation matrix into a space called “clip space”.
    This is the final space that the graphics programmer needs to worry about. The projection transformation matrix will not be discussed in this article.

'''

'''
_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 1x1x1: (0, 0, 0) - FRONT

Camera Location :       0,   -1.6,      0
Camera Rotation :      90,      0,      0
Camera Direction:       0,      1,      0

MATRIX WORLD: <Matrix 4x4
            (1.0000,  0.0000,  0.0000,  0.0000) # 1 normalized direction.x
            (0.0000,  0.0000, -1.0000, -1.6000) # -1.6 Translation.y
            (0.0000,  1.0000,  0.0000,  0.0000)
            (0.0000,  0.0000,  0.0000,  1.0000)>

    - Direction: [right.x, up.z, -forward.y]
    - Position : [0.0, -1.6, 0.0]

CALC MATRIX CAMERA: <Matrix 4x4
            (2.0000, 0.0000,  0.0000,  0.0000)
            (0.0000, 2.0000,  0.0000,  0.0000)
            (0.0000, 0.0000, -0.0020, -1.0002)
            (0.0000, 0.0000,  0.0000,  1.0000)>
_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 1x1x1: (0, 0, 0) - LEFT

Camera Location :    -1.6,      0,      0
Camera Rotation :      90,      0,    -90
Camera Direction:       1,      0,      0

MATRIX WORLD: <Matrix 4x4
            ( 0.0000,  0.0000, -1.0000, -1.6000) # -1.6 Translation.x
            (-1.0000,  0.0000,  0.0000,  0.0000)
            ( 0.0000,  1.0000,  0.0000,  0.0000)
            ( 0.0000,  0.0000,  0.0000,  1.0000)>

    - Direction: [-right.y, up.z, -forward.x]
    - Position : [-1.6, 0.0, 0.0]

CALC MATRIX CAMERA: <Matrix 4x4
            (2.0000, 0.0000,  0.0000,  0.0000)
            (0.0000, 2.0000,  0.0000,  0.0000)
            (0.0000, 0.0000, -0.0020, -1.0002)
            (0.0000, 0.0000,  0.0000,  1.0000)>
_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 1x1x1: (0, 0, 0) - RIGHT

Camera Location :     1.6,      0,      0
Camera Rotation :      90,      0,     90
Camera Direction:      -1,      0,      0

# CAMERA SCALE 1.0:
MATRIX WORLD:
    ( 0.0000, 0.0000,  1.0000,  1.6000)
    ( 1.0000, 0.0000,  0.0000,  0.0000)
    ( 0.0000, 1.0000,  0.0000,  0.0000)
    ( 0.0000, 0.0000,  0.0000,  1.0000)

    - Direction: [right.y, up.z, forward.x]
    - Position : [-1.6, 0.0, 0.0]

CALC MATRIX CAMERA:
    (2.0000, 0.0000,  0.0000,  0.0000)
    (0.0000, 2.0000,  0.0000,  0.0000)
    (0.0000, 0.0000, -0.0020, -1.0002)
    (0.0000, 0.0000,  0.0000,  1.0000)

# CAMERA SCALE 2.0: (smaller objects/more range)
MATRIX WORLD:
    ( 0.0000, 0.0000,  1.0000,  1.6000)
    ( 2.0000, 0.0000,  0.0000,  0.0000)
    ( 0.0000, 2.0000,  0.0000,  0.0000)
    ( 0.0000, 0.0000,  0.0000,  1.0000)
CALC MATRIX CAMERA:
    (2.0000, 0.0000,  0.0000,  0.0000)
    (0.0000, 2.0000,  0.0000,  0.0000)
    (0.0000, 0.0000, -0.0020, -1.0002)
    (0.0000, 0.0000,  0.0000,  1.0000)

_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 1x1x1: (0, 0, 0) - 3/4 FRONT-RIGHT

Camera Location :  0.7778,-0.7778,      0 # 45º (grado sexagesimal) => rad(45º) = 0,7853981634
Camera Rotation :      90,      0,     45  
Camera Direction:    -0.5,    0.5,      0

MATRIX WORLD:
    (0.7071,  0.0000,  0.7071,  0.7778) # 45º (grado centesimal ) => rad(45g) = 0,706858
    (0.7071,  0.0000, -0.7071, -0.7778)
    (0.0000,  1.0000,  0.0000,  0.0000)
    (0.0000,  0.0000,  0.0000,  1.0000)

CALC MATRIX CAMERA:
    (2.0000, 0.0000,  0.0000,  0.0000)
    (0.0000, 2.0000,  0.0000,  0.0000)
    (0.0000, 0.0000, -0.0020, -1.0002)
    (0.0000, 0.0000,  0.0000,  1.0000)



# SIZES ###############################################################
_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 2x1x1: (0, 0, 0) - FRONT

MATRIX WORLD: <Matrix 4x4
            (1.0000,  0.0000,  0.0000,  0.0000)
            (0.0000,  0.0000, -1.0000, -1.6000)
            (0.0000,  1.0000,  0.0000,  0.0000)
            (0.0000,  0.0000,  0.0000,  1.0000)>
CALC MATRIX CAMERA: <Matrix 4x4
            (2.0000, 0.0000,  0.0000,  0.0000)
            (0.0000, 2.0000,  0.0000,  0.0000)
            (0.0000, 0.0000, -0.0020, -1.0002)
            (0.0000, 0.0000,  0.0000,  1.0000)>
_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 1x2x1: (0, 0, 0) - FRONT

MATRIX WORLD: <Matrix 4x4
            (1.0000,  0.0000,  0.0000,  0.0000)
            (0.0000,  0.0000, -1.0000, -2.1000)
            (0.0000,  1.0000,  0.0000,  0.0000)
            (0.0000,  0.0000,  0.0000,  1.0000)>
CALC MATRIX CAMERA: <Matrix 4x4
            (2.0000, 0.0000,  0.0000,  0.0000)
            (0.0000, 2.0000,  0.0000,  0.0000)
            (0.0000, 0.0000, -0.0020, -1.0002)
            (0.0000, 0.0000,  0.0000,  1.0000)>
_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 1x1x2: (0, 0, 0) - FRONT

MATRIX WORLD: <Matrix 4x4
            (1.0000,  0.0000,  0.0000,  0.0000)
            (0.0000,  0.0000, -1.0000, -1.6000)
            (0.0000,  1.0000,  0.0000,  0.0000)
            (0.0000,  0.0000,  0.0000,  1.0000)>
CALC MATRIX CAMERA: <Matrix 4x4
            (2.0000, 0.0000,  0.0000,  0.0000)
            (0.0000, 2.0000,  0.0000,  0.0000)
            (0.0000, 0.0000, -0.0020, -1.0002)
            (0.0000, 0.0000,  0.0000,  1.0000)>
_______________________________________________________________________

ORTHOGRAPHIC OVER A CUBE OF 2x2x2: (0, 0, 0) - FRONT

MATRIX WORLD: <Matrix 4x4
            (1.0000,  0.0000,  0.0000,  0.0000)
            (0.0000,  0.0000, -1.0000, -2.1000)
            (0.0000,  1.0000,  0.0000,  0.0000)
            (0.0000,  0.0000,  0.0000,  1.0000)>
CALC MATRIX CAMERA: <Matrix 4x4
            (2.0000, 0.0000,  0.0000,  0.0000)
            (0.0000, 2.0000,  0.0000,  0.0000)
            (0.0000, 0.0000, -0.0020, -1.0002)
            (0.0000, 0.0000,  0.0000,  1.0000)>

_______________________________________________________________________


'''

'''
bool BKE_camera_view_frame_fit_to_coords(const Depsgraph *depsgraph,
                                         const float (*cos)[3],
                                         int num_cos,
                                         Object *camera_ob,
                                         float r_co[3],
                                         float *r_scale)
{
  Scene *scene_eval = DEG_get_evaluated_scene(depsgraph);
  Object *camera_ob_eval = DEG_get_evaluated_object(depsgraph, camera_ob);
  CameraParams params;
  CameraViewFrameData data_cb;

  /* just in case */
  *r_scale = 1.0f;

  camera_frame_fit_data_init(scene_eval, camera_ob_eval, &params, &data_cb);

  /* run callback on all given coordinates */
  while (num_cos--) {
    camera_to_frame_view_cb(cos[num_cos], &data_cb);
  }

  return camera_frame_fit_calc_from_data(&params, &data_cb, r_co, r_scale);
}
'''

'''
CAMERA_VIEWFRAME_NUM_PLANES = 4

class CameraViewFrameData():
    def __init__(self):
        self.plane_tx  = Matrix.Identity(CAMERA_VIEWFRAME_NUM_PLANES) # 4x4 - float # 4 planes
        self.normal_tx = Matrix.Identity(CAMERA_VIEWFRAME_NUM_PLANES) # 4x3 - float #
        self.dist_vals_sq = Vector.Fill(CAMERA_VIEWFRAME_NUM_PLANES)  # float # distance squared (signed)
        self.tot = 0 # int

        # Ortho camera only.
        self.is_ortho = True # bool
        self.camera_no = Vector.Fill(3) # float
        self.dist_to_cam = 0.0 # float

        # Not used by callbacks...
        self.camera_rotmat = Matrix.Identity(3) # 3x3 - float


def camera_frame_fit_calc_from_data(data, r_scale):
    pass

def camera_to_frame_view(co: Vector, data):
    pass

def camera_view_frame_fit_to_coords(*coords):
    # Get depsgraph evaluated.
    Scene *scene_eval = DEG_get_evaluated_scene(depsgraph)
    Object *camera_ob_eval = DEG_get_evaluated_object(depsgraph, camera_ob)
    
    # Initialization.
    data = CameraViewFrameData()
    
    r_scale = 1.0

    camera_frame_fit_data_init(scene_eval, camera_ob_eval, &params, &data_cb)
    
    # Run callback on all given coordinates.
    for co in coords:
        camera_to_frame_view(co, data)
    
    return camera_frame_fit_calc_from_data(&params, &data_cb, r_co, r_scale)
'''
'''
mat = Matrix.OrthoProjection('XZ', 4)
>>> mat
Matrix(((1.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0)))
'''
'''
* FRONT
MATRIX WORLD: <Matrix 4x4
            (1.0000,  0.0000,  0.0000,  0.0000) # 1 normalized direction.x
            (0.0000,  0.0000, -1.0000, -1.6000) # -1.6 Translation.y
            (0.0000,  1.0000,  0.0000,  0.0000)
            (0.0000,  0.0000,  0.0000,  1.0000)>
* LEFT
MATRIX WORLD: <Matrix 4x4
            ( 0.0000,  0.0000, -1.0000, -1.6000) # -1.6 Translation.x
            (-1.0000,  0.0000,  0.0000,  0.0000)
            ( 0.0000,  1.0000,  0.0000,  0.0000)
            ( 0.0000,  0.0000,  0.0000,  1.0000)>

    - Direction: [-right.y, up.z, -forward.x]
    - Position : [-1.6, 0.0, 0.0]
* RIGHT
MATRIX WORLD:
    ( 0.0000, 0.0000,  1.0000,  1.6000)
    ( 1.0000, 0.0000,  0.0000,  0.0000)
    ( 0.0000, 1.0000,  0.0000,  0.0000)
    ( 0.0000, 0.0000,  0.0000,  1.0000)
'''
