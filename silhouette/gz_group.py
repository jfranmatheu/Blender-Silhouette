from bpy.types import GizmoGroup
from bpy.props import IntProperty, BoolProperty


class VIEW3D_GGT_silhouettes(GizmoGroup):
    #bl_idname = 'gizmogroup.dynamic_picker'
    bl_label = "GizmoGroup: Dynamic Picker "
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE', 'SHOW_MODAL_ALL'}#, , 'DEPTH_3D', 'SELECT'} #, 'TOOL_INIT'}

    radius : IntProperty(default=80, name="Radius")
    max_bone_count : IntProperty(default=12, name="Max Bones", description="Max number of pose bones to display")

    @classmethod
    def poll(cls, context):
        return context.active_object and context.mode == 'POSE'

    '''
    __slots__ = (
        "gizmos",
        "master",
        "_radius",
        '_max_bone_count'
    )
    '''

    default_op = 'gizmogroup.gizmo_tweak'

    hotkeys = (
        'LEFTMOUSE',
        'RIGHTMOUSE',
    )

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
    
    '''
    def refresh(self, context):
        pass
    '''
    
    def setup(self, context):
        print("GGT: Setup")
        
        gz = self.gizmos.new("VIEW3D_GT_dynamic_picker")
        gz.init(context)
        
        gz.color = 0, 0, 0
        gz.alpha = .5
        gz.color_highlight = 0.1, 0.1, 0.1
        gz.alpha_highlight = .8
        
        #gz.use_modal_handle_exit = True
        gz.use_operator_tool_properties = True
        gz.use_event_handle_all = False
        gz.use_draw_modal = True
        
        gz.scale_basis = 1
        
        self.master = gz
