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

from bpy.types import Header, Menu, PropertyGroup;
from bpy.props import BoolProperty, PointerProperty;

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/");

from bpy_sys import *;

if (ver_more(3,0,0)):
    from bl_ui.space_time import TIME_MT_editor_menus, TIME_HT_editor_buttons;
    from bl_ui.space_dopesheet import DOPESHEET_MT_editor_menus, DOPESHEET_HT_editor_buttons;

bl_conf = {
    "DOPESHEET_HT_header": None,
}

class DOPESHEET_HT_header(Header):
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'HEADER'
    
    def draw(self, context):        
        lc_space_data = context.space_data;
        lc_tool_settings = context.tool_settings;
        a_obj = context.active_object;
        
        lc_main = self.layout.row(align = True);
        
        lc_main.template_header();
        lc_main.separator();
        
        if (lc_space_data.mode == 'TIMELINE'):            
            lc_row = lc_main.row(align = False);
            TIME_MT_editor_menus.draw_collapsible(context, lc_row);
            TIME_HT_editor_buttons.draw_header(context, lc_row);
        else:
            lc_row = lc_main.row(align = True);
            lc_row.prop(lc_space_data, "ui_mode", text="");
                
            lc_row.separator();
                
            if (lc_space_data.mode == 'GPENCIL'):
                if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "dope_compact_menu")):
                    if (bpy_preferences("addons", "megabag").m7a_megabag_props.dope_compact_menu == True):
                        lc_row.menu("M7A_DOPE_SHEET_MT_Menu");
                    else: DOPESHEET_MT_editor_menus.draw_collapsible(context, lc_row);
                else: DOPESHEET_MT_editor_menus.draw_collapsible(context, lc_row);
                
                lc_main.separator_spacer();
                
                selected = lc_space_data.dopesheet.show_only_selected;
                lc_enable = selected and a_obj is not None and a_obj.type == 'GPENCIL';

                lc_row = lc_main.row(align=True);
                lc_row.enabled = lc_enable;
                lc_row.operator("gpencil.layer_add", icon='ADD', text="");
                lc_row.operator("gpencil.layer_remove", icon='REMOVE', text="");
                lc_row.menu("GPENCIL_MT_layer_context_menu", icon='DOWNARROW_HLT', text="");
                
                lc_main.separator();

                lc_row = lc_main.row(align=True);
                lc_row.enabled = lc_enable;
                lc_row.operator("gpencil.layer_move", icon='TRIA_UP', text="").type = 'UP';
                lc_row.operator("gpencil.layer_move", icon='TRIA_DOWN', text="").type = 'DOWN';
                
                lc_main.separator();
                
                lc_row = lc_main.row(align=True);
                lc_row.enabled = lc_enable;
                lc_row.operator("gpencil.layer_isolate", icon='RESTRICT_VIEW_ON', text="").affect_visibility = True;
                lc_row.operator("gpencil.layer_isolate", icon='LOCKED', text="").affect_visibility = False;

                lc_row.separator_spacer();
                
                lc_row.operator("action.keyframe_insert", text="", icon='KEYFRAME_HLT');
                lc_row.operator("gpencil.frame_duplicate", text="", icon='DUPLICATE');
                lc_row.operator("action.duplicate_move", text="", icon_value=lc_icon("DUP_MOVE"));
                lc_row.operator("action.delete", text="", icon='TRASH');
                lc_row.separator();
                lc_row.operator("action.keyframe_type", text="", icon='KEYTYPE_KEYFRAME_VEC');
                                
                if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "dope_play_pause")):
                    if (bpy_preferences("addons", "megabag").m7a_megabag_props.dope_play_pause == True):
                        lc_main.separator_spacer();
                        DRAW_PLAY_PAUSE_Panel(context, lc_main, lc_tool_settings);
                
                lc_main.separator_spacer();
                        
                lc_main.prop(lc_space_data.dopesheet, "show_only_selected", text="");
                lc_main.prop(lc_space_data.dopesheet, "show_hidden", text="");
                
                lc_main.separator();
                
                lc_row_btn = lc_main.row(align = True);
                lc_row_btn.active = lc_tool_settings.use_proportional_action;
                lc_row_btn.prop(lc_tool_settings, "use_proportional_action", text="", icon_only=True);
                lc_row_btn.prop(lc_tool_settings, "proportional_edit_falloff", text="", icon_only=True);
                
                lc_main.separator();

                if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "dope_play_pause")):
                    if (bpy_preferences("addons", "megabag").m7a_megabag_props.dope_play_pause == True):
                        
                        lc_row_btn = lc_main.row(align = True);
                        if context.scene.show_subframe: lc_row_btn.prop(context.scene, "frame_float", text="");
                        else: lc_row_btn.prop(context.scene, "frame_current", text="");
                        lc_width(lc_row_btn, 4);
                        
                        lc_main.separator();

                        lc_main.prop(context.scene, "use_preview_range", text="", toggle=True)
                        
                        lc_row_btn = lc_main.row(align = True);
                        if not context.scene.use_preview_range:
                            lc_row_btn.prop(context.scene, "frame_start", text="Start");
                            lc_row_btn.prop(context.scene, "frame_end", text="End");
                        else:
                            lc_row_btn.prop(context.scene, "frame_preview_start", text="Start");
                            lc_row_btn.prop(context.scene, "frame_preview_end", text="End");
                        lc_width(lc_row_btn, 8);

                        lc_main.separator();
                        
                lc_main.popover(panel="DOPESHEET_PT_filters", text="", icon='FILTER');
            else:
                if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "dope_compact_menu")):
                    if (bpy_preferences("addons", "megabag").m7a_megabag_props.dope_compact_menu == True):
                        lc_main.menu("M7A_DOPE_SHEET_MT_Menu");
                    else: DOPESHEET_MT_editor_menus.draw_collapsible(context, lc_main);
                else: DOPESHEET_MT_editor_menus.draw_collapsible(context, lc_main);
                
                lc_main.separator();
                
                if (lc_space_data.mode in {'DOPESHEET'}): 
                    if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "dope_play_pause")):
                        lc_main.separator_spacer();
                            
                        lc_main.operator("action.keyframe_insert", text="", icon='KEYFRAME_HLT');
                        lc_main.operator("action.duplicate_move", text="", icon_value=lc_icon("DUP_MOVE"));
                        lc_main.operator("action.delete", text="", icon='TRASH');
                            
                        lc_main.separator();
                            
                        lc_main.operator("action.keyframe_type", text="", icon='KEYTYPE_KEYFRAME_VEC');
                
                        if (bpy_preferences("addons", "megabag").m7a_megabag_props.dope_play_pause == True):
                            lc_main.separator();
                            
                            DRAW_PLAY_PAUSE_Panel(context, lc_main, lc_tool_settings);
                            
                DOPESHEET_HT_editor_buttons.draw_header(context, lc_main);
                
def DRAW_PLAY_PAUSE_Panel(context, lc_main, lc_tool_settings):
    lc_main.prop(lc_tool_settings, "use_keyframe_insert_auto", text="", toggle=True);
    lc_main.separator();
    lc_main.operator("screen.frame_jump", text="", icon='REW').end = False;
    lc_main.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False;
    if not (context.screen.is_animation_playing):
        lc_main.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True;
        lc_main.operator("screen.animation_play", text="", icon='PLAY');
    else:
        lc_main.scale_x = 2;
        lc_main.operator("screen.animation_play", text="", icon='PAUSE');
        lc_main.scale_x = 1;
    lc_main.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
    lc_main.operator("screen.frame_jump", text="", icon='FF').end = True
                
class M7A_DOPE_SHEET_MT_Menu(Menu):
    bl_idname      = 'M7A_DOPE_SHEET_MT_Menu';
    bl_label       = 'Menu';
    bl_description = 'Dope Sheet Menu';
    
    @staticmethod
    def draw(self, context):
        lc_space_data = context.space_data;
        lc_main = self.layout.column();

        lc_main.menu("DOPESHEET_MT_view")
        lc_main.menu("DOPESHEET_MT_select")
        if (lc_space_data.show_markers): lc_main.menu("DOPESHEET_MT_marker")

        if (lc_space_data.mode == 'DOPESHEET') or \
            (lc_space_data.mode == 'ACTION' and lc_space_data.action is not None):
            lc_main.menu("DOPESHEET_MT_channel")
        elif lc_space_data.mode == 'GPENCIL':
            lc_main.menu("DOPESHEET_MT_gpencil_channel")

        if (lc_space_data.mode == 'GPENCIL'): lc_main.menu("DOPESHEET_MT_gpencil_key");
        else: lc_main.menu("DOPESHEET_MT_key");

classes = (
    DOPESHEET_HT_header, M7A_DOPE_SHEET_MT_Menu,
);

def register():
    global bl_conf;
    
    r_unregister_class(bl_conf, "DOPESHEET_HT_header");
    
    for cls in classes:
        try: bpy.utils.register_class(cls);
        except: pass
    
def unregister():
    global bl_conf;
    
    for cls in classes:
        try: bpy.utils.unregister_class(cls);
        except: pass
    
    r_register_class(bl_conf, "DOPESHEET_HT_header");
