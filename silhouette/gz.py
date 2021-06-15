from bpy.types import Gizmo as SILUETA, Context, Event, SpaceView3D, bpy_prop_collection, Object, Mesh
from mathutils import Vector, Color
import blf
from bpy.app import timers
from gpu_extras.presets import draw_texture_2d
from gpu.types import GPUOffScreen
from gpu_extras.batch import batch_for_shader
import bpy
from time import time as get_time
from bgl import (
    glEnable, glDisable, GL_BLEND, GL_DEPTH_TEST,
    glBlendFunc, GL_SRC_COLOR, GL_ONE_MINUS_CONSTANT_ALPHA,
    glActiveTexture, glBindTexture, GL_TEXTURE0, GL_TEXTURE_2D
)

from functools import partial

from . import DEBUG
from . matrix import get_magic_matrices_from_view_and_fixed_dimensions, get_cam_matrices, get_view_cam_matrices
from . prefs import get_prefs
from . utils import point_inside_rect
from . draw.text import Draw_Text


import bpy

from bpy.app.handlers import persistent
@persistent
def depsgraph_post_update(scene):
    if bpy.context.mode == 'EDIT_MESH': #, 'SCULPT'}:
        return
    VIEW3D_GT_silhouette.push_depsgraph_updates(bpy.context.evaluated_depsgraph_get().updates)


shading_props = {
    'light' : 'FLAT',
    'background_type' : 'VIEWPORT',
    'background_color' : (0.0, 0.0, 0.0),
    'color_type' : 'SINGLE',
    'single_color' : (1.0, 1.0, 1.0),
    'show_xray' : False,
    'show_shadows' : False,
    'show_cavity' : False,
    'show_specular_highlight' : False,
    'use_dof' : False,
}


class VIEW3D_GT_silhouette(SILUETA):

    _draw_handler_instance = None
    _offscreen_instance = None
    _instance = None

    @classmethod
    def push_depsgraph_updates(cls, dep_updates):
        if not cls._instance:
            if DEBUG:
                print("No Gizmo Instance")
            return
        instance = cls._instance
        if instance.deps_dirty:
            if DEBUG:
                print("Already marked dirty")
            return
        for update in dep_updates:
            # instance.target
            if update.id.original == bpy.context.object and (update.is_updated_geometry or update.is_updated_transform):
                if DEBUG:
                    print("Depsgraph Update mesh -> ", bpy.context.object)
                instance.deps_dirty = True
                return
    
    @classmethod
    def stop_draw_handler(cls):
        if cls._draw_handler_instance:
            try:
                SpaceView3D.draw_handler_remove(cls._draw_handler_instance, 'WINDOW')
            except ValueError:
                print("ERROR: DRAW HANDLER -> ValueError: callback_remove(handler): NULL handler given, invalid or already removed")
            cls._draw_handler_instance = None
            cls._instance = None
            return True
        return False

    def start_draw_handler(self, context = None):
        if not context: context = bpy.context
        self.__class__._instance = self
        #self.refresh_region(context)
        self.draw_handler = self.__class__._draw_handler_instance = SpaceView3D.draw_handler_add(self.draw_silhouette, (context,), 'WINDOW', 'POST_PIXEL')


    ''' Initialization. '''

    def setup(self) -> None:
        self.__class__._instance = self
        if DEBUG:
            print("GZ: SETUP")
        self.offscreen = None

        self.deps_dirty = False
        self.target = None
        self.target_location = Vector((0, 0, 0))
        self.target_rotation = Vector((0, 0, 0))
        self.target_dimensions = Vector((0, 0, 0))
        #self.target_scale = Vector((1, 1, 1)) # Used for multi-objects as collections...

        #self.camera = None
        self.camera_obj = None
        #self.camera_location = Vector((0, 0, 0))
        #self.camera_rotation = Vector((0, 0, 0))

        self.position = (50, 50)
        self.width  = 256
        self.height = 256

        self.act_op = None

        #self.init_offscreen()
        #self.init_graphics()

    def update_dimensions(self, context):
        if self.settings.is_navigation() and self.settings.use_region_dimensions:
            scale = self.settings.scale
            self.width = int(context.region.width * scale)
            self.height = int(context.region.height * scale)
        else:
            self.width, self.height = self.settings.dimensions

    def init(self, context):
        if DEBUG:
            print("GZ: INIT")

        self.offscreen = None
        self.act_op = id(context.active_operator) if context.active_operator else None

        self.style = get_prefs(context).style
        self.settings = context.scene.silhouette
        self.settings.dirty = True # HACK. Force init update...
        #self.view = self.settings.view_preset

        self.update_dimensions(context)

        self.target = None
        self.target_type = self.settings.target_type
        self.act_ob = context.active_object

        self.mode = context.mode
        self.time = get_time()
        self.sculpt_update_interval = 5.0

        self.init_offscreen()
        self.init_graphics()

        self.ctx_area = context.area

        self.__class__.stop_draw_handler()
        self.start_draw_handler(context)

        #print("\t-", self.style)
        #print("\t-", self.draw_handler)

    def refresh(self, context):
        self.style = get_prefs(context).style
        self.settings = context.scene.silhouette
        self.ctx_area = context.area
        #print("GZ: REFRESH")
        # Ensure that draw handler is initialized. (enabling/disabling/enabling BUG)
        #if self.style.dirty:
        #    self.update_shader(context)
        pass


    ''' Event handle. '''

    @staticmethod
    def get_mouse_pos(evt: Event) -> Vector:
        return Vector((evt.mouse_region_x, evt.mouse_region_y))

    def test_select(self, ctx: Context, loc: (int, int)) -> int:
        #print("TEST SELECT...")

        # NOTE: removed in 2.1.6
        ##if self.style.dirty:
        ##    self.update_shader(ctx)
        return 1 if point_inside_rect(*loc, *self.position, self.width, self.height) else -1

    def invoke(self, ctx: Context, evt: Event) -> set:
        if DEBUG:
            print("GZ: INVOKE", evt.type, evt.value)
        if evt.type in {'LEFTMOUSE', 'RIGHTMOUSE'}:
            # User/Manual Update for Sculpt Meshes.
            if ctx.mode == 'SCULPT' and ctx.active_object:
                ctx.region.tag_redraw()
                ctx.active_object.data.remesh_voxel_size *= 1
                self.redraw_silhouette(ctx)
        return {'FINISHED'}

    def modal(self, ctx: Context, evt: Event, tweak: str) -> set:
        if DEBUG:
            print("GZ: MODAL")
        return {'FINISHED'}

    def exit(self, ctx: Context, cancel: bool) -> None:
        if DEBUG:
            print("GZ: EXIT")

    def time_function(self, wait_time: float, func: callable, *args) -> None:
        timers.register(partial(func, *args), first_interval=wait_time) 


    ''' Drawing. '''

    def init_graphics(self) -> None:
        if DEBUG:
            print("GZ: Init Graphics")
        from . draw.gpu_shaders import shader_silueta
        self.shader = shader_silueta
        self.repaint() 

    def repaint(self) -> None:
        ##print("GZ: Repaint")
        self.update_shader()
        self.update_batch()

    def update_batch(self) -> None:
        from . draw.geo import get_silu_verts
        self.batch = batch_for_shader(self.shader, 'TRI_FAN', { "pos" : get_silu_verts(*self.position, self.width, self.height), "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) },)
        ##print("\t-", self.batch)

    def update_shader(self, ctx = None) -> None:
        #if DEBUG:
        #print("*** SHADER UPDATED ***")
        shader = self.shader
        style = self.style
        shader.bind()
        shader.uniform_float("use_transp", 1.0 if style.use_transparency else 0.0)
        shader.uniform_float("alpha", style.opacity)
        shader.uniform_float("co", style.color)
        shader.uniform_float("bco", style.bg_color)
        style.dirty = False

        if ctx and ctx.area and ctx.area.type == 'VIEW_3D':
            ctx.region.tag_redraw()
        ##print("\t-", self.shader)

    def init_offscreen(self) -> None:
        if DEBUG:
            print("GZ: Init Offscreen")
        if self.__class__._offscreen_instance:
            self.offscreen = self.__class__._offscreen_instance
        else:
            self.update_offscreen()
        ##print("\t-", self.offscreen)

    def update_offscreen(self):
        self.offscreen = self.__class__._offscreen_instance = GPUOffScreen(self.width, self.height)

    def refresh_region(self, ctx: Context) -> None:
        #print("GZ: Refresh Region")
        if not ctx.region:
            print("ERROR: AttributeError: 'NoneType' object has no attribute 'tag_redraw'")
            return
        ctx.region.tag_redraw()

    def draw(self, context: Context) -> None:
        #print("Drawing...")
        if not self.__class__._draw_handler_instance:
            self.start_draw_handler(context)

    def draw_select(self, ctx: Context, select_id: int) -> None:
        pass

    def draw_silhouette_from_view_preset(self, context):
        if self.settings.dirty:
            self.update_dimensions(context)
            self.update_targets(context) # full update in case property of target type or target changed.

        elif context.active_object: # and context.active_object.type in 'MESH':
            
            #''' Active object has changed so we may check few cases... '''
            if self.act_ob != context.active_object:
                self.act_ob = context.active_object

                if isinstance(self.target, Object):
                    if self.settings.target_type == 'ACTIVE_OBJECT':
                        self.update_targets(context)
                    # Else: Fixed Object. NO NEED TO DO ANYTHING...
                    #print("FIXED OBJECT")
                
                elif self.settings.target_type == 'SELECTED_OBJECTS':
                    self.update_targets(context)
                
                # BUG. Should check targets first...
                else:
                    self.update_targets(context, False)
                    if self.target and context.active_object in self.target:
                        self.redraw_silhouette(context)
            
            #''' They are the same, check position/dimensions... '''
            else:
                if isinstance(self.target, Object):
                    to_check_ob = self.target # ACTIVE_OBJECT or OBJECT (Fixed Target)
                    
                elif self.target and context.active_object in self.target:
                    to_check_ob = context.active_object

                    # Special case...
                    # Change selection from 2 to 1 but active object remain the same...
                    if self.settings.target_type == 'SELECTED_OBJECTS':
                        target_count = len(self.target)
                        self.update_targets(context, False)
                        if target_count != len(self.target):
                            self.redraw_silhouette(context)
                
                else:
                    to_check_ob = None

                if to_check_ob:
                    #print("LOCATION:", self.target_location, to_check_ob.location)
                    if self.target_location != to_check_ob.location:
                        self.redraw_silhouette(context)
                        self.target_location = to_check_ob.location.copy()
                    elif self.target_dimensions != to_check_ob.dimensions:
                        self.redraw_silhouette(context)
                        self.target_dimensions = to_check_ob.dimensions.copy()
                    elif self.check_rotation_change(to_check_ob):
                        self.redraw_silhouette(context)
                    
                    # BUG: For some reason scale!=1,1,1 doesn't affect with multiple objects matrix algorithm...
                    #elif self.multi_object and self.target_scale != to_check_ob.scale:
                    #    self.target_scale = to_check_ob.scale.copy()
                    #    self.redraw_silhouette(context)

                    # NOTE: for now we need to update on edit mode every time cause mesh it's going to be edited all time...
                    ## WORKAROUND: for future would be to use handlers depsgraph in some way...
                    elif context.mode in {'EDIT', 'EDIT_MESH'}:
                        if self.deps_dirty:
                            self.deps_dirty = False
                            self.redraw_silhouette(context)
                        elif context.active_operator and id(context.active_operator) != self.act_op:
                            self.act_op = id(context.active_operator)
                            self.redraw_silhouette(context)
                    elif context.mode == 'SCULPT':
                        if self.settings.use_sculpt_auto_update:
                            '''
                            if self.deps_dirty:
                                print("HELLO??")
                                to_check_ob.data.remesh_voxel_size *= 1 #OK... Quicker lmao
                                self.deps_dirty = False
                                self.redraw_silhouette(context)
                                self.time = get_time()
                            '''
                            if get_time() - self.time > self.sculpt_update_interval:
                                #to_check_ob.data.vertices.update() # OK...
                                #to_check_ob.data.update_tag() # OK...
                                #to_check_ob.update_tag(refresh={'DATA'}) #OK...
                                ##to_check_ob.data.update_gpu_tag() # NOPE
                                #context.window_manager.operators
                                to_check_ob.data.remesh_voxel_size *= 1 #OK... Quicker lmao
                                self.redraw_silhouette(context)
                                self.time = get_time()


        # NOTE: Not useful code atm!
        elif context.mode != self.mode:
            if self.mode == 'SCULPT':
                self.redraw_silhouette(context)
                self.time = get_time()
            self.mode = context.mode

    def draw_silhouette_from_view_camera(self, context, is_navigation: bool = True):
        #if self.settings.dirty:
        #    self.update_dimensions(context)
        #    self.settings.dirty = False
        
        if not is_navigation:
            if not self.settings.view_camera:
                return

            if not self.camera_obj or self.settings.view_camera != self.camera_obj.data:
                self.camera_obj = bpy.data.objects.get(self.settings.view_camera.name, None)
                if not self.camera_obj:
                    return

        self.redraw_silhouette(context)

        ''' SCULPT WORKAROUND. '''
        if context.mode != self.mode:
            if self.mode == 'SCULPT':
                #self.redraw_silhouette(context)
                self.time = get_time()
            self.mode = context.mode
            return

        if context.mode == 'SCULPT': # and to_check_ob:
            if self.settings.use_sculpt_auto_update:
                if get_time() - self.time > self.sculpt_update_interval:
                    #to_check_ob.data.remesh_voxel_size *= 1 #OK... Quicker lmao
                    context.active_object.data.remesh_voxel_size *= 1
                    #self.redraw_silhouette(context)
                    self.time = get_time()

    def draw_silhouette(self, context) -> None:
        #if context.area != self.ctx_area:
        #    return
        #print("Drawing Offscreen...")
        if not self.offscreen: # not target or 
            return

        #context = bpy.context
        style = self.style
        view_mode = self.settings.view_mode

        if self.settings.refresh_offscreen:
            self.update_dimensions(context)
            self.update_offscreen()
            self.settings.refresh_offscreen = False
            self.settings.dirty = False
            #self.redraw_silhouette(context)
            self.repaint()

            if self.settings.is_preset():
                self.update_targets(context) # full update in case property of target type or target changed.

        elif self.settings.force_refresh:
            self.update_targets(context)
            self.settings.dirty = False

        if view_mode == 'PRESET':
            self.draw_silhouette_from_view_preset(context)
        elif view_mode in {'CAMERA', 'NAV'}:
            self.draw_silhouette_from_view_camera(context, view_mode=='NAV')

        #icon = context.active_object.material_slots[0].material.preview.icon_id #self.target[0].preview.icon_id
        #glBindTexture(GL_TEXTURE_2D, icon)
        #draw_texture_2d(icon, Vector(self.position)+Vector((self.width, 0)), self.width, self.height)

        if not style.show_in_front:
            glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.offscreen.color_texture)

        # Draw texture.
        #draw_texture_2d(self.offscreen.color_texture, self.position, self.width, self.height)
        if self.style.dirty:
            self.update_shader(context)
        self.batch.draw(self.shader)

        if not style.show_in_front:
            glDisable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)

        if context.mode == 'SCULPT' and not self.settings.use_sculpt_auto_update:
            Draw_Text(self.position[0] + 5, self.position[1] + 5, "Tap to refresh!", 12, 0, 1.0, .06, .9, .9, True)

        #print("Drawing Offscreen... END")


    def update_targets(self, context, redraw_on_update: bool = True):
        settings = self.settings
        target, multi_object = settings.get_target(context)
        
        if not target or (not multi_object and target.type != 'MESH'):
            return
        
        self.target = target
        self.multi_object = multi_object

        if redraw_on_update:
            self.redraw_silhouette(context)


    def redraw_silhouette(self, context) -> None:
        style = self.style

        scene = context.scene
        settings = self.settings

        if settings.is_navigation():
            if not scene.camera:
                return
        
        # Backup. # We want to hide overlays and gizmos for any configuration we have.
        space = context.space_data
        shading = space.shading

        show_overlays   = space.overlay.show_overlays
        show_gizmo      = space.show_gizmo
        space.overlay.show_overlays = False
        space.show_gizmo            = False

        # Shading settings...
        backup_props = {}
        for key, value in shading_props.items():
            backup_props[key] = getattr(shading, key)
            setattr(shading, key, value)

        # Offscreen draw 3d viewport.
        #if self.target != target or self.target_location != target.location or self.target_dimensions != target.dimensions:

        # TODO: OVERLAYS TOGGLE SHOULD BE HERE...
        if settings.is_preset():
            mat = get_magic_matrices_from_view_and_fixed_dimensions(self.target, self.multi_object, settings.view_preset, self.width, self.height)
        elif self.camera_obj and settings.is_camera():
            mat = get_cam_matrices(context, self.camera_obj, self.width, self.height)
        else:
            #if settings.use_region_dimensions:
            #    dims = (int(context.region.width*settings.scale), int(context.region.height*settings.scale))
            #else:
            dims = (self.width, self.height)
            mat = get_view_cam_matrices(context, *dims)

        self.offscreen.draw_view3d(
            scene,
            context.view_layer,
            context.space_data,
            context.region,
            *mat
        )
        
        # Return to original settings.
        space.overlay.show_overlays     = show_overlays
        space.show_gizmo                = show_gizmo

        for key, value in backup_props.items():
            setattr(shading, key, value)
        
        self.settings.dirty = False
        if DEBUG:
            print("REDRAW SILHOUETTE")

    def check_rotation_change(self, to_check_ob):
        rot_mode = to_check_ob.rotation_mode
        if rot_mode == 'QUATERNION' and self.target_rotation != to_check_ob.rotation_euler:
            self.target_rotation = to_check_ob.rotation_quaternion # NOTE: No need to copy...
            return True
        elif rot_mode == 'AXIS_ANGLE' and self.target_rotation != to_check_ob.rotation_axis_angle:
            self.target_rotation = to_check_ob.rotation_axis_angle # NOTE: No need to copy...
            return True
        elif self.target_rotation != to_check_ob.rotation_euler:
            self.target_rotation = to_check_ob.rotation_euler.copy() # NOTE: Needs to copy...
            return True
        return False
