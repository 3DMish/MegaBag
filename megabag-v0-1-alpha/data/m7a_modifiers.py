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
from bpy.props import EnumProperty;
from bpy.types import Panel, Menu, WindowManager as lc_manager;

if ver_less(3,0,0): import m7a_templates;

bl_conf = {
    "DATA_PT_modifiers": None,
    "DATA_PT_gpencil_modifiers": None,
}

class DATA_PT_modifiers(Panel):
    bl_space_type  = 'PROPERTIES';
    bl_region_type = 'WINDOW';
    bl_label       = "M7A Modifiers";
    bl_context     = "modifier";
    bl_options     = {'HIDE_HEADER'};

    def draw(self, context):
        lc_main = self.layout.column(align = False);
        lc_type = context.object.type;
        m7a_megabag_props = bpy_preferences("addons", "megabag").m7a_megabag_props;
        
        lc_row = lc_main.row(align = True);
        if (lc_type not in {"GPENCIL"}): lc_row.operator_menu_enum("object.modifier_add", "type");
        else: lc_row.operator_menu_enum("object.gpencil_modifier_add", "type");
        
        if (m7a_megabag_props.modifiers_options):
            lc_row_btn = lc_row.row(align = True);
            lc_row_btn.menu("M7A_DATA_MT_MOD_options", icon="COLLAPSEMENU", text="Options");
            lc_width(lc_row_btn, 6);
        
        if (lc_type in {"MESH", "CURVE"}):
            if (ver_more(3,0,0)) and (m7a_megabag_props.modifiers_m7a_pack):
                lc_row = lc_main.row(align = True);
                lc_row.menu("M7A_DATA_MT_MOD_menu");
                lc_row.menu("M7A_DATA_MT_MOD_pref", text="", icon="TOOL_SETTINGS");
        
        gp_len = len(context.object.grease_pencil_modifiers) if (ver_more(3,0,0)) else 10;
        if (len(context.object.modifiers) < 1) and (gp_len < 1):
            lc_main.separator();
            lc_main_box = lc_main.row();
            lc_main_box.alignment = "CENTER";
            lc_main_box.label(text="Object don't have a modifiers");
        
        if (ver_more(2,90,0)):
            if (lc_type not in {"GPENCIL"}): lc_main.template_modifiers();
            else: lc_main.template_grease_pencil_modifiers();
        else: lc_main.separator(); m7a_templates.modifiers(lc_main, context);

class M7A_DATA_MT_MOD_options(Menu):
    bl_idname = 'M7A_DATA_MT_MOD_options';
    bl_label = "Modifier's Options";
    bl_description = '';
        
    @staticmethod
    def draw(self, context):
        lc_main = self.layout.column(align = False);
        
        lc_pic = "FILE_TICK" if (ver_less(2,90,0)) else "CHECKMARK";
        lc_btn = lc_main.operator('m7a.megabag_button', icon=lc_pic, text="Apply All");
        lc_btn.option = "MOD_APPLY_ALL";
        lc_btn_description(lc_btn, "Apply all modifiers visible in viewport");
        
        lc_main.separator();
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon='RESTRICT_VIEW_OFF', text="Viewport: All ON");
        lc_btn.option = "MOD_VIEWPORT_ON";
        lc_btn_description(lc_btn, "Turn-ON visible in viewport all modifiers");
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon='RESTRICT_VIEW_ON', text="Viewport: All OFF");
        lc_btn.option = "MOD_VIEWPORT_OFF";
        lc_btn_description(lc_btn, "Turn-OFF visible in viewport all modifiers");
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon='RESTRICT_SELECT_OFF', text="Viewport: All Toggle");
        lc_btn.option = "MOD_VIEWPORT_TOGGLE";
        lc_btn_description(lc_btn, "Toggle visible in viewport all modifiers");
        
        lc_main.separator();
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon='RESTRICT_RENDER_OFF', text="Render: All ON");
        lc_btn.option = "MOD_RENDER_ON";
        lc_btn_description(lc_btn, "Turn-ON visible for render all modifiers");
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon='RESTRICT_RENDER_ON', text="Render: All OFF");
        lc_btn.option = "MOD_RENDER_OFF";
        lc_btn_description(lc_btn, "Turn-OFF visible for render all modifiers");
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon='RESTRICT_SELECT_OFF', text="Render: All Toggle");
        lc_btn.option = "MOD_RENDER_TOGGLE";
        lc_btn_description(lc_btn, "Toggle visible for render all modifiers");
        
        lc_main.separator();
        
        lc_pic = 'TRASH' if (ver_more(2,90,0)) else 'X';
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon=lc_pic, text="Remove: Viewport OFF");
        lc_btn.option = "MOD_REMOVE_VIEW";
        lc_btn_description(lc_btn, "Delete all dasabled viewport modifiers");
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon=lc_pic, text="Remove: Render OFF");
        lc_btn.option = "MOD_REMOVE_RENDER";
        lc_btn_description(lc_btn, "Delete all dasabled render modifiers");
        
        lc_main.separator();
        
        lc_btn = lc_main.operator('m7a.megabag_button', icon=lc_pic, text="Remove: All");
        lc_btn.option = "MOD_REMOVE_ALL";
        lc_btn_description(lc_btn, "Delete all modifiers");

class M7A_DATA_PT_Modifiers_Menu(Menu):
    bl_idname = 'M7A_DATA_MT_MOD_menu';
    bl_label = 'Add M7A Modifier';
    bl_description = 'Add M7A Modifier';
    
    @staticmethod
    def draw(self, context):
        lc_main_row = self.layout.row(align = False);
        
        if (context.object.type == "MESH"):
            lc_col_1 = lc_main_row.column(align = True);
            lc_col_1.label(text="Generate");
            lc_col_1.separator();
            
            lc_btn = lc_col_1.operator('m7a.megabag_button', icon='MOD_ARRAY', text="Vector Array");
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Vector Array";
            lc_btn_description(lc_btn, "Add modifier 'Vector Array' based on geometry nodes");
            
            lc_btn = lc_col_1.operator('m7a.megabag_button', text="Circle Array", icon_value=lc_icon("CIRCLE_ARRAY"));
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Circle Array";
            lc_btn_description(lc_btn, "Add modifier 'Circle Array' based on geometry nodes");
            
            lc_btn = lc_col_1.operator('m7a.megabag_button', text="Flower", icon_value=lc_icon("FLOWER"));
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Flower";
            lc_btn_description(lc_btn, "Add modifier 'Flower' based on geometry nodes");
            
            lc_btn = lc_col_1.operator('m7a.megabag_button', text="Beads Wireframe", icon_value=lc_icon("BEADS_WIREFRAME"));
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Beads Wireframe";
            lc_btn_description(lc_btn, "Add modifier 'Beads Wireframe' based on geometry nodes");
            
            lc_col_2 = lc_main_row.column(align = True);
            lc_col_2.label(text="Create");
            lc_col_2.separator();
            
            lc_btn = lc_col_2.operator('m7a.megabag_button', icon='FREEZE', text="Icing");
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Icing";
            lc_btn_description(lc_btn, "Add modifier 'Icing' based on geometry nodes");
            
            lc_btn = lc_col_2.operator('m7a.megabag_button', text="Frosting", icon_value=lc_icon("FROSTING"));
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Frosting";
            lc_btn_description(lc_btn, "Add modifier 'Frosting' based on geometry nodes");
            
            lc_btn = lc_col_2.operator('m7a.megabag_button', text="Sprinkles", icon_value=lc_icon("SPRINKLES"));
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Sprinkles";
            lc_btn_description(lc_btn, "Add modifier 'Sprinkles' based on geometry nodes");
            
            lc_btn = lc_col_2.operator('m7a.megabag_button', text="Cherry on Top", icon_value=lc_icon("CHERRY"));
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Cherry on Top";
            lc_btn_description(lc_btn, "Add modifier 'Cherry on Top' based on geometry nodes");
            
            #lc_btn = lc_col_2.operator('m7a.megabag_button', icon_value=lc_icon["ELECTRIC"], text="Electricity Lightning (!)");
            #lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "";
            #lc_btn_description(lc_btn, "Add modifier 'Electricity Lightning' based on geometry nodes");

            lc_col_3 = lc_main_row.column(align = True);
            lc_col_3.label(text="Deform");
            lc_col_3.separator();
            
            lc_btn = lc_col_3.operator('m7a.megabag_button', icon='MOD_NOISE', text="Noise");
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Mesh Noise";
            lc_btn_description(lc_btn, "Add modifier 'Noise' based on geometry nodes");
            
        elif (context.object.type == "CURVE"):
            lc_col_1 = lc_main_row.column(align = True);
            lc_col_1.label(text="Generate");
            lc_col_1.separator();
            
            lc_btn = lc_col_1.operator('m7a.megabag_button', text="Electricity Arch", icon_value=lc_icon("ELECTRIC"));
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Electricity Arch";
            lc_btn_description(lc_btn, "Add modifier 'Electricity Arch' based on geometry nodes");
            
            #lc_btn = lc_col_1.operator('m7a.megabag_button', icon_value=lc_icon["LIGHTNING"], text="Lightning (!)");
            #lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "";
            #lc_btn_description(lc_btn, "Lightning' based on geometry nodes");
            
            lc_col_2 = lc_main_row.column(align = True);
            lc_col_2.label(text="Create");
            lc_col_2.separator();
            
            lc_btn = lc_col_2.operator('m7a.megabag_button', icon='LINKED', text="Chain");
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Chain";
            lc_btn_description(lc_btn, "Add modifier 'Chain' based on geometry nodes");
            
            lc_col_3 = lc_main_row.column(align = True);
            lc_col_3.label(text="Deform");
            lc_col_3.separator();
            
            lc_btn = lc_col_3.operator('m7a.megabag_button', icon='MOD_NOISE', text="Noise");
            lc_btn.option = "ADD_M7A_MODIFIER"; lc_btn.data = "M7A GeoNodes Curve Noise";
            lc_btn_description(lc_btn, "Add modifier 'Noise' based on geometry nodes");

class M7A_DATA_PT_MOD_Preferences(Menu):
    bl_idname = 'M7A_DATA_MT_MOD_pref';
    bl_label = 'M7A Settings';
    bl_description = 'M7A Modifiers Settings';
        
    @staticmethod
    def draw(self, context):
        lc_main = self.layout.column(align = True);
        lc_wm = context.window_manager;
        
        lc_btn = lc_main.operator(
            'm7a.megabag_button', icon='RADIOBUT_ON' if (lc_wm.m7a_howmod_add == "use_exist") else 'RADIOBUT_OFF', 
            text="If GeoNodes Exist - Use It");
        lc_btn.option = "MOD_ADD_AS_EXIST"; lc_btn.data = "ON";
        lc_btn_description(lc_btn, "Use exist, If not exist create new");
        
        lc_btn = lc_main.operator(
            'm7a.megabag_button', icon='RADIOBUT_ON' if (lc_wm.m7a_howmod_add != "use_exist") else 'RADIOBUT_OFF', 
            text="Always create new GeoNodes");
        lc_btn.option = "MOD_ADD_AS_EXIST"; lc_btn.data = "OFF";
        lc_btn_description(lc_btn, "Always create new GeoNodes");

classes = (
    DATA_PT_modifiers, M7A_DATA_MT_MOD_options, M7A_DATA_PT_Modifiers_Menu, M7A_DATA_PT_MOD_Preferences,
);

def register():
    global bl_conf;
    
    r_unregister_class(bl_conf, "DATA_PT_modifiers");
    r_unregister_class(bl_conf, "DATA_PT_gpencil_modifiers");
    
    lc_manager.m7a_howmod_add = EnumProperty(
        name="How add M7A Modifier",
        description="How to add new m7a modifier, always create new geonodes, or if exist use it",
        items=[
            ("use_exist", "If exist use it", "Use exist, if not exist create new"), 
            ("always_new", "Always new", "Always add as new"),
        ],
    );
        
    for cls in classes:
        try: bpy.utils.register_class(cls);
        except: pass

def unregister():
    global bl_conf;
    
    for cls in classes:
        try: bpy.utils.unregister_class(cls);
        except: pass
    
    r_remove_attr(lc_manager, "m7a_howmod_add");
    
    r_register_class(bl_conf, "DATA_PT_modifiers");
    r_register_class(bl_conf, "DATA_PT_gpencil_modifiers");
