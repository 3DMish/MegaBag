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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../");

from bpy_sys import *;

def draw_properties(self, context, lc_main):
    lc_scene = context.scene;
    obj = context.object;
    
    lc_box = lc_main.box().column(align = True);
    
    lc_label_row = lc_box.row(align = True);
    lc_icon_1 = "DOWNARROW_HLT" if (ver_more(3,0,0)) else "TRIA_DOWN";
    lc_icon_2 = "RIGHTARROW" if (ver_more(3,0,0)) else "TRIA_RIGHT";
    lc_label_row.prop(
        context.scene, "m7a_megabag_show_keys", 
        icon=lc_icon_1 if (context.scene.m7a_megabag_show_keys) else lc_icon_2, 
        emboss=False, text="Keyframes",
    );
    lc_label_row.separator();
    lc_label_row.label(text="", icon='KEYINGSET');
    
    if (context.scene.m7a_megabag_show_keys):
        lc_box.separator();
        
        lc_main_row = lc_box.row(align = True);
        lc_main_row.operator("m7a.megabag_button", text="", icon="MEMORY" if (ver_more(3,0,0)) else "ZOOM_ALL").option = "OBJECT_MEMORY";
        lc_main_row.prop(lc_scene, "m7a_megabag_memory_keys", text = "");
        lc_main_row.operator("m7a.megabag_button", text="", icon="X").option = "CLEAR_OBJECT_MEMORY";
        
        lc_main_row = lc_box.row(align = True);
        lc_main_row.operator("m7a.megabag_button", text="Insert Keyframes", icon="KEY_HLT").option = "SET_KEYFRAMES";
        lc_main_row.operator("m7a.megabag_button", text="", icon="TRACKING_CLEAR_BACKWARDS" if (ver_more(3,0,0)) else "REW").option = "SET_KEYFRAME_BACKWARD";
        lc_main_row.operator("m7a.megabag_button", text="", icon="TRACKING_CLEAR_FORWARDS" if (ver_more(3,0,0)) else "FF").option = "SET_KEYFRAME_FORWARD";
        
