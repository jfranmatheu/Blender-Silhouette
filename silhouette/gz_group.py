from bpy.types import GizmoGroup as SILUETAS
from . gz import VIEW3D_GT_silhouette
from . import DEBUG


class VIEW3D_GGT_silhouettes(SILUETAS):
    bl_label = "GizmoGroup: Silhouettes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE', 'SHOW_MODAL_ALL'} #, 'TOOL_INIT'}

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            if VIEW3D_GT_silhouette.stop_draw_handler(): # HACK.
                context.region.tag_redraw()
            return False
        if context.scene.silhouette.is_preset() and context.active_object.type not in {'MESH', 'CURVE', 'ARMATURE'}:
            if VIEW3D_GT_silhouette.stop_draw_handler(): # HACK.
                context.region.tag_redraw()
            return False
        if not context.scene.silhouette.enabled:
        #if not context.space_data.silhouette_enabled:
            if VIEW3D_GT_silhouette.stop_draw_handler(): # HACK.
                context.region.tag_redraw()
            return False
        return True
    
    def setup(self, context):
        if DEBUG:
            print("GGT: Setup")
        
        gz = self.gizmos.new("VIEW3D_GT_silhouette")
        gz.init(context)
        gz.use_event_handle_all = False
        gz.use_draw_modal = False
        self.master = gz

    def refresh(self, context):
        #print("GGT: Refresh")
        self.master.refresh(context)


class VIEW3D_GGT_silhouettes_gizmos(SILUETAS):
    bl_label = "GizmoGroup: Silhouette's Gizmos"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE', 'DEPTH_3D'}

    @classmethod
    def poll(cls, context):
        return context.scene.silhouette.enabled and context.scene.silhouette.is_preset() and VIEW3D_GT_silhouette._draw_handler_instance
    
    def setup(self, context):
        if DEBUG:
            print("GGT: Setup")

        # Gizmo. Front.
        gz = self.gizmos.new("GIZMO_GT_button_2d")
        gz.target_set_operator("view3d.silhouette_toggle_front")
        gz.icon = 'AXIS_FRONT'
        gz.draw_options = {'BACKDROP', 'OUTLINE'}
        gz.alpha = .8
        gz.color = 79/255, 98/255, 47/255
        gz.color_highlight = 128/255, 200/255, 17/255
        gz.alpha_highlight = 0.8
        gz.scale_basis = 12
        gz.use_event_handle_all = False
        gz.use_draw_modal = False
        gz.use_grab_cursor = False
        gz.use_draw_hover = False
        self.gizmo_front = gz

        # Gizmo. Side.
        gz = self.gizmos.new("GIZMO_GT_button_2d")
        gz.target_set_operator("view3d.silhouette_toggle_side")
        gz.icon = 'AXIS_SIDE'
        gz.draw_options = {'BACKDROP', 'OUTLINE'}
        gz.alpha = .8
        gz.color = 107/255, 59/255, 65/255
        gz.color_highlight = 234/255, 55/255, 81/255
        gz.alpha_highlight = 0.8
        gz.scale_basis = 12
        gz.use_event_handle_all = False
        gz.use_draw_modal = False
        gz.use_grab_cursor = False
        gz.use_draw_hover = False
        self.gizmo_side = gz

        # Gizmo. Top.
        gz = self.gizmos.new("GIZMO_GT_button_2d")
        gz.target_set_operator("view3d.silhouette_toggle_top")
        gz.icon = 'AXIS_TOP'
        gz.draw_options = {'BACKDROP', 'OUTLINE'}
        gz.alpha = .8
        gz.color = 56/255, 80/255, 107/255
        gz.color_highlight = 46/255, 133/255, 232/255
        gz.alpha_highlight = 0.8
        gz.scale_basis = 12
        gz.use_event_handle_all = False
        gz.use_draw_modal = False
        gz.use_grab_cursor = False
        gz.use_draw_hover = False
        self.gizmo_top = gz

    def draw_prepare(self, context):
        silhouette = context.scene.silhouette
        width = silhouette.dimensions[0]

        self.gizmo_top.matrix_basis[0][3]   = 50 + width + 16
        self.gizmo_top.matrix_basis[1][3]   = 50 + 16

        self.gizmo_side.matrix_basis[0][3]  = 50 + width + 16
        self.gizmo_side.matrix_basis[1][3]  = 50 + 46

        self.gizmo_front.matrix_basis[0][3] = 50 + width + 16
        self.gizmo_front.matrix_basis[1][3] = 50 + 76

    def refresh(self, context):
        silhouette = context.scene.silhouette
        width = silhouette.dimensions[0]

        self.gizmo_top.matrix_basis[0][3]   = 50 + width + 16
        self.gizmo_top.matrix_basis[1][3]   = 50 + 16

        self.gizmo_side.matrix_basis[0][3]  = 50 + width + 16
        self.gizmo_side.matrix_basis[1][3]  = 50 + 46

        self.gizmo_front.matrix_basis[0][3] = 50 + width + 16
        self.gizmo_front.matrix_basis[1][3] = 50 + 76
