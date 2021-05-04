from bpy.types import PropertyGroup, Object, Collection, Camera
from bpy.props import *

from . ctx import get_area_off


VIEW_FRONT = 0
VIEW_BACK = 1
VIEW_LEFT = 2
VIEW_RIGHT = 3
VIEW_TOP = 4
VIEW_BOTTOM = 5
VIEW_CAMERA = 6
VIEW_NAV = 7

VIEW_3_4_FRONT_LEFT = 8
VIEW_3_4_FRONT_RIGHT = 9
VIEW_3_4_BACK_LEFT = 10
VIEW_3_4_BACK_RIGHT = 11


class SILHOUETTE_STYLE(PropertyGroup):
    def mark_dirty(self, context):
        self.dirty = True

        #print("MARK DIRTY")
        #print("\t", context.area.type)
        #if context.area.type == 'VIEW_3D':
        #    context.area.tag_redraw()

    use_viewport_settings : BoolProperty(default=False, name="Use Viewport Settings", update=mark_dirty)

    use_transparency : BoolProperty(default=False, name="Use Transparent Background", update=mark_dirty)
    show_in_front : BoolProperty(default=False, name="Show In Front")

    use_flat_style : BoolProperty(default=True, name="Use Flat Style")
    show_shadows : BoolProperty(default=False, name="Show Shadows")
    show_cavity : BoolProperty(default=False, name="Show Cavity")

    color : FloatVectorProperty(default=(1, 1, 1), min=0, max=1,name="Color", subtype='COLOR', update=mark_dirty)
    bg_color : FloatVectorProperty(default=(0, 0, 0), min=0, max=1,name="Background Color", subtype='COLOR', update=mark_dirty)
    opacity : FloatProperty(default=1, max=1, min=0.01, step=0.1, name="Opacity", update=mark_dirty)

    dirty : BoolProperty(default=False)


class SILHOUETTE_SETTINGS(PropertyGroup):
    def mark_dirty(self, context):
        self.dirty = True

    def mark_off_dirty(self, context):
        self.refresh_offscreen = True
        #self.dirty = True

    def select_target(self, context):
        if not self.target_object:
            return
        if self.target_object.type != 'MESH':
            self.target_object = None
            return
        self.mark_dirty(context)

    def get_target(self, context):
        target_type = self.target_type
        if target_type == 'ACTIVE_OBJECT':
            return context.active_object, False
        elif target_type == 'SELECTED_OBJECTS':
            return [ob for ob in context.selected_objects if ob.type == 'MESH'], True
        elif target_type == 'OBJECT':
            if self.target_object:
                return self.target_object, False
            return context.active_object, False
        elif target_type == 'COLLECTION':
            if self.target_collection and bool(self.target_collection.objects):
                return [ob for ob in self.target_collection.objects if ob.type == 'MESH'], True
            return context.active_object, False
        return context.active_object, False

    enabled : BoolProperty(default=False, name="Enable Silhouette", description="Toggle silhouette overlay in 3d viewport")

    target_type : EnumProperty(
        items=(
            ('ACTIVE_OBJECT', 'Active Object', "Will focus on active object"),
            ('SELECTED_OBJECTS', 'Selected Objects', "Will frame every select object"),
            ('OBJECT', 'Fixed Object', "Will focus on the specified object"),
            ('COLLECTION', 'Collection', "Will frame every object in specified collection"),
        ),
        name="Target Type",
        default='ACTIVE_OBJECT',
        update=mark_dirty
    )

    target_object : PointerProperty(type=Object, name="Target Object", update=select_target) # TODO: make it a duynamic enum and filter mesh objects.
    target_collection : PointerProperty(type=Collection, name="Target Collection", update=mark_dirty)

    def update_mode(self, context):
        if self.is_navigation():
            self.refresh_offscreen = True
        elif self.prev_view_mode == 'NAV':
            self.refresh_offscreen = True
        self.prev_view_mode = self.view_mode
        self.mark_dirty(context)

    view_mode : EnumProperty (
        items = (
            ('PRESET',   "Preset",    "Use a predefined view"),
            ('CAMERA',   "Camera",    "Custom view based on a camera object"),
            ('NAV',      "Navigation","View based on your current 3d viewport view")
            #('CUSTOM',   "Custom",    "Custom view based on your viewport view, you can update it with {'SHORTCUT'}")
        ),
        default = 'PRESET',
        name = "View Mode",
        description = "Options to adjust the silhouette's view",
        update=update_mode
    )

    prev_view_mode : StringProperty(default='PRESET')

    def is_preset(self): return self.view_mode == 'PRESET'
    def is_camera(self): return self.view_mode == 'CAMERA'
    def is_navigation(self): return self.view_mode == 'NAV'

    use_region_dimensions : BoolProperty(default=True, name='Use Viewport Proportions', description="Sync silhouette dimensions with 3d viewport's editor proportions", update=mark_off_dirty)
    scale : FloatProperty(default=.24, min=0.1, max=.5, step=0.05, name='Scale', update=mark_off_dirty, description="Scale silhouette by using 3d viewport's editor proportions and dimensions")

    dimensions : IntVectorProperty(default=(256, 256), min=64, max=1024, update=mark_off_dirty, name="Dimensions", size=2, subtype='XYZ', step=16)

    dirty : BoolProperty(default=False)
    refresh_offscreen : BoolProperty(default=False)

    view_preset : EnumProperty (
        items = (
            ('FRONT',   "Front",    "front view",    VIEW_FRONT),
            #('3_4_FRONT_LEFT', "3/4 Front Left", "3/4 front left view", VIEW_3_4_FRONT_LEFT),
            #('3_4_FRONT_RIGHT', "3/4 Front Right", "3/4 front right view", VIEW_3_4_FRONT_RIGHT),
            #('3_4_BACK_LEFT', "3/4 Back Left", "3/4 back right view", VIEW_3_4_BACK_LEFT),
            #('3_4_BACK_RIGHT', "3/4 Back Right", "3/4 back right view", VIEW_3_4_BACK_RIGHT),
            ('BACK',    "Back",     "back view",     VIEW_BACK),
            ('LEFT',    "Left",     "left view",     VIEW_LEFT),
            ('RIGHT',   "Right",    "right view",    VIEW_RIGHT),
            ('TOP',     "Top",      "top view",      VIEW_TOP),
            ('BOTTOM',  "Bottom",   "bottom view",   VIEW_BOTTOM),
            #('CAMERA',  "Custom",   "Custom view based on a camera", VIEW_CAMERA),
            #('NAV',     "View",     "Based on viewport navigation view", VIEW_NAV)
        ),
        default = 'FRONT',
        name = "View",
        description = "Preset for silhouette view",
        update=mark_dirty
    )

    view_camera : PointerProperty(type=Camera, name="View Camera", update=mark_dirty)

    use_multi_view : BoolProperty(default=False, name="Use Multi View", description="Toggle multi view silhouettes", update=mark_dirty)

    alignment : EnumProperty (
        items=(
            ('TOP_LEFT',        "Top-Left",     "Align silhouette to the top-left corner"),
            ('TOP_RIGHT',       "Top-Right",    "Align silhouette to the top-right corner"),
            ('BOTTOM_LEFT',     "Bottom-Left",  "Align silhouette to the bottom-left corner"),
            ('BOTTOM_RIGHT',    "Bottom-Right", "Align silhouette to the bottom-right corner")
        ), default='TOP_LEFT',
        name = "Alignment",
        update=mark_dirty
    )

    direction : EnumProperty (
        items=(
            ('HORIZONTAL',     "Horizontal",  "Align silhouettes horizontaly"),
            ('VERTICAL',       "Vertical",    "Align silhouettes verticaly")
        ), default='VERTICAL',
        name = "Direction",
        update=mark_dirty
    )

    use_sculpt_auto_update : BoolProperty(default=False, name="Auto-Update on Sculpt Mode", description="Sculpt Mode doesn't register sculpting actions by itself (core bug since 2.82) so this is meant to solve that issue (tho you still can tap over the silhouette to manually update preview or use 'Navigation Live View' feature!)")
    force_refresh : BoolProperty(default=False, name="Force Refresh")

    ''' Live Navigation View Settings. '''
    live_scale : FloatProperty(default=.5, min=0.2, max=1, step=0.05)

    live_alignment : EnumProperty (
        items=(
            ('TOP_LEFT',        "Top-Left",     "Align silhouette to the top-left corner"),
            ('TOP_RIGHT',       "Top-Right",    "Align silhouette to the top-right corner"),
            ('BOTTOM_LEFT',     "Bottom-Left",  "Align silhouette to the bottom-left corner"),
            ('BOTTOM_RIGHT',    "Bottom-Right", "Align silhouette to the bottom-right corner")
        ), default='TOP_LEFT'
    )

    live_texid : IntProperty(default=-1)

    def get_live_pos_size(self, context):
        a = context.area
        h = a.height * .5 * self.live_scale
        w = a.width * .5 * self.live_scale
        if self.live_alignment == 'TOP_LEFT':
            x, y = get_area_off(a, {'TOOLS', 'TOOL_HEADER', 'HEADER'})
            return x, y + a.height - h, w, h
        elif self.live_alignment == 'TOP_RIGHT':
            x, y = get_area_off(a, {'UI', 'TOOL_HEADER'})
            return x + a.width - w, y + a.height - h, w, h
        elif self.live_alignment == 'BOTTOM_LEFT':
            x, y = get_area_off(a, {'TOOLS'})
            return x, y, w, h # TODO: What if tool header position is flipped?
        elif self.live_alignment == 'BOTTOM_RIGHT':
            x, y = get_area_off(a, {'UI'})
            return x + a.width - w, y, w, h
        return 0, 0, 256, 256
