# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Silhouette",
    "author" : "J. Fran Matheu (@jfranmatheu)",
    "description" : "Quickly preview silhouettes of your mesh over the viewport from different view presets",
    "blender" : (2, 93, 0),
    "version" : (2, 1, 8),
    "location" : "3D Viewport",
    "warning" : "This 2.0 version is a rewrite from the 1.X series, you should expect quite different things",
    "category" : "Generic"
}

DEBUG = False

from . import auto_load

auto_load.init()


def register():
    from bpy.types import Scene as scn#, SpaceView3D
    from bpy.props import PointerProperty as Pointer, BoolProperty
    from . data import SILHOUETTE_SETTINGS
    #from . gz import depsgraph_post_update
    #from bpy.app.handlers import depsgraph_update_post
    #depsgraph_update_post.append(depsgraph_post_update)

    #SpaceView3D.silhouette_enabled = BoolProperty(default=False, name="Enable Silhouette", description="Toggle silhouette overlay in 3d viewport")

    auto_load.register()
    
    scn.silhouette = Pointer(type=SILHOUETTE_SETTINGS)


def unregister():
    auto_load.unregister()
    
    from bpy.types import Scene as scn#, SpaceView3D
    del scn.silhouette
    
    #del SpaceView3D.silhouette_enabled

    #from bpy.app.handlers import depsgraph_update_post
    #from . gz import depsgraph_post_update
    #depsgraph_update_post.remove(depsgraph_post_update)
