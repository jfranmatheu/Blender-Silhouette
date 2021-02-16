from bpy.types import GizmoGroup


class VIEW3D_GGT_silhouettes(GizmoGroup):
    bl_label = "GizmoGroup: Silhouettes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE', 'SHOW_MODAL_ALL', 'DEPTH_3D'}#, 'SELECT'} #, 'TOOL_INIT'}

    __slots__ = ()

    default_op = 'gizmogroup.gizmo_tweak'

    hotkeys = (
        'LEFTMOUSE',
        'RIGHTMOUSE',
    )
    
    @classmethod
    def poll(cls, context):
        return context.active_object

    @classmethod
    def setup_keymap(cls, keyconfig):
        print("GGT: SETUP KEYMAPS")
        km = keyconfig.keymaps.get(cls.__name__, None)
        if km and km.keymap_items and len(km.keymap_items) > 1:
            print("\t* ALREADY INITIALIZED! *") # COULD BE FALSE NEGATIVE
            return km
        km = keyconfig.keymaps.new(name=cls.__name__, space_type='VIEW_3D', region_type='WINDOW')
        for key in cls.hotkeys:
            km.keymap_items.new(cls.default_op, key, 'ANY', any=True)
        return km
    
    def setup(self, context):
        print("GGT: Setup")
        
        gz = self.gizmos.new("VIEW3D_GT_silhouette")
        gz.init(context)
        
        gz.color = 0, 0, 0
        gz.alpha = .5
        gz.color_highlight = 0.1, 0.1, 0.1
        gz.alpha_highlight = .8

        gz.use_operator_tool_properties = True
        gz.use_event_handle_all = False
        gz.use_draw_modal = True
        
        gz.scale_basis = 1
        
        self.master = gz

    def refresh(self, context):
        pass
