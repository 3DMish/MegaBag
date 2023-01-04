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
    
    lc_box = lc_main.box().column(align = True);
    
    lc_label_row = lc_box.row(align = True);
    lc_icon_1 = "DOWNARROW_HLT" if (ver_more(3,0,0)) else "TRIA_DOWN";
    lc_icon_2 = "RIGHTARROW" if (ver_more(3,0,0)) else "TRIA_RIGHT";
    lc_label_row.prop(
        context.scene, "m7a_megabag_show_props", 
        icon=lc_icon_1 if (context.scene.m7a_megabag_show_props) else lc_icon_2, 
        emboss=False, text="Custom Properties",
    );
    
    if (context.scene.m7a_megabag_show_props):
        lc_label_row.separator();
        lc_label_row.menu("M7A_OBJECT_MT_ADD_Prop", text="", icon='ADD' if (ver_more(3,0,0)) else "ZOOMIN");
        lc_box.separator();
        
        if (context.object):
            data_path = 'object';
            items = list(context.object.keys());
            items.sort(); show = False;
            
            for item in items:
                if not (item == 'cycles') and not (hasattr(obj[item], "name")):
                    show = True;
                
            if not (items == []) and (items != ['cycles']) and (show):
                lc_box.label(text="Object", icon="LAYER_USED");
            
            for item in items:
                if not (item == 'cycles') and not (hasattr(obj[item], "name")):
                    lc_row = lc_box.row(align = True);
                    lc_row.prop(obj, '["%s"]' % item);
                    props = lc_row.operator("wm.properties_edit", text="", icon='PREFERENCES');
                    props.data_path = data_path;
                    if (ver_less(3,0,0)): props.property = item;
                    else: props.property_name = item;
                    props = lc_row.operator("wm.properties_remove", text="", icon='X');
                    props.data_path = data_path;
                    if (ver_less(3,0,0)): props.property = item;
                    else: props.property_name = item;
            
            data_path = 'object.data';
            items = list(context.object.data.keys());
            items.sort(); show = False;
            
            for item in items:
                if not (item == 'cycles') and not (hasattr(obj.data[item], "name")):
                    show = True;
            
            if not (items == []) and (show): lc_box.label(text="Data", icon="LAYER_USED");
            
            for item in items:
                if not (item == 'cycles') and not (hasattr(obj.data[item], "name")):
                    lc_row = lc_box.row(align = True);
                    lc_row.prop(obj.data, '["%s"]' % item);
                    props = lc_row.operator("wm.properties_edit", text="", icon='PREFERENCES');
                    props.data_path = data_path;
                    if (ver_less(3,0,0)): props.property = item;
                    else: props.property_name = item;
                    props = lc_row.operator("wm.properties_remove", text="", icon='X');
                    props.data_path = data_path;
                    if (ver_less(3,0,0)): props.property = item;
                    else: props.property_name = item;
                    
            if (obj.type == 'ARMATURE') and (context.selected_pose_bones) and (context.active_pose_bone):
                data_path = 'active_pose_bone';
                items = list(context.active_pose_bone.keys());
                items.sort(); show = False;
            
                for item in items:
                    if not (item == 'cycles') and not (hasattr(context.active_pose_bone[item], "name")):
                        show = True;
                
                if not (items == []) and (show) and (context.mode in {'POSE'}):
                    lc_box.label(text="Bone", icon="LAYER_USED");
                
                for item in items:
                    if not (item == 'cycles') and not (hasattr(context.active_pose_bone[item], "name")):
                        lc_row = lc_box.row(align = True);
                        lc_row.prop(context.active_pose_bone, '["%s"]' % item);
                        props = lc_row.operator("wm.properties_edit", text="", icon='PREFERENCES');
                        props.data_path = data_path;
                        if (ver_less(3,0,0)): props.property = item;
                        else: props.property_name = item;
                        props = lc_row.operator("wm.properties_remove", text="", icon='X');
                        props.data_path = data_path;
                        if (ver_less(3,0,0)): props.property = item;
                        else: props.property_name = item;
    else:
        lc_label_row.separator();
        lc_label_row.label(text="", icon='PROPERTIES' if (ver_more(3,0,0)) else "UI");
