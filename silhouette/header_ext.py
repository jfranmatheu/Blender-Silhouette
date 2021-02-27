

def header_ext(self, context):
    settings = context.scene.silhouette
    #self.layout.popover('VIEW3D_PT_silhouette', icon="GHOST_ENABLED", text="")
    row = self.layout.row(align=True)
    #space = context.space_data
    #row.prop(space, 'silhouette_enabled', text="", icon="GHOST_ENABLED" if space.silhouette_enabled else "GHOST_DISABLED")
    row.prop(settings, 'enabled', text="", icon="GHOST_ENABLED" if settings.enabled else "GHOST_DISABLED")
    row.popover('VIEW3D_PT_silhouette', text="")

def register():
    from bl_ui.space_view3d import VIEW3D_HT_header as Header
    Header.append(header_ext)

def unregister():
    from bl_ui.space_view3d import VIEW3D_HT_header as Header
    Header.remove(header_ext)
