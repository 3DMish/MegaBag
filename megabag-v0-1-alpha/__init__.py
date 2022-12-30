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

import bpy, sys, os, inspect;

from bpy.types import AddonPreferences;
from bpy.props import EnumProperty, PointerProperty, BoolProperty;

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/data/");

from bpy_sys import *;

if (ver_less(2,80,0)): import m7a_props_v1 as m7a_props;
else: import m7a_props_v2 as m7a_props;

import m7a_modifiers, m7a_text_editor, m7a_view3d_panels, m7a_navigate, m7a_quick_pack;
import m7a_view3d_header, m7a_view3d_tool_header, m7a_dope_sheet;

bl_info = {
    "name":     "MegaBag v0.1.Alpha",
    "category": "3DMish",
    "author":   "3DMish (Mish7913)",
    "version":  (0, 1, "0-Alpha-2023.01.01-14.42"),
    "blender":  (3, 3, 0),
    "wiki_url": "https://3dmish.blogspot.com/p/megabag-en.html",
    "warning":  "It's an alpha version.",
    "description": "MegaBag - it's a mega pack of different stuff...",
}

def register():
    m7a_props.register();
    
    if (bpy_preferences("addons", "megabag")):
        if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "view3d_update")):
            m7a_view3d_header.register();
            
            if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_update):
                
                if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "view3d_tools")):
                    if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_tools):
                        m7a_view3d_panels.register();
                     
                if (ver_more(2,80,0)): 
                    if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "view3d_tool_header")):
                        if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_tool_header):
                            m7a_view3d_tool_header.register();
                        
                if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "view3d_quick_pack")):
                    if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_quick_pack):
                        m7a_quick_pack.register();
                
        if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "text_editor_update")):
            if (bpy_preferences("addons", "megabag").m7a_megabag_props.text_editor_update):
                m7a_text_editor.register();
                
        if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "modifiers_update")):
            if (bpy_preferences("addons", "megabag").m7a_megabag_props.modifiers_update):
                m7a_modifiers.register();
              
        if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "dope_sheet_update")):
            m7a_dope_sheet.register();
    
    m7a_navigate.register();

def unregister():
    m7a_navigate.unregister();    m7a_view3d_header.unregister(); m7a_view3d_panels.unregister();
    m7a_text_editor.unregister(); m7a_modifiers.unregister();
    if (ver_more(2,80,0)): m7a_view3d_tool_header.unregister();
    m7a_quick_pack.unregister();
    
    if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "dope_sheet_update")):
        m7a_dope_sheet.unregister();
    
    m7a_props.unregister();
    
if __name__ == "__main__": register();
