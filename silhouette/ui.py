import bpy
from bpy.types import Panel
from . prefs import get_prefs


class VIEW3D_PT_silhouette(Panel):
    bl_label = "Silhouette"
    bl_context = "NONE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    bl_ui_units_x = 12

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
        if not settings.view_camera:
            camera = settings.get_camera(bpy.context)
            if camera:
                content.label(text=f"Using scene camera: {camera.name}", icon='INFO')
            else:
                content.alert = True
                content.label(text="No camera in the scene", icon='ERROR')
                content.alert = False

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

        left_layout = layout.column(align=True)
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

        self.draw_style(left_layout, prefs.style)

        # El auto-update de sculpt solo tiene sentido en Preset y Camera, Navigation ya se redibuja con el viewport.
        if not settings.is_navigation():
            self.draw_common_settings(settings, left_layout)

        from . support import draw_support
        draw_support(layout)


    
    def draw_style(self, layout, style):
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

        row = content.row(align=True)
        row.prop(style, 'show_view_name', text='View Name')
        bgcol = row.column()
        bgcol.active = style.show_view_name
        bgcol.prop(style, 'text_color', text='')

        content.row().prop(style, "opacity", slider=True)

        row = content.row()
        row.prop(style, 'show_in_front')
