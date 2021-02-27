from bpy.types import Operator, SpaceView3D
import bpy
from math import cos
from mathutils import Euler, Vector
from bgl import glEnable, glDisable, GL_DEPTH_TEST

from . rt_prop_fun import update_render_textures, override
from . rect import draw_rect
from . text import Draw_Text_AlignCenter
from . gl_fun import GetPixel
from . rt_draw import Draw_Image_MoreSimple

global rtlive
rtlive = None

class SILHOUETTE_OT_start_live(Operator):
    bl_idname = "silhouette.start_live"
    bl_label = "Start Live Navigation View"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        global rtlive
        return rtlive is not None # len(rtlive) == 0

    def execute(self, context):
        from . import DEBUG
        global rtlive
        if rtlive:
            bpy.ops.rt.stop_live_render_texture()
        rt = context.window_manager.render_texture.live
        rt.texid = -1 # Reset ID.
        if DEBUG:
            dummy = (rt, 'debug_buffer')
            self.finish(context, -1, dummy)
        else:
            # OLD METHOD
            if not rt.use_modal_to_find_id:
                texid = rt.get_id(context)
                self.finish(context, texid if texid is not None else 0, None)
                return {'FINISHED'}
            '''
            id = rt.get_id(context)
            if not id:
                self.report({'ERROR'}, "Can't create the silhouette. Try using it on default sculpting workspace before reporting it.")
                return {'FINISHED'}
            dummy = None
            '''
            # NEW METHOD
            if not context.window_manager.modal_handler_add(self):
                return {'CANCELLED'}
            
            self.texid = 0
            texid = rt.get_id(context)
            rt.texid = texid if texid else 0
            self.match = False
            self.shading = {}
            self.skip_matches = 0
            self.x, self.y, self.w, self.h = rt.get_pos_size(context.area)
            self.start_timer(context)
            self.init_style(context)
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            bpy.ops.view3d.localview()
            bpy.ops.view3d.view_axis(type='FRONT', align_active=True)
            context.active_object.name = "TemporalSyncCube"
            self._handler = SpaceView3D.draw_handler_add(self.draw, (context, ), 'WINDOW', 'POST_PIXEL')
            context.area.tag_redraw()
            return {'RUNNING_MODAL'}
        context.area.tag_redraw()
        return {'FINISHED'}
    
    
    def init_style(self, context):
        shading = context.space_data.shading
        
        self.backup_style(shading)

        # UPDATE DATA TEMPORALY.
        shading.type                = 'SOLID'
        shading.light               = 'FLAT'
        shading.color_type          = 'SINGLE'
        shading.single_color        = [1.0, 1.0, 0.0]
        shading.background_type     = 'VIEWPORT'
        shading.background_color    = [0.0, 0.0, 0.0]
    
    def backup_style(self, shading):
        # BACKUP DATA.
        self.shading['type']                = shading.type
        self.shading['light']               = shading.light
        self.shading['color_type']          = shading.color_type
        self.shading['single_color']        = shading.single_color
        self.shading['background_type']     = shading.background_type
        self.shading['background_color']    = shading.background_color
    
    def restore_style(self, context):
        # RESTORE DATA.
        shading   = context.space_data.shading
        
        shading.type = self.shading['type']
        shading.light = self.shading['light']
        shading.color_type = self.shading['color_type']
        shading.single_color = self.shading['single_color']
        shading.background_type = self.shading['background_type']
        shading.background_color = self.shading['background_color']
    
    def finish(self, context, texid, dummy):
        global rtlive
        ##print("[MODAL] Finished!")
        from . live_draw import live_draw_callback_px
        from . id_finder import IDFinder
        rt = context.window_manager.render_texture.live
        IDFinder.reset()
        DC = DrawContext(context)
        DC.set_handler(live_draw_callback_px, bpy.ops.rt.stop_live_render_texture, rt, texid, dummy)
        rtlive = DC
        context.area.tag_redraw()

    def draw_overlap(self, context):
        a = context.area
        draw_rect((0,0),(a.width,a.height),(0.1,0.1,0.1,1.0))
        Draw_Text_AlignCenter(a.width/2, a.height/2, "Loading ...", 32, (1,1,1,1), False, 0)

    def draw(self, context):
        if self.match:
            ##print("[MODAL-DRAW] Matched!")
            return
        glDisable(GL_DEPTH_TEST)
        ##print("[MODAL-DRAW] Tex ID:", self.texid)
        x, y, w, h = self.x, self.y, self.w, self.h
        Draw_Image_MoreSimple(self.texid, x, y, w, h)
        
        px = [ch/255 for ch in GetPixel(x+w/2-1, y+h/2-1).to_list()[0:3]]
        ##print("- Pixel:", px)
        
        match = px == [1.0, 1.0, 0.0]
        if match:
            self.match = self.skip_matches == 0
            self.skip_matches -= 1
        else:
            self.texid += 1
        
        #px1 = [ch/255 for ch in GetPixel(x+5, y+5).to_list()[0:3]]
        #px2 = [ch/255 for ch in GetPixel(x+w-5, y+5).to_list()[0:3]]
        #px3 = [ch/255 for ch in GetPixel(x+5, y+h-5).to_list()[0:3]]
        #px4 = [ch/255 for ch in GetPixel(x+w-5, y+h-5).to_list()[0:3]]
        
        #print("- Pixel 1:", px1)
        #print("- Pixel 2:", px2)
        #print("- Pixel 3:", px3)
        #print("- Pixel 4:", px4)
        
        #self.match = px1 == px2 == px3 == px4 == [0.0, 1.0, 0.2]
        
        glEnable(GL_DEPTH_TEST)
        
        self.draw_overlap(context)
        
    def stop_draw(self):
        if hasattr(self, '_handler'):
            SpaceView3D.draw_handler_remove(self._handler, 'WINDOW')
    
    def start_timer(self, context):
        self.timer = context.window_manager.event_timer_add(1/120, window=context.window)
    
    def stop_timer(self, context):
        if hasattr(self, 'timer'):
            context.window_manager.event_timer_remove(self.timer)
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            context.area.tag_redraw()
            rt = context.window_manager.render_texture.live
            #x, y, w, h = self.x, self.y, self.w, self.h

            if self.match:
                ##print("[MODAL] Matched!")
                rt.texid = self.texid
                self.restore_style(context)
                self.finish_modal(context)
                return {'FINISHED'}

            if self.texid > 100:
                texid = rt.get_id(context)
                if texid:
                    self.texid = texid
                self.finish_modal(context)
                return {'FINISHED'}
        return {'RUNNING_MODAL'}
    
    def finish_modal(self, context):
        self.restore_style(context)
        self.stop_timer(context)
        self.stop_draw()
        self.finish(context, self.texid, None)
        bpy.ops.view3d.localview()
        bpy.ops.object.delete(use_global=True)


class SILHOUETTE_OT_stop_live(Operator):
    bl_idname = "silhouette.stop_live"
    bl_label = "Stop Live Navigation View"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        global rtlive
        return rtlive # and len(rtlive) != 0

    def execute(self, context):
        global rtlive
        #for rtl in rtlive:
        #    rtl.stop()
        rtlive.stop()
        rtlive.clear()
        context.area.tag_redraw()
        return {'FINISHED'}
