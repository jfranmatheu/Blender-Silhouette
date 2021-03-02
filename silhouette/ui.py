from bpy.types import Panel
from . prefs import get_prefs


class VIEW3D_PT_silhouette(Panel):
    bl_label = "Silhouette"
    bl_context = "NONE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    bl_ui_units_x = 20

    #@classmethod
    #def poll(cls, context):
    #    return False

    def draw(self, context):
        layout = self.layout
        style = get_prefs(context).style
        settings = context.scene.silhouette

        layout.use_property_split = True
        
        main_row = layout.split(factor=0.5)

        left_layout = main_row.column(align=True)
        left_layout.active = settings.enabled

        block_header = left_layout.box()
        block_header.label(text="Fixed View")

        left_layout = left_layout.box()

        col = left_layout.column(align=True)

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
        
        #left_layout.separator()

        col = left_layout.column(align=True)

        header = col.box()
        header.label(text="Other Settings")

        content = col.box()
        content.use_property_split = False
        content.prop(settings, 'use_sculpt_auto_update')
    
        from . liv_ops import rtlive

        right_layout = main_row.column(align=True)
        right_layout.active = True

        block_header = right_layout.box()
        block_header.label(text="Navigation Live View")
        block_header.alert = True
        block_header.label(text="BETA Feature !")
        block_header.alert = False

        col = right_layout.column(align=True)

        '''
        header = col.box()
        header.label(text="Navigation Live View")
        header.alert = True
        header.label(text="[ BETA FEATURE ]")
        header.alert = False
        '''

        content = col.box()
        content.scale_y = 1.5

        if not rtlive:
            content.operator('silhouette.start_live', text="Start Live Silhouette")

        else:
            content.alert = True
            content.operator('silhouette.stop_live', text="Remove Live Silhouette")
            content.alert = False

            box = content.box()
            #box.label(text="Settings:", icon='SETTINGS')
            box.prop(settings, 'live_scale', text="Scale")
            box.prop(settings, 'live_alignment', text="Alignment")


        #box.prop(rt, 'color', text="Color")
        #box.prop(rt, 'bg_color', text="Background Color")
        #box.prop(rt, 'in_front', text="Show In Front")
