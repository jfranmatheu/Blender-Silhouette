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
        
        layout.label(text="Settings")
        layout.prop(settings, 'view_alignment')

        layout.separator()

        layout.prop(settings, 'target_type')
        if settings.target_type == 'OBJECT':
            layout.prop(settings, 'target_object')
        elif settings.target_type == 'COLLECTION':
            layout.prop(settings, 'target_collection')
        
        #layout.separator()
