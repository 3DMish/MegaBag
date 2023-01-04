#!/usr/bin/env python -------------------------------- -*- coding: utf-8 -*-#
#                      2023 3DMish <Mish7913@gmail.com>                     #

# -----              ##### BEGIN GPL LICENSE BLOCK #####              ----- #
#                                                                           #
#  This  program  is  free  software;   you  can  redistribute  it  and/or  #
#  modify  it  under  the  terms  of   the   GNU  General  Public  License  #
#  as  published  by  the  Free  Software  Foundation;  either  version  2  #
#  of the License, or (at your option) any later version.                   #
#                                                                           #
#  This program  is  distributed  in the hope  that  it  will  be  useful,  #
#  but  WITHOUT  ANY  WARRANTY;  without  even  the  implied  warranty  of  #
#  MERCHANTABILITY  or  FITNESS   FOR  A  PARTICULAR  PURPOSE.    See  the  #
#  GNU General Public License for more details.                             #
#                                                                           #
#  You  should  have  received  a  copy  of the GNU General Public License  #
#  along with this program; if not, write to the Free Software Foundation,  #
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.       #
#                                                                           #
# -----               ##### END GPL LICENSE BLOCK #####               ----- #

import bpy, sys, os;

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/");

from bpy_sys import *;
from bpy.types import Panel, Menu;

class M7A_VIEW3D_HT_Navigate(Panel):
    bl_space_type  = 'VIEW_3D';
    bl_region_type = 'TOOLS'; # ('WINDOW', 'HEADER', 'CHANNELS', 'TEMPORARY', 'UI', 'TOOLS', 'TOOL_PROPS', 'PREVIEW');
    bl_category    = "Navigate Gizmos";
    bl_label       = "Navigate Gizmos";

    @classmethod
    def poll(cls, context):
        if (bpy_preferences("addons", "megabag")):
            if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_navigate) and \
                (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_update):
                return True;
            else: return False;
        else: return False;
    
    def draw(self, context):
        lc_main = self.layout.column(align = False);
    
        lc_cont = lc_split_row(lc_main, 140);
        lc_cont.operator("view3d.rotate", text="Rotate");
        lc_cont.operator("view3d.move",   text="Pan");
        lc_cont.operator("view3d.zoom",   text="Zoom");

classes = (
    M7A_VIEW3D_HT_Navigate,
);

def register():
    global bl_conf;
    
    if (ver_less(2,79,5)):
        for cls in classes: bpy.utils.register_class(cls);

def unregister():
    global bl_conf;
    
    if (ver_less(2,79,5)):
        for cls in classes: bpy.utils.unregister_class(cls);
