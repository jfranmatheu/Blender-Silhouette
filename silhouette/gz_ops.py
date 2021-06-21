from bpy.types import Operator


class VIEW3D_OT_silhouette_toggle_front(Operator):
    bl_label = "Toggle Silhouette Front"
    bl_idname = "view3d.silhouette_toggle_front"

    def execute(self, context):
        context.scene.silhouette.view_preset = 'FRONT'
        return {'FINISHED'}

class VIEW3D_OT_silhouette_toggle_side(Operator):
    bl_label = "Toggle Silhouette Side"
    bl_idname = "view3d.silhouette_toggle_side"

    def execute(self, context):
        context.scene.silhouette.view_preset = 'RIGHT'
        return {'FINISHED'}

class VIEW3D_OT_silhouette_toggle_top(Operator):
    bl_label = "Toggle Silhouette Top"
    bl_idname = "view3d.silhouette_toggle_top"

    def execute(self, context):
        context.scene.silhouette.view_preset = 'TOP'
        return {'FINISHED'}
