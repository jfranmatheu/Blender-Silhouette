POINT_VS = """
uniform mat4 ModelViewProjectionMatrix;
uniform float size;
in vec2 p;
void main()
{
 gl_Position = ModelViewProjectionMatrix * vec4(p, 0.0, 1.0);
 gl_PointSize = size;
}
"""
POINT_FS = """
uniform vec3 co;
out vec4 fragco;
void main()
{
 fragco = vec4(co, 1.0);
}
"""
