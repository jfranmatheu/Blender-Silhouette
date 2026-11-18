# Desde Blender 4.x los shaders se crean con GPUShaderCreateInfo,
# asi que aqui solo va el cuerpo GLSL (sin uniforms/in/out, eso se declara en gpu_shaders.py).

vert_shader = '''
void main()
{
    gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0f, 1.0f);
    gl_Position.z = 1.0;
    texCoord_interp = texCoord;
}
'''
frag_shader = '''
void main()
{
    fragColor = texture(image, texCoord_interp);

    if (use_transp == 1.0) { // fragColor.r < 0.5
        fragColor.a = smoothstep(0.0, 1.0, fragColor.r * 2.0);
        if (fragColor.a < .5) {
            discard;
        }
        fragColor.a = fragColor.r;
        fragColor.r = 1.0;
    }

    fragColor.rgb = mix(bco, co, fragColor.r);
    fragColor.a *= alpha;
}
'''
