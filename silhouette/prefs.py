import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import PointerProperty, BoolProperty

from . data import SILHOUETTE_STYLE


class SilhouetteAddonPreferences(AddonPreferences):
    bl_idname = __package__

    style : PointerProperty(type=SILHOUETTE_STYLE, name="Default Silhouette Style")

    def draw(self, context):
        layout = self.layout

        from . support import draw_support
        draw_support(layout)

        row = layout.row()
        
        self.draw_style(row, self.style, 'Silhouette Style')

    def draw_style(self, layout, style, title):
        col = layout.column(align=True)

        box = col.box()
        
        box.label(text=title)
        
        box = col.box()

        #box.prop(style, "use_viewport_settings")
        #row.enabled = not style.use_viewport_settings
        
        subcol = box.column(align=True)

        subcol.prop(style, "show_in_front")
        
        #subcol.separator()
        
        #subcol.prop(style, "use_flat_style")
        #subcol.prop(style, "show_shadows")
        #subcol.prop(style, "show_cavity")
        
        subcol = box.column(align=True)
        subcol.use_property_split = True
        subcol.use_property_decorate = False

        subcol.prop(style, "color")

        row = subcol.row(align=True)
        row.prop(style, 'show_background', text='Background')
        bgcol = row.column()
        bgcol.active = style.show_background
        bgcol.prop(style, 'bg_color', text='')

        row = subcol.row(align=True)
        row.prop(style, 'show_view_name', text='View Name')
        bgcol = row.column()
        bgcol.active = style.show_view_name
        bgcol.prop(style, 'text_color', text='')

        subcol.row().prop(style, "opacity", slider=True)



def get_prefs(ctx):
    return ctx.preferences.addons[__package__].preferences
