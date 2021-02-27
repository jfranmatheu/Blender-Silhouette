import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import PointerProperty

from . data import SILHOUETTE_STYLE


class SilhouetteAddonPreferences(AddonPreferences):
    bl_idname = __package__

    style : PointerProperty(type=SILHOUETTE_STYLE, name="Default Style")

    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        
        style = self.style
        box = col.box()
        
        box.label(text="Silhouette Style")
        #box.alert=True
        #box.label(text="Default style settings for when you create a silhouette", icon='INFO')
        #box.alert=False
        
        box = col.box()

        box.prop(style, "use_viewport_settings")
        
        row = box.row()
        row.enabled = not style.use_viewport_settings
        
        subcol = row.column(align=True)
        
        subcol.prop(style, "use_transparency")
        subcol.prop(style, "show_in_front")
        
        #subcol.separator()
        
        #subcol.prop(style, "use_flat_style")
        #subcol.prop(style, "show_shadows")
        #subcol.prop(style, "show_cavity")
        
        subcol = row.column(align=True)
        subcol.use_property_split = True
        subcol.use_property_decorate = False
        
        subcol.prop(style, "color")
        subcol.prop(style, "bg_color")
        subcol.row().prop(style, "opacity", slider=True)


def get_prefs(ctx):
    return ctx.preferences.addons[__package__].preferences
