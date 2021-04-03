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

    def draw_view_preset(self, settings, left_layout, content):
        content.label(text="Target")
        content.prop(settings, 'target_type', text="Type")
        if settings.target_type == 'OBJECT':
            content.prop(settings, 'target_object', text="")
        elif settings.target_type == 'COLLECTION':
            content.prop(settings, 'target_collection', text="")

    def draw_view_camera(self, settings, left_layout, content):
        pass

    def draw_view_nav(self, settings, left_layout, content):
        content.use_property_split = False
        content.prop(settings, 'use_region_dimensions')
        
        if settings.use_region_dimensions:
            content.prop(settings, 'scale', slider=True)
        else:
            content.column(align=True).prop(settings, 'dimensions', slider=True)

    def draw_common_settings(self, settings, left_layout):
        col = left_layout.column(align=True)
        col.use_property_split = False

        header = col.box()
        header.label(text="Other Settings")

        content = col.box()
        content.prop(settings, 'use_sculpt_auto_update')

    def draw(self, context):
        layout = self.layout
        prefs = get_prefs(context)
        style = prefs.style
        settings = context.scene.silhouette

        layout.use_property_split = True
        layout.use_property_decorate = False

        main_row = layout.split(factor=0.5)

        left_layout = main_row.column(align=True)
        #left_layout.active = settings.enabled

        block_header = left_layout.box()
        block_header.label(text="Fixed View")

        left_layout = left_layout.box()

        col = left_layout.column(align=True)

        options = col.row()
        options.use_property_split = False
        options.prop(settings, 'view_mode', expand=True, text="PRESET")

        header = col.box()
        header.label(text="Settings")

        content = col.box()
        if not settings.is_navigation():
            content.prop(settings, 'view_'+settings.view_mode.lower())

            dims = content.row()
            dims.use_property_split = False
            dims.row(align=True).prop(settings, 'dimensions', slider=True)

        if settings.view_mode == 'PRESET':
            self.draw_view_preset(settings, left_layout, content)
        elif settings.view_mode == 'CAMERA':
            self.draw_view_camera(settings, left_layout, content)
        else:
            self.draw_view_nav(settings, left_layout, content)

        self.draw_common_settings(settings, left_layout)

        if prefs.show_beta_features:
            self.draw_live_view(settings, main_row)

    
    def draw_live_view(self, settings, main_row):
    
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
