from bpy.types import Gizmo, Context, Event
from mathutils import Vector
import blf
from bpy.app import timers

from functools import partial


class VIEW3D_GT_silhouette(Gizmo):

    ''' Initialization. '''

    def setup(self) -> None:
        print("GZ: SETUP")

    def init(self, ctx: Context):
        print("GZ: INIT")


    ''' Event handle. '''

    @staticmethod
    def get_mouse_pos(evt: Event):
        return Vector((evt.mouse_region_x, evt.mouse_region_y))

    def test_select(self, ctx: Context, loc: (int, int)) -> int:
        return -1

    def invoke(self, ctx: Context, evt: Event) -> set:
        print("GZ: INVOKE", evt.type, evt.value)
        return {'FINISHED'}

    def modal(self, ctx: Context, evt: Event, tweak: str) -> set:
        print("GZ: MODAL")
        return {'FINISHED'}

    def exit(self, ctx: Context, cancel: bool) -> None:
        print("GZ: EXIT")

    def time_function(self, time: float, func: callable, *args):
        timers.register(partial(func, *args), first_interval=time) 


    ''' Drawing. '''

    def draw(self, ctx: Context) -> None:'
        pass

    def draw_select(self, ctx: Context, select_id: int) -> None:
        pass
