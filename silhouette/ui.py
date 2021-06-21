from bpy.types import Panel
from . prefs import get_prefs


class VIEW3D_PT_silhouette(Panel):
    bl_label = "Silhouette"
    bl_context = "NONE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    bl_ui_units_x = 22

    #@classmethod
    #def poll(cls, context):
    #    return False

    def draw_view_preset(self, settings, left_layout, content):
        content = content.box()
        content.label(text="TARGET :", icon='TRACKER')
        content.prop(settings, 'target_type', text="Type")
        if settings.target_type == 'OBJECT':
            content.prop(settings, 'target_object', text="")
        elif settings.target_type == 'COLLECTION':
            content.prop(settings, 'target_collection', text="")

    def draw_view_camera(self, settings, left_layout, content):
        pass

    def draw_view_nav(self, settings, left_layout, content):
        content = content.box()
        content.label(text="TRANSFORM :", icon='FULLSCREEN_ENTER')
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
        header.label(text="Other Settings", icon='OPTIONS')

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
        options.scale_y = 1.5
        options.prop(settings, 'view_mode', expand=True, text="PRESET")

        header = col.box()
        header.label(text="Settings", icon='SETTINGS')

        content = col.box().column(align=True)

        view_mode = 'view_'+settings.view_mode.lower()
        if settings.view_mode == 'PRESET':
            box = content.box()
            box.label(text="VIEW :", icon='RESTRICT_VIEW_OFF')
            box.prop(settings, view_mode, text="Preset")
            self.draw_view_preset(settings, left_layout, content)
        elif settings.view_mode == 'CAMERA':
            box = content.box()
            box.label(text="VIEW :", icon='RESTRICT_VIEW_OFF')
            box.prop(settings, view_mode, text="Camera")
            self.draw_view_camera(settings, left_layout, content)
        else:
            self.draw_view_nav(settings, left_layout, content)

        if not settings.is_navigation():
            content = content.box()
            content.label(text="TRANSFORM :", icon='FULLSCREEN_ENTER')
            if settings.view_mode == 'PRESET':
                #col = content.column(align=True)
                #col.row(align=True).prop(settings, 'scaling_mode', text='Mode', expand=True)
                
                if not settings.is_adaptive():
                    content.row(align=True).prop(settings, 'dimensions', slider=True)
                else:
                    content.row(align=True).prop(settings, 'scale', slider=True)
            else:
                dims = content.row()
                dims.row(align=True).prop(settings, 'dimensions', slider=True)

        self.draw_style(left_layout, prefs.style, False)

        self.draw_common_settings(settings, left_layout)

        if prefs.show_beta_features:
            self.draw_live_view(prefs, settings, main_row)

    
    def draw_live_view(self, prefs, settings, main_row):
    
        from . liv_ops import rtlive

        right_layout = main_row.column(align=True)
        right_layout.active = True

        block_header = right_layout.box()
        block_header.label(text="Navigation Live View")
        block_header.alert = True
        block_header.label(text="BETA Feature !")
        block_header.label(text="(Recommended for sculpting)")
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
        content.scale_y = 1.1

        if not rtlive:
            content.operator('silhouette.start_live', text="Start Live Silhouette")

        else:
            content.alert = True
            content.operator('silhouette.stop_live', text="Remove Live Silhouette")
            content.alert = False

            settings_layout = content.column(align=True)
            box = settings_layout.box()
            box.label(text="Settings", icon='SETTINGS')

            box = settings_layout.box()
            #box.label(text="Settings:", icon='SETTINGS')
            box.prop(settings, 'live_scale', text="Scale")
            box.prop(settings, 'live_alignment', text="Alignment")

            #box.prop(rt, 'color', text="Color")
            #box.prop(rt, 'bg_color', text="Background Color")
            #box.prop(rt, 'in_front', text="Show In Front")

            self.draw_style(content, prefs.live_style, True)

    def draw_style(self, layout, style, is_live_view: bool):
        style_layout = layout.column(align=True)
        style_layout.use_property_decorate = False
        style_layout.use_property_split = False

        header = style_layout.box()
        header.label(text="Style", icon='SHADERFX')

        content = style_layout.box().column(align=True)
        
        content.row().prop(style, "color")
        row = content.row(align=True)
        row.prop(style, 'show_background', text='Background')
        bgcol = row.column()
        bgcol.active = style.show_background
        bgcol.prop(style, 'bg_color', text='')

        if not is_live_view:
            row = content.row(align=True)
            row.prop(style, 'show_view_name', text='View Name')
            bgcol = row.column()
            bgcol.active = style.show_view_name
            bgcol.prop(style, 'text_color', text='')

        content.row().prop(style, "opacity", slider=True)

        row = content.row()
        row.prop(style, 'show_in_front')
