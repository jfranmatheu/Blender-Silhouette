from math import cos

import bpy
from bpy.types import Operator, SpaceView3D
from mathutils import Euler, Vector
from bgl import glEnable, glDisable, GL_DEPTH_TEST

from . ctx import *
from . draw.rect import draw_rect
from . draw.text import Draw_Text_AlignCenter
from . draw.gl_fun import GetPixel
from . draw.image import Draw_Texture


rtlive = []


class SILHOUETTE_OT_start_live(Operator):
    bl_idname = "silhouette.start_live"
    bl_label = "Start Live Navigation View"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.active_object or context.active_object.type != 'MESH':
            return False
        return rtlive is not None and len(rtlive) == 0


    def execute(self, context):
        from . import DEBUG
        if rtlive:
            bpy.ops.silhouette.stop_live()
        
        '''
        rt = context.window_manager.render_texture.live
        rt.texid = -1 # Reset ID.
        if DEBUG:
            dummy = (rt, 'debug_buffer')
            self.finish(context, -1, dummy)
        else:
        '''
        if not context.window_manager.modal_handler_add(self):
            return {'CANCELLED'}
        
        self.silhouette = context.scene.silhouette

        self.init_mode = context.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        self.silhouette_state = self.silhouette.enabled
        self.silhouette.enabled = False
        self.texid = 0
        #texid = rt.get_id(context)
        #rt.texid = texid if texid else 0
        self.silhouette.live_texid = 0
        self.match = False
        self.shading = {}
        self.skip_matches = 0
        self.x, self.y, self.w, self.h = self.silhouette.get_live_pos_size(context)
        self.start_timer(context)
        self.init_style(context)
        self.init_object = context.active_object
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.view3d.localview()
        bpy.ops.view3d.view_axis(type='FRONT', align_active=True)
        context.active_object.name = "TemporalSyncCube"
        self._handler = SpaceView3D.draw_handler_add(self.draw, (context, ), 'WINDOW', 'POST_PIXEL')
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}


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

    def finish(self, context):
        from . prefs import get_prefs
        ##print("[MODAL] Finished!")
        from . liv_draw import live_draw_callback_px
        from . id_finder import IDFinder

        context.area.tag_redraw()

        #rt = context.window_manager.render_texture.live
        style = get_prefs(context).style
        IDFinder.reset()
        DC = DrawContext(context)
        DC.set_handler(live_draw_callback_px, bpy.ops.silhouette.stop_live, (self.silhouette, style))
        rtlive.append(DC)

        self.silhouette.enabled = self.silhouette_state

        from . draw.gpu_shaders import shader_live_silueta as shader
        shader.bind()
        shader.uniform_float("use_transp", 1.0 if style.use_transparency else 0.0)
        shader.uniform_float("alpha", style.opacity)
        shader.uniform_float("co", style.color)
        shader.uniform_float("bco", style.bg_color)

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
        Draw_Texture(self.texid, x, y, w, h)
        
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
        #if event.type == 'TIMER':
        context.area.tag_redraw()
        #rt = context.window_manager.render_texture.live
        #x, y, w, h = self.x, self.y, self.w, self.h

        if self.match:
            ##print("[MODAL] Matched!")
            #rt.texid = self.texid
            self.silhouette.live_texid = self.texid
            self.restore_style(context)
            self.finish_modal(context)
            return {'FINISHED'}

        if self.texid > 100:
            #texid = rt.get_id(context)
            #if texid:
            #    self.texid = texid
            self.texid = None
            self.silhouette.live_texid = -1 # 0

            self.finish_modal(context)
            return {'FINISHED'}
        #print("Hi")
        return {'RUNNING_MODAL'}

    def finish_modal(self, context):
        self.restore_style(context)
        self.stop_timer(context)
        self.stop_draw()
        self.finish(context)
        bpy.ops.view3d.localview()
        bpy.ops.object.delete(use_global=True)
        if self.init_object:
            context.view_layer.objects.active = self.init_object
            self.init_object.select_set(True)
            bpy.ops.object.mode_set(mode=self.init_mode)
        #print("*** FINISH START MODAL ***")


class SILHOUETTE_OT_stop_live(Operator):
    bl_idname = "silhouette.stop_live"
    bl_label = "Stop Live Navigation View"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return rtlive and len(rtlive) != 0

    def execute(self, context):
        #global rtlive
        context.area.tag_redraw()
        for rtl in rtlive:
            rtl.stop()
        rtlive.clear()
        return {'FINISHED'}
