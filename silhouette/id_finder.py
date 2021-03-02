from mathutils import Vector
import bpy

from . draw.gl_fun import SetPoint, RstPoint, GetPixel
from . draw.point import dimm_point

from . draw.image import Draw_Texture
from . draw.text import Draw_Text


class IDFinder():
    id_data = {
        'id' : 0,
        'to_check' : True,
        'matched' : False,
        'match' : False,
        'last_matched_id' : -1,
        'cube' : None,
        'chroma_color' : [0.0, 1.0, 0.2]
    }
    shading = {
        'type' : 'SOLID',
        'light' : 'FLAT',
        'color_type' : 'SINGLE',
        'single_color' : [1, 1, 1],
        'background_type' : 'VIEWPORT',
        'background_color' : [0, 0, 0]
    }
    
    @classmethod
    def reset(cls):
        cls.id_data['last_matched_id'] = cls.id_data['id']
        cls.id_data['id'] = 0
        cls.id_data['to_check'] = True
        cls.id_data['match'] = False
        cls.id_data['matched'] = False
    
    @classmethod
    def resume(cls):
        pass
     
    @classmethod
    def get_next_id(cls):
        cls.id_data['id'] += 1
        return cls.id_data['id']
    
    @classmethod
    def setup_temp_cube(cls, ctx):
        
        '''
        print(0)
        bpy.ops.mesh.primitive_cube_add(ctx_made, size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        #ctx.active_object.name = "TemporalSyncCube"
        print(1)
        bpy.ops.view3d.localview(ctx_made)
        print(2)
        '''
        shading   = ctx.space_data.shading

        # BACKUP DATA.
        cls.shading['type']                = shading.type
        cls.shading['light']               = shading.light
        cls.shading['color_type']          = shading.color_type
        cls.shading['single_color']        = shading.single_color
        cls.shading['background_type']     = shading.background_type
        cls.shading['background_color']    = shading.background_color

        # UPDATE DATA TEMPORALY.
        shading.type                = 'SOLID'
        shading.light               = 'FLAT'
        shading.color_type          = 'SINGLE'
        shading.single_color        = cls.id_data['chroma_color']
        shading.background_type     = 'VIEWPORT'
        shading.background_color    = cls.id_data['chroma_color'] #[1, 1, 1]
    
    @classmethod
    def cleanup_temp_cube(cls, ctx):
        '''
        bpy.ops.view3d.localview(ctx)
        bpy.ops.object.delete(ctx, use_global=True)
        '''
        
        # RESTORE DATA.
        shading   = ctx.space_data.shading
        
        shading.type = cls.shading['type']
        shading.light = cls.shading['light']
        shading.color_type = cls.shading['color_type']
        shading.single_color = cls.shading['single_color']
        shading.background_type = cls.shading['background_type']
        shading.background_color = cls.shading['background_color']
        
    @classmethod
    def refresh_hack(cls, ctx):
        # HACK.
        ctx.area.tag_redraw()
        ##print("Refresh ...")
        if ctx.active_object:
            ctx.active_object.data.remesh_voxel_size = ctx.active_object.data.remesh_voxel_size
    
    @classmethod
    def draw_next(cls, ctx, a, x, y, w, h):
        if cls.id_data['match']:
            ##print("Matching...")

            Draw_Texture(cls.id_data['id'], x, y, w, h)
            
            px = [ch/255 for ch in GetPixel(x+w/2+1, y+h/2+1).to_list()[0:3]]
            ##print("- Pixel:", px)
            cls.id_data['matched'] = px == cls.id_data['chroma_color']
            
            # Check corners to white too?
            ##px1 = [ch/255 for ch in GetPixel(x+1, y+1).to_list()[0:3]]
            ##px2 = [ch/255 for ch in GetPixel(x+w-1, y+1).to_list()[0:3]]
            ##px3 = [ch/255 for ch in GetPixel(x+1, y+h-1).to_list()[0:3]]
            ##px4 = [ch/255 for ch in GetPixel(x+w-1, y+h-1).to_list()[0:3]]
            
            # FINISH.
            if cls.id_data['matched']:
                ##print("MACTHING DONE!")
                cls.cleanup_temp_cube(ctx)
            else:
                cls.id_data['id'] -= 1
            
            # HACK.
            cls.refresh_hack(ctx)
            return
        
        co1 = [0, 0, 1]
        co2 = [0, 1, 0]
        co3 = [1, 0, 0]
        co4 = [1, 0, 1]
        
        r = 25
        ax, ay = a.x, a.y
        aw, ah = a.width, a.height
        
        Draw_Text(60, 30, "* Sync in progress... *", 24)
        
        off_h = 28
        off_w = 10
        #for reg in a.regions:
        #    if reg.type in {'HEADER', 'TOOL_HEADER'}:
        #        off_h += reg.height/2
        dimm_point(Vector((0,0)), r, co1)
        dimm_point(Vector((aw-off_w*2, 0)), r, co2)
        dimm_point(Vector((0, ah-off_h)), r, co3)
        dimm_point(Vector((aw-off_w, ah-off_h)), r, co4)

        # HACK to wait until next update.
        if not cls.id_data['to_check']:
            cls.id_data['to_check'] = True
            Draw_Texture(cls.id_data['id'], x, y, w, h)
            # HACK.
            cls.refresh_hack(ctx)
            return
        
        ##print("Check ID:", cls.id_data['id'])
        
        Draw_Texture(cls.get_next_id(), x, y, w, h)
        
        px1 = [ch/255 for ch in GetPixel(x+1, y+1).to_list()[0:3]]
        px2 = [ch/255 for ch in GetPixel(x+w-1, y+1).to_list()[0:3]]
        px3 = [ch/255 for ch in GetPixel(x+1, y+h-1).to_list()[0:3]]
        px4 = [ch/255 for ch in GetPixel(x+w-1, y+h-1).to_list()[0:3]]
        
        ##print("- Pixel 1:", px1)
        ##print("- Pixel 2:", px2)
        ##print("- Pixel 3:", px3)
        ##print("- Pixel 4:", px4)
        
        cls.id_data['to_check'] = False
        
        cls.id_data['match'] = px1 == co1 and px2 == co2 and px3 == co3 and px4 == co4
        if cls.id_data['match']:
            cls.setup_temp_cube(ctx)
            ##print("MATCH!")
            #return
        
        # BUG. If this happen, it's a bug or special corner case.
        if cls.id_data['id'] > 100:
            cls.id_data['id'] = 0
            
        cls.refresh_hack(ctx)
        
    @classmethod
    def matched(cls):
        ##print("MATCHED:", cls.id_data['matched'])
        return cls.id_data['matched']
