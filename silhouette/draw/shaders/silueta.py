vert_shader = '''
uniform mat4 ModelViewProjectionMatrix;

/* Keep in sync with intern/opencolorio/gpu_shader_display_transform_vertex.glsl */
in vec2 texCoord;
in vec2 pos;
out vec2 texCoord_interp;

void main()
{
    gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0f, 1.0f);
    texCoord_interp = texCoord;
}
'''
frag_shader = '''
in vec2 texCoord_interp;
out vec4 fragColor;

uniform sampler2D i;
uniform float alpha;
uniform vec3 co;
uniform vec3 bco;
uniform float use_transp;

void main()
{
    fragColor = texture(i, texCoord_interp);
    
    if (use_transp == 1.0 && fragColor.r < 0.5) {
        fragColor.a = smoothstep(0.0, 1.0, fragColor.r * 2.0);
        if (fragColor.a < .5) {
            discard;
        }
    }
    
    fragColor.rgb = mix(bco, co, fragColor.r);
    fragColor.a *= alpha;
}
'''

live_frag_shader = '''
in vec2 texCoord_interp;
out vec4 fragColor;

uniform sampler2D i;
uniform float alpha;
uniform vec3 co;
uniform vec3 bco;
uniform float use_transp;

void main()
{
    fragColor = texture(i, texCoord_interp);
    
    if (use_transp == 1.0) {
        if (fragColor.a < .1) {
            discard;
        }
    }

    fragColor.rgb = mix(bco, co, fragColor.a);
    fragColor.a = alpha;
}
'''
