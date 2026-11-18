import bpy
from bpy.types import SpaceView3D


def override(ctx):
    for window in ctx.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return {
                            'window' : window,
                            'screen' : window.screen,
                            'area' : area,
                            'region' : region
                        }
    return None

def get_area_off_dim(area, search, dim):
    for reg in area.regions:
        if reg.type == search:
            return getattr(reg, dim)

def get_area_off(area, search):
    x = 0
    y = 0
    for reg in area.regions:
        if reg.type in search:
            if reg.type == 'TOOLS':
                x += reg.width
            elif reg.type == 'UI':
                x -= reg.width
            elif reg.type == 'TOOL_HEADER':
                y -= reg.height
            elif reg.type == 'HEADER':
                y -= reg.height
    return x, y

def get_space_types(ctx):
    return {area.type for area in ctx.window.screen.areas}


class DrawContext:
    def __init__(self, context):
        self.context = context
        self.area = context.area
        self.region = context.region
        self.workspace = context.workspace
        self.scene = context.scene
        self.handler = None
        self.kwargs = None

    def set_handler(self, callback, on_error, data, *args, **kwargs):
        self.callback = callback
        self.data = data
        self.on_error = on_error
        self.args = args if args else None
        self.kwargs = kwargs if kwargs else None
        self.handler = SpaceView3D.draw_handler_add(self.draw, (), 'WINDOW', 'POST_PIXEL')

    def check_context(self):
        ''' Devuelve False si no hay que dibujar en este area. '''
        if not self.context:
            self.stop(True)
            return False
        # Cada viewport llama al handler, solo dibujamos en el nuestro.
        if bpy.context.area != self.area:
            return False
        if self.scene != bpy.context.scene:
            self.stop(True)
            return False
        if self.context.workspace != self.workspace:
            self.stop(True)
            return False
        return True

    def stop(self, forced=False):
        if hasattr(self, 'handler'):
            SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
            del self.handler
        if not forced:
            self.area.tag_redraw()
        else:
            self.on_error()

    def draw(self):
        if not self.check_context():
            return
        self.callback(self, self.data, self.args, self.kwargs)
