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

import bpy, sys, os, inspect, math;

from bpy.types import Panel, Menu, Scene;
from bpy.props import StringProperty, BoolProperty;

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/");

from bpy_sys import *;

bl_conf = {
    "ICONS": bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys(),
    "HISTORY": [],
    "SELECTED": "",
    "TEXT_PT_find": None,
    "TEXT_PT_properties": None,
    "TEXT_HT_header": None,
    "TEXT_HT_footer": None,
}

class M7A_TEXT_PT_Text(Panel):
    bl_idname      = 'M7A_TEXT_PT_Text';
    bl_space_type  = 'TEXT_EDITOR';
    bl_region_type = 'UI';
    bl_category    = "Text";
    bl_label       = "Text";
    
    def draw(self, context):
        lc_main = self.layout.column(align = False);
        
        lc_row = lc_main.row(align=True);
        lc_row.operator("text.cut", icon="PASTEFLIPUP");
        lc_row.operator("text.copy", icon="COPYDOWN");
        lc_row.operator("text.paste", icon="PASTEDOWN");
        
        lc_main.separator();
            
        lc_row = lc_main.row(align=True);
        lc_row.label(text="Line(s):");
        lc_pic = "SORT_DESC" if (ver_more(2,90,0)) else "TRIA_UP_BAR" if (ver_more(2,79,0)) else "MOVE_UP_VEC";
        lc_row.operator("text.move_lines", icon=lc_pic, text="").direction = "UP";
        
        lc_pic = "SORT_ASC" if (ver_more(2,90,0)) else "TRIA_DOWN_BAR" if (ver_more(2,79,0)) else "MOVE_DOWN_VEC";
        lc_row.operator("text.move_lines", icon=lc_pic, text="").direction = "DOWN";
        
        lc_pic = "SEQ_STRIP_DUPLICATE" if (ver_more(2,90,0)) else "MOD_ARRAY";
        lc_row.operator("text.duplicate_line", icon=lc_pic, text="");
        
        lc_pic = "TRACKING_BACKWARDS" if (ver_more(2,90,0)) else "LINENUMBERS_ON";
        lc_row.operator("text.line_break", icon=lc_pic, text="Enter");
        
        lc_row = lc_main.row(align=True);
        lc_row.label(text="Move Caret:" if (ver_more(2,90,0)) else "Caret:");
        lc_row.operator("text.move", icon="BACK", text="").type='PREVIOUS_CHARACTER';
        lc_row.operator("text.move", icon="FORWARD", text="").type='NEXT_CHARACTER';
        lc_row.operator("text.jump", icon="DECORATE_DRIVER" if (ver_more(2,90,0)) else "LOOP_FORWARDS", text="");

class M7A_TEXT_PT_find(Panel):
    bl_parent_id   = "M7A_TEXT_PT_Text";
    bl_space_type  = 'TEXT_EDITOR';
    bl_region_type = 'UI';
    bl_category    = "Text";
    bl_label       = "Find & Replace";
    
    def draw(self, context):
        lc_space_data = context.space_data;
        lc_main = self.layout.column(align = False);
        
        lc_row = lc_main.row(align = True);
        lc_row.prop(lc_space_data, "find_text", icon='VIEWZOOM', text="");
        lc_row.operator("text.find_set_selected", text="", icon='EYEDROPPER');
        lc_main.operator("text.find");
        
        lc_main.separator();
        
        lc_row = lc_main.row(align = True);
        lc_pic = 'DECORATE_OVERRIDE' if (ver_more(2,90,0)) else "FILE_REFRESH";
        lc_row.prop(lc_space_data, "replace_text", icon=lc_pic, text="");
        lc_row.operator("text.replace_set_selected", text="", icon='EYEDROPPER');
        
        lc_row = lc_main.row(align=True);
        lc_row.operator("text.replace");
        if (ver_more(2,90,0)): lc_row.operator("text.replace", text="Replace All").all = True;
        else: lc_row.operator("m7a.megabag_button", text="Replace All").option = "TEXT_REPLACE_ALL";
        
        lc_main.separator();
        
        lc_row = lc_main.row(align=True);
        lc_row.prop(lc_space_data, "use_match_case", text="Case", toggle=True)
        lc_row.prop(lc_space_data, "use_find_wrap",  text="Wrap", toggle=True)
        lc_row.prop(lc_space_data, "use_find_all",   text="All",  toggle=True)

class M7A_TEXT_PT_Info(Panel):
    bl_space_type  = 'TEXT_EDITOR';
    bl_region_type = 'UI';
    bl_category    = "Text";
    bl_label       = "Info";
    bl_options     = {'DEFAULT_CLOSED'};
    
    @classmethod
    def poll(cls, context):
        if (bpy_preferences("addons", "megabag")):
            if (bpy_preferences("addons", "megabag").m7a_megabag_props.text_editor_info) and (context.space_data.text):
                return True;
            else: return False;
        else: return False;
    
    def draw(self, context):
        lc_space_data = context.space_data;
        lc_main = self.layout.column(align=True);
        
        lc_main.box().label(text="Name: " + str(lc_space_data.text.name));
        
        lc_main.separator();
        
        lc_box = lc_main.box().column(align=True);
        
        lc_row = lc_box.row(align=True);
        lc_row.label(text="Lines: " + str(len(lc_space_data.text.lines)));
        lc_cont = lc_box if (context.region.width < 250) else lc_row;
        lc_cont.label(text="Characters: " + str(len(lc_space_data.text.as_string())));
        
        lc_row = lc_box.row(align=True);
        lc_row.label(text="Current Line: " + str(lc_space_data.text.current_line_index+1));
        lc_cont = lc_box if (context.region.width < 250) else lc_row;
        lc_cont.label(text="Current Char: " + str(lc_space_data.text.select_end_character));
        
class M7A_TEXT_PT_File(Panel):
    bl_space_type  = 'TEXT_EDITOR';
    bl_region_type = 'UI';
    bl_category    = "Text";
    bl_label       = "File";
    bl_options     = {'DEFAULT_CLOSED'};
    
    @classmethod
    def poll(cls, context):
        if (bpy_preferences("addons", "megabag")):
            if (bpy_preferences("addons", "megabag").m7a_megabag_props.text_editor_file) and (context.space_data.text):
                return True;
            else: return False;
        else: return False;
    
    def draw(self, context):
        lc_space_data = context.space_data;
        lc_main = self.layout.column(align = False);
        
        lc_main.prop(lc_space_data.text, "name");
        
        if (hasattr(lc_space_data.text, "filepath")):
            lc_row = lc_main.row(align = True);
            lc_row.prop(lc_space_data.text, "filepath", text="Path");
            lc_row.operator("text.reload", icon="RECOVER_LAST", text="");
            lc_row.operator("text.save", icon="IMPORT", text="");
            
class M7A_TEXT_PT_Icons(Panel):
    bl_space_type  = 'TEXT_EDITOR';
    bl_region_type = 'UI';
    bl_category    = "Development";
    bl_label       = "Icon Viewer";
    bl_options     = {'DEFAULT_CLOSED'};
    
    @classmethod
    def poll(cls, context):
        if (bpy_preferences("addons", "megabag")):
            if (bpy_preferences("addons", "megabag").m7a_megabag_props.text_editor_icons): return True;
            else: return False;
        else: return False;
            
    def draw(self, context):
        global bl_conf;
        
        if (ver_more(3,0,0)):
            prefs = bpy_preferences().system;
            lc_max_column = context.region.width / math.ceil((prefs.dpi * prefs.pixel_size / 72) * 20)-3;
        elif (ver_more(2,79,0)):
            prefs = bpy_preferences().system;
            lc_max_column = context.region.width / math.ceil((prefs.dpi * prefs.pixel_size / 72) * 20)-2;
        else:
            prefs = bpy_preferences().system;
            lc_max_column = context.region.width / math.ceil((prefs.dpi * 1.0 / 72) * 20)-2;
        del prefs;
        
        lc_main = self.layout.column(align = False);
        
        lc_row = lc_main.row(align = True);
        lc_row.prop(context.scene, "m7a_icons_filter", text="", icon='VIEWZOOM');
        lc_row.menu('TEXT_MT_Icons_menu', text="", icon='COLLAPSEMENU');
        
        lc_main.separator();
        
        lc_main_col = lc_main.column(align = True);
        h_icons = bl_conf["HISTORY"];
        if (h_icons != []) and (bpy.context.scene.m7a_icons_history):
            lc_box = lc_main_col.box().column(align = True);
            lc_row = lc_box.row(align = True);
            lc_row.alignment = 'CENTER';
            
            lc_h_icons = 0; len_icons = len(h_icons)-1;
            
            for i in range(0, len(bl_conf["HISTORY"])):
                if (lc_h_icons < lc_max_column):
                    lc_icon = lc_row.operator(
                        "m7a.icon_select", text="", icon=h_icons[len_icons-i], 
                        emboss=h_icons[len_icons-i] == bl_conf["SELECTED"]
                    );
                    lc_icon.option = "COPY";
                    lc_icon.icon = h_icons[len_icons-i];
                    lc_h_icons += 1;
        
        lc_box = lc_main_col.box().column(align = True);
        lc_row = lc_box.row(align = True);
        lc_row.alignment = 'LEFT';
        
        lc_column = 0; filter = True; lc_icons = 0;
                
        for i, icon in enumerate(bl_conf["ICONS"]):
            if (bpy.context.scene.m7a_icons_filter != ""):
                if (len(icon) >= len(bpy.context.scene.m7a_icons_filter)):
                    if (icon.find(bpy.context.scene.m7a_icons_filter.upper()) != -1):
                        filter = True;
                    else: filter = False;
                else: filter = False;
            else: filter = True;
        
            if (icon != "NONE") and (filter == True):
                lc_icon = lc_row.operator(
                    "m7a.icon_select", text="", icon=icon, 
                    emboss=icon == bl_conf["SELECTED"]
                );
                lc_icon.option = "COPY";
                lc_icon.icon = icon;
                
                lc_icons += 1;
                lc_column += 1;
                
                if (lc_icons < lc_max_column):
                    lc_row.alignment = 'CENTER';
                
                if (lc_column > lc_max_column):
                    lc_row = lc_box.row(align = True);
                    lc_row.alignment = 'LEFT';
                    lc_column = 0;
                    
        if (lc_icons == 0):
            lc_row.alignment = 'CENTER';
            lc_row.label(text="Sorry, I can't find any icon!");

class M7A_TEXT_MT_ICONS_Menu(Menu):
    bl_idname      = 'TEXT_MT_Icons_menu';
    bl_label       = 'Menu';
    bl_description = 'Icons Menu';
    
    @staticmethod
    def draw(self, context):
        lc_main = self.layout.column(align = True);
        lc_main.prop(context.scene, "m7a_icons_history", text="Show History", icon='VIEWZOOM');
        lc_main.operator("m7a.icon_select", text="Clear History", icon='TRASH' if (ver_more(3,0,0)) else "X").option = "CLEAR";
        
            
classes = (
    M7A_TEXT_PT_Text, M7A_TEXT_MT_ICONS_Menu, M7A_TEXT_PT_find, M7A_TEXT_PT_Info, M7A_TEXT_PT_File, M7A_TEXT_PT_Icons,
);

def register():
    global bl_conf;
    
    #r_unregister_class(bl_conf, "TEXT_HT_header", bpy.types.TEXT_HT_header);
    r_unregister_class(bl_conf, "TEXT_PT_find");
    r_unregister_class(bl_conf, "TEXT_PT_properties");
    #r_unregister_class(bl_conf, "TEXT_HT_footer", bpy.types.TEXT_HT_footer);
    
    if (ver_more(2,79,0)):
        Scene.m7a_icons_filter = StringProperty(description="Icons Filter", options={'TEXTEDIT_UPDATE'});
    else: Scene.m7a_icons_filter = StringProperty(description="Icons Filter");
    Scene.m7a_icons_history = BoolProperty(default=True, description="Show Icons Choose History");
    
    for cls in classes:
        try: bpy.utils.register_class(cls);
        except: pass
    
def unregister():
    global bl_conf;
    
    if (hasattr(Scene, "m7a_icons_filter")): del Scene.m7a_icons_filter;
    if (hasattr(Scene, "m7a_icons_history")): del Scene.m7a_icons_history;
    
    for cls in classes:
        try: bpy.utils.unregister_class(cls);
        except: pass
    
    #r_register_class(bl_conf, "TEXT_HT_header");
    r_register_class(bl_conf, "TEXT_PT_find");
    r_register_class(bl_conf, "TEXT_PT_properties");
    #r_register_class(bl_conf, "TEXT_HT_footer");
