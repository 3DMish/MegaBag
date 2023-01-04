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

from bpy.utils import escape_identifier;

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../");

from bpy_sys import *;

def draw_properties(self, context, lc_main):
    obj = context.object;
    
    if (context.mode in {"OBJECT"}):
        lc_row = lc_main.row(align = True);
        lc_row.operator("object.shade_smooth", icon='SHADING_RENDERED' if (ver_more(2,90,0)) else "SOLID");
        if (ver_more(3,3,0)): lc_row.operator("object.shade_smooth", icon='SHADING_RENDERED', text="").use_auto_smooth = True;
        lc_row = lc_row.row(align = True);
        lc_row.operator("object.shade_flat", icon='SHADING_WIRE' if (ver_more(2,90,0)) else "WIRE", text="" if (ver_more(3,3,0)) else "Flat");
        if (ver_more(2,90,0)): lc_row.scale_x = 0.5;
        
        lc_main.separator();
        
        lc_main.operator("object.data_transfer", icon='MOD_DATA_TRANSFER');
        
        lc_main.separator();
                
#    lc_box = lc_main.column(align = True);
#    
#    lc_label_row = lc_box.box().row(align = True);
#    lc_icon_1 = "DOWNARROW_HLT" if (ver_more(3,0,0)) else "TRIA_DOWN";
#    lc_icon_2 = "RIGHTARROW" if (ver_more(3,0,0)) else "TRIA_RIGHT";
#    lc_label_row.prop(
#        context.scene, "m7a_megabag_shape_keys", 
#        icon=lc_icon_1 if (context.scene.m7a_megabag_shape_keys) else lc_icon_2, 
#        emboss=False);
#    lc_label_row.separator();
#    lc_label_row.label(text="", icon='SHAPEKEY_DATA');
#    
#    if (context.scene.m7a_megabag_shape_keys):
#        lc_row = lc_box.row(align = True);

#        lc_row.template_list(
#            "MESH_UL_shape_keys", "", 
#            obj.data.shape_keys, "key_blocks", 
#            obj, "active_shape_key_index", rows=5
#        )

#        lc_col = lc_row.column(align = True)

#        lc_col.operator("object.shape_key_add", icon='ADD' if (ver_more(3,0,0)) else 'ZOOMIN', text="").from_mix = False;
#        lc_col.operator("object.shape_key_remove", icon='REMOVE' if (ver_more(3,0,0)) else 'ZOOMOUT', text="").all = False;

#        lc_col.separator();

#        lc_col.menu("MESH_MT_shape_key_context_menu", icon='DOWNARROW_HLT', text="");
#        
#        lc_col.separator();
#        
#        lc_sub = lc_col.column(align = True);
#        lc_sub.operator("object.shape_key_move", icon='TRIA_UP', text="").type = 'UP';
#        lc_sub.operator("object.shape_key_move", icon='TRIA_DOWN', text="").type = 'DOWN';
#        
#        lc_box.separator();
#        
#        if (context.object.active_shape_key):
#            lc_row = lc_box.row(align = True);
#            lc_btn_row = lc_row.row(align = True);
#            lc_btn_row.prop(obj.data.shape_keys, "use_relative", toggle=True);
#            
#            if (obj.data.shape_keys.use_relative):
#                if (obj.active_shape_key_index):
#                    lc_btn_row.scale_x = 0.6;
#                    lc_row.prop(obj.data.shape_keys.key_blocks[obj.active_shape_key_index], "value");
#            else:
#                lc_btn_row.scale_x = 0.6;
#                lc_row.prop(obj.data.shape_keys, "eval_time", text="E - Time");
#            
#            lc_row.prop(obj, "use_shape_key_edit_mode", text="");
#        
