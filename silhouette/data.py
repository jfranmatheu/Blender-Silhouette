from bpy.types import PropertyGroup, Object, Collection
from bpy.props import *


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
    def mark_dirty(self, dummy):
        self.dirty = True

    use_viewport_settings : BoolProperty(default=False, name="Use Viewport Settings")

    use_transparency : BoolProperty(default=False, name="Use Transparent Background", set=mark_dirty)
    show_in_front : BoolProperty(default=False, name="Show In Front")

    use_flat_style : BoolProperty(default=True, name="Use Flat Style")
    show_shadows : BoolProperty(default=False, name="Show Shadows")
    show_cavity : BoolProperty(default=False, name="Show Cavity")

    color : FloatVectorProperty(default=(1, 1, 1), min=0, max=1,name="Color", subtype='COLOR', set=mark_dirty)
    bg_color : FloatVectorProperty(default=(0, 0, 0), min=0, max=1,name="Background Color", subtype='COLOR', set=mark_dirty)
    opacity : FloatProperty(default=1, max=1, min=0.01, step=0.1, name="Opacity", set=mark_dirty)

    dirty : BoolProperty(default=False)


class SILHOUETTE_SETTINGS(PropertyGroup):
    def mark_dirty(self, context):
        self.dirty = True

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

    target_object : PointerProperty(type=Object, name="Target Object", update=mark_dirty) # TODO: make it a duynamic enum and filter mesh objects.
    target_collection : PointerProperty(type=Collection, name="Target Collection", update=mark_dirty)

    dirty : BoolProperty(default=False)

    view_alignment : EnumProperty (
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
        description = "View alignment for silhouette",
        update=mark_dirty
    )
