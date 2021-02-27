from bpy.types import Panel
from . prefs import get_prefs


class VIEW3D_PT_silhouette(Panel):
    bl_label = "Silhouette"
    bl_context = "NONE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    
    #@classmethod
    #def poll(cls, context):
    #    return False

    def draw(self, context):
        layout = self.layout
        style = get_prefs(context).style
        settings = context.scene.silhouette

        layout.active = settings.enabled
        
        col = layout.column(align=True)

        header = col.box()
        header.label(text="Settings")

        content = col.box()
        content.prop(settings, 'view_preset')

        content.separator()

        content.label(text="Target")
        content.prop(settings, 'target_type', text="Type")
        if settings.target_type == 'OBJECT':
            content.prop(settings, 'target_object', text="")
        elif settings.target_type == 'COLLECTION':
            content.prop(settings, 'target_collection', text="")
        
        layout.separator()

        col = layout.column(align=True)

        header = col.box()
        header.label(text="Other Settings")

        content = col.box()
        content.prop(settings, 'use_sculpt_auto_update')
