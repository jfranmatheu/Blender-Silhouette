import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import PointerProperty, BoolProperty

from . data import SILHOUETTE_STYLE


class SilhouetteAddonPreferences(AddonPreferences):
    bl_idname = __package__

    style : PointerProperty(type=SILHOUETTE_STYLE, name="Default Silhouette Style")
    live_style : PointerProperty(type=SILHOUETTE_STYLE, name="Default Live Silhouette Style")
    show_beta_features : BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        self.draw_style(row, self.style, 'Silhouette Style')
        self.draw_style(row, self.live_style, 'Live Silhouette Style')

        layout.prop(self, 'show_beta_features', text="Show BETA features")

    def draw_style(self, layout, style, title):
        col = layout.column(align=True)

        box = col.box()
        
        box.label(text=title)
        
        box = col.box()

        #box.prop(style, "use_viewport_settings")
        #row.enabled = not style.use_viewport_settings
        
        subcol = box.column(align=True)
        
        subcol.prop(style, "use_transparency")
        subcol.prop(style, "show_in_front")
        
        #subcol.separator()
        
        #subcol.prop(style, "use_flat_style")
        #subcol.prop(style, "show_shadows")
        #subcol.prop(style, "show_cavity")
        
        subcol = box.column(align=True)
        subcol.use_property_split = True
        subcol.use_property_decorate = False

        subcol.prop(style, "color")
        if not style.use_transparency:
            subcol.prop(style, "bg_color")
        subcol.row().prop(style, "opacity", slider=True)


def get_prefs(ctx):
    return ctx.preferences.addons[__package__].preferences
