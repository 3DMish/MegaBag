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

import bpy, sys, os, shutil;

from bpy.types import Operator, PropertyGroup, AddonPreferences, WindowManager as lc_manager;
from bpy.props import StringProperty, BoolProperty, FloatProperty, PointerProperty, EnumProperty;

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/");

from bpy_sys import *;
from m7a_quick_pack_scripts import *;

import m7a_modifiers, m7a_text_editor, m7a_quick_pack, m7a_view3d_header, m7a_view3d_tool_header;
import m7a_text_editor, m7a_dope_sheet;

bl_conf = {
    "OBJECT": [],
}

class M7A_MEGABAG_Button(Operator):
    bl_idname      = "m7a.megabag_button";
    bl_label       = "M7A Button";
    bl_options     = {'REGISTER', 'UNDO'};
    
    option : StringProperty();
    value  : FloatProperty(default=0.1);
    data   : StringProperty();
    desc   : StringProperty();
    
    @classmethod
    def description(cls, context, properties):
        if not (properties.desc == ""): return properties.desc;
        else: pass;
    
    def execute(self, context):
        global bl_conf; a_obj = context.active_object;
        lc_tool_settings = context.tool_settings;
        a_obj_modifiers = a_obj.modifiers if (a_obj.type != "GPENCIL") else a_obj.grease_pencil_modifiers;
        
        def opt_modifiers(list_modifiers, view = "view", value = False):
            for modifier in list_modifiers:
                if   (view == "view"):       modifier.show_viewport = value;
                elif (view == "render"):     modifier.show_render = value;
                if   (view == "view_tgl"):   modifier.show_viewport = False if (modifier.show_viewport) else True;
                elif (view == "render_tgl"): modifier.show_render = False if (modifier.show_viewport) else True;
                elif (view == "apply"):      bpy.ops.object.modifier_apply(modifier=modifier.name);
        
        if   (self.option == "MOD_APPLY_ALL"):       opt_modifiers(a_obj_modifiers, "apply");
        
        elif (self.option == "MOD_VIEWPORT_ON"):     opt_modifiers(a_obj_modifiers, "view", True);
        elif (self.option == "MOD_VIEWPORT_OFF"):    opt_modifiers(a_obj_modifiers, "view", False);
        elif (self.option == "MOD_VIEWPORT_TOGGLE"): opt_modifiers(a_obj_modifiers, "view_tgl");
        
        elif (self.option == "MOD_RENDER_ON"):       opt_modifiers(a_obj_modifiers, "render", True);
        elif (self.option == "MOD_RENDER_OFF"):      opt_modifiers(a_obj_modifiers, "render", False);
        elif (self.option == "MOD_RENDER_TOGGLE"):   opt_modifiers(a_obj_modifiers, "render_tgl");
                    
        elif (self.option == "MOD_REMOVE_VIEW"):
            list_modifiers = [];
            for modifier in a_obj_modifiers:
                if (modifier.show_viewport == False): list_modifiers.append(modifier.name);
            for modifier in list_modifiers: a_obj_modifiers.remove(a_obj_modifiers[modifier]);
            del list_modifiers;
            
        elif (self.option == "MOD_REMOVE_RENDER"):
            list_modifiers = [];
            for modifier in a_obj_modifiers:
                if (modifier.show_render == False): list_modifiers.append(modifier.name);
            for modifier in list_modifiers: a_obj_modifiers.remove(a_obj_modifiers[modifier]);
            del list_modifiers;
            
        elif (self.option == "MOD_REMOVE_ALL"):
            for i in range(0, len(a_obj_modifiers)):
                a_obj_modifiers.remove(a_obj_modifiers[len(a_obj_modifiers)-1]);
        
        # -------------------------------------------
        
        elif (self.option == "SET_MISHKEY_PROPS"):
            if (ver_less(3,4,1)): bpy_preferences().inputs.select_mouse = 'LEFT';
            bpy_preferences().inputs.walk_navigation.use_gravity = True;
            bpy_preferences().inputs.invert_mouse_zoom = True;
            bpy_preferences().inputs.invert_zoom_wheel = False;
            bpy_preferences().inputs.view_rotate_method = 'TURNTABLE';
            
        elif (self.option in {"INSTALL_MISHKEY", "REINSTALL_MISHKEY"}):
            path = bpy.utils.user_resource('SCRIPTS', path=os.path.join("presets", "keyconfig"), create=True);
            path = os.path.join(path, "MishKey.py");
            
            if (self.option == "REINSTALL_MISHKEY"): os.remove(path);
                
            shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), "m7a_lg_mishkey.py"), path);
            bpy.utils.keyconfig_set(path);
        
        elif (self.option in {"UNINSTALL_MISHKEY"}):
            path = bpy.utils.user_resource('SCRIPTS', path=os.path.join("presets", "keyconfig"), create=True);
            path = os.path.join(path, "MishKey.py"); os.remove(path);
            context.window_manager.keyconfigs.remove(context.window_manager.keyconfigs['MishKey']);
        
        # -------------------------------------------
        
        elif (self.option in {"OBJECT_MEMORY"}): bl_conf["OBJECT"] = context.selected_objects;
        elif (self.option in {"CLEAR_OBJECT_MEMORY"}): bl_conf["OBJECT"] = [];
            
        elif (self.option in {"SET_KEYFRAMES"}):
            for obj in context.selected_objects if (bl_conf["OBJECT"] == []) else bl_conf["OBJECT"]:
                obj.keyframe_insert(data_path="location");
                obj.keyframe_insert(data_path="rotation_euler");
                obj.keyframe_insert(data_path="scale");
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1);
            
        elif (self.option in {"SET_KEYFRAME_BACKWARD", "SET_KEYFRAME_FORWARD"}):
            hide_frame = 1 if (self.option in {"SET_KEYFRAME_FORWARD"}) else -1;
            
            def set_status(obj, status): obj.hide_viewport = status; obj.hide_render = status;
            
            def set_key(obj, status, frame):
                set_status(obj, status); obj.keyframe_insert(data_path="hide_viewport", frame=frame);
                obj.keyframe_insert(data_path="hide_render", frame=frame);
                
            for obj in context.selected_objects if (bl_conf["OBJECT"] == []) else bl_conf["OBJECT"]:
                current = context.scene.frame_current; set_key(obj, False, current);
                set_key(obj, True, current + hide_frame); set_status(obj, False);
                obj.select_set(True); bpy.context.view_layer.objects.active = obj;
            
        # -------------------------------------------
        
        elif (self.option in {"ISOLATE_ANIM_BONES"}):
            anim_name = context.object.animation_data.action.name;
            
            for bone in list(a_obj.data.bones):
                if not (bpy.data.objects[a_obj.name].pose.bones[bone.name] in context.selected_pose_bones_from_active_object):
                    if (bone.name in list(bpy.data.actions[anim_name].groups.keys())):
                        bpy.data.actions[anim_name].groups[bone.name].mute = True;
            
                        if (context.scene.m7a_megabag_keep_pose == False):
                            auto_key = lc_tool_settings.use_keyframe_insert_auto;
                            
                            bpy.data.objects[a_obj.name].pose.bones[bone.name].location = (0, 0, 0);
                            bpy.data.objects[a_obj.name].pose.bones[bone.name].rotation_quaternion = (1, 0, 0, 0);
                            bpy.data.objects[a_obj.name].pose.bones[bone.name].scale = (1, 1, 1);
                            
                            lc_tool_settings.use_keyframe_insert_auto = auto_key;
            
            bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_current;
        
        elif (self.option in {"MUTE_ANIM_BONES"}):
            anim_name = context.object.animation_data.action.name;
            
            for bone in list(a_obj.data.bones):
                if (bpy.data.objects[a_obj.name].pose.bones[bone.name] in context.selected_pose_bones_from_active_object):
                    if (bone.name in list(bpy.data.actions[anim_name].groups.keys())):
                        bpy.data.actions[anim_name].groups[bone.name].mute = True;
            
                        if (context.scene.m7a_megabag_keep_pose == False):
                            auto_key = lc_tool_settings.use_keyframe_insert_auto;
                            
                            bpy.data.objects[a_obj.name].pose.bones[bone.name].location = (0, 0, 0);
                            bpy.data.objects[a_obj.name].pose.bones[bone.name].rotation_quaternion = (1, 0, 0, 0);
                            bpy.data.objects[a_obj.name].pose.bones[bone.name].scale = (1, 1, 1);
                            
                            lc_tool_settings.use_keyframe_insert_auto = auto_key;
            
            bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_current;
        
        elif (self.option in {"ALL_ANIM_BONES"}):
            anim_name = context.object.animation_data.action.name;
            
            for bone in list(a_obj.data.bones):
                if (bone.name in list(bpy.data.actions[anim_name].groups.keys())):
                    bpy.data.actions[anim_name].groups[bone.name].mute = False;
            
            bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_current;
        
        # -------------------------------------------
        
        elif (self.option in {"RUN_SCRIPT_IN_OBJECT"}):
            name = context.scene.m7a_megabag_viewer;
            if   (name == "M7A-7913-SCRIPT-8755933"): m7a_script_add_seam(self.value);
            elif (name == "M7A-7913-SCRIPT-8755934"): m7a_script_add_jeans_seam();
            
        elif (self.option in {"ADD_MESH_IN_OBJECT"}):
            name = context.scene.m7a_megabag_viewer;
            if (name != ""):
                bpy.ops.mesh.select_all(action='DESELECT');
                
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
                bpy.ops.wm.append(directory=data_path+"/m7a_data.blend/Object", filename=name);
                
                p_obj = bpy.data.objects[name]; p_obj.hide_viewport = False;
                p_obj.location = context.scene.cursor.location;
                
                bpy.ops.object.select_all(action='DESELECT');
                
                a_obj.select_set(True); p_obj.select_set(True);
                bpy.context.view_layer.objects.active = a_obj;
                
                bpy.ops.object.join();
                
                bpy.ops.object.mode_set(mode='EDIT', toggle=False);
            
        elif (self.option in {"CHANGE_PROP_SIZE"}):
            context.scene.tool_settings.proportional_size += self.value;
            
        elif (self.option in {"MOD_ADD_AS_EXIST"}):
            if (hasattr(lc_manager, "m7a_howmod_add")):
                if (self.data in {"ON"}): context.window_manager.m7a_howmod_add = "use_exist";
                else: context.window_manager.m7a_howmod_add = "always_new";
            
        elif (self.option in {"ADD_M7A_MODIFIER"}):
            name = self.data; a_obj = context.active_object; exist = False;
            mod_name = name.replace("GeoNodes ", "");
            
            if (hasattr(lc_manager, "m7a_howmod_add")):
                if (context.window_manager.m7a_howmod_add == "use_exist") and \
                    (mod_name in bpy.data.node_groups):
                        m7a_geonode = bpy.data.node_groups[mod_name];
                        exist = True;
            
            if (exist == False):
                if (ver_more(3,3,0)): file_name = 'm7a_data_3.3.blend';
                else: file_name = 'm7a_data_3.0.blend';
                bpy.ops.wm.append(directory=data_path+"/"+file_name+"/NodeTree", filename=name);
                m7a_geonode = bpy.data.node_groups[name];
                m7a_geonode.name = mod_name;
                bpy.context.active_object.select_set(True);
                    
            m7a_modifier = a_obj_modifiers.new(name=mod_name, type='NODES');
            bpy.ops.object.modifier_set_active(modifier=m7a_modifier.name);
            m7a_modifier.node_group = m7a_geonode;
        
        elif (self.option == "SNAP_POINT_CENTER_X"):
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
            for vert in a_obj.data.vertices:
                if (vert.select == True):
                    vert.co.x = 0.0;
            bpy.ops.object.mode_set(mode='EDIT', toggle=False);
        
        elif (self.option == "FLIP_ACTIVE_CAMERA"):
            if (context.scene.camera.scale.x < 0): context.scene.camera.scale.x = 1;
            else: context.scene.camera.scale.x = -1;
        
        elif (self.option == "RESET_GISMO_SIZE"):
            if (ver_more(3,0,0)): bpy_preferences().view.gizmo_size = 75;
            else: bpy_preferences().view.manipulator_size = 75;
            
        elif (self.option == "CLEAR_LOCATION_X"):
            if not (context.mode in {'POSE'}): a_obj.location[0] = 0.0;
            else: context.active_pose_bone.location[0] = 0.0;
        elif (self.option == "CLEAR_LOCATION_Y"):
            if not (context.mode in {'POSE'}): a_obj.location[1] = 0.0;
            else: context.active_pose_bone.location[1] = 0.0;
        elif (self.option == "CLEAR_LOCATION_Z"):
            if not (context.mode in {'POSE'}): a_obj.location[2] = 0.0;
            else: context.active_pose_bone.location[2] = 0.0;
        
        elif (self.option == "CLEAR_ROTATION_EULER_X"):
            if not (context.mode in {'POSE'}): a_obj.rotation_euler[0] = 0.0;
            else: context.active_pose_bone.rotation_euler[0] = 0.0;
        elif (self.option == "CLEAR_ROTATION_EULER_Y"):
            if not (context.mode in {'POSE'}): a_obj.rotation_euler[1] = 0.0;
            else: context.active_pose_bone.rotation_euler[1] = 0.0;
        elif (self.option == "CLEAR_ROTATION_EULER_Z"):
            if not (context.mode in {'POSE'}): a_obj.rotation_euler[2] = 0.0;
            else: context.active_pose_bone.rotation_euler[2] = 0.0;
        
        elif (self.option == "CLEAR_ROTATION_QUATERNION_W"):
            if not (context.mode in {'POSE'}): a_obj.rotation_quaternion[0] = 1.0;
            else: context.active_pose_bone.rotation_quaternion[0] = 1.0;
        elif (self.option == "CLEAR_ROTATION_QUATERNION_X"):
            if not (context.mode in {'POSE'}): a_obj.rotation_quaternion[1] = 0.0;
            else: context.active_pose_bone.rotation_quaternion[1] = 0.0;
        elif (self.option == "CLEAR_ROTATION_QUATERNION_Y"):
            if not (context.mode in {'POSE'}): a_obj.rotation_quaternion[2] = 0.0;
            else: context.active_pose_bone.rotation_quaternion[2] = 0.0;
        elif (self.option == "CLEAR_ROTATION_QUATERNION_Z"):
            if not (context.mode in {'POSE'}): a_obj.rotation_quaternion[3] = 0.0;
            else: context.active_pose_bone.rotation_quaternion[3] = 0.0;
        
        elif (self.option == "CLEAR_ROTATION_AXIS_ANGLE_W"):
            if not (context.mode in {'POSE'}): a_obj.rotation_axis_angle[0] = 0.0;
            else: context.active_pose_bone.rotation_axis_angle[0] = 0.0;
        elif (self.option == "CLEAR_ROTATION_AXIS_ANGLE_X"):
            if not (context.mode in {'POSE'}): a_obj.rotation_axis_angle[1] = 0.0;
            else: context.active_pose_bone.rotation_axis_angle[1] = 0.0;
        elif (self.option == "CLEAR_ROTATION_AXIS_ANGLE_Y"):
            if not (context.mode in {'POSE'}): a_obj.rotation_axis_angle[2] = 0.0;
            else: context.active_pose_bone.rotation_axis_angle[2] = 0.0;
        elif (self.option == "CLEAR_ROTATION_AXIS_ANGLE_Z"):
            if not (context.mode in {'POSE'}): a_obj.rotation_axis_angle[3] = 0.0;
            else: context.active_pose_bone.rotation_axis_angle[3] = 0.0;
        
        elif (self.option == "CLEAR_SCALE_X"):
            if not (context.mode in {'POSE'}): a_obj.scale[0] = 1.0;
            else: context.active_pose_bone.scale[0] = 1.0;
        elif (self.option == "CLEAR_SCALE_Y"):
            if not (context.mode in {'POSE'}): a_obj.scale[1] = 1.0;
            else: context.active_pose_bone.scale[1] = 1.0;
        elif (self.option == "CLEAR_SCALE_Z"):
            if not (context.mode in {'POSE'}): a_obj.scale[2] = 1.0;
            else: context.active_pose_bone.scale[2] = 1.0;
            
        return {'FINISHED'};

def update_view3d(self, context):
    bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_quick_pack = \
    bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_quick_pack;
    
    bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_tool_header = \
    bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_tool_header;
    
    if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_update):
        m7a_view3d_header.register();
    else: m7a_view3d_header.unregister();
    
def update_text_panel(self, context):
    if (bpy_preferences("addons", "megabag").m7a_megabag_props.text_editor_update):
        m7a_text_editor.register();
    else: m7a_text_editor.unregister();

def update_modifiers(self, context):
    if (bpy_preferences("addons", "megabag").m7a_megabag_props.modifiers_update):
        m7a_modifiers.register();
    else: m7a_modifiers.unregister();

def update_quick_pack(self, context):
    if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_quick_pack) and \
        (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_update):
        m7a_quick_pack.register();
    else: m7a_quick_pack.unregister();
    
def update_tool_header(self, context):
    if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_tool_header) and \
        (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_update):
        m7a_view3d_tool_header.register();
    else: m7a_view3d_tool_header.unregister();
    
def update_dope_sheet(self, context):
    bpy_preferences("addons", "megabag").m7a_megabag_props.dope_compact_menu = \
    bpy_preferences("addons", "megabag").m7a_megabag_props.dope_compact_menu;
    
    bpy_preferences("addons", "megabag").m7a_megabag_props.dope_play_pause = \
    bpy_preferences("addons", "megabag").m7a_megabag_props.dope_play_pause;
    
    if (bpy_preferences("addons", "megabag").m7a_megabag_props.dope_sheet_update):
        m7a_dope_sheet.register();
    else: m7a_dope_sheet.unregister();

class M7A_MEGABAG_Properties(PropertyGroup):
    view3d_update       : BoolProperty(default=True, update=update_view3d);
    view3d_compact_menu : BoolProperty(default=True);
    view3d_tool_header  : BoolProperty(default=True, update=update_tool_header);
    view3d_quick_pack   : BoolProperty(default=True, update=update_quick_pack);
    
    modifiers_update    : BoolProperty(default=True, update=update_modifiers);
    modifiers_options   : BoolProperty(default=True);
    modifiers_m7a_pack  : BoolProperty(default=True);
    
    text_editor_update  : BoolProperty(default=True, update=update_text_panel);
    text_editor_file    : BoolProperty(default=True);
    text_editor_icons   : BoolProperty(default=True);
    text_editor_info    : BoolProperty(default=True);
    
    dope_sheet_update   : BoolProperty(default=True, update=update_dope_sheet);
    dope_compact_menu   : BoolProperty(default=True);
    dope_play_pause     : BoolProperty(default=True);

class M7A_MEGABAG_Preferences(AddonPreferences):
    bl_idname = "megabag";
    
    m7a_megabag_props : PointerProperty(type=M7A_MEGABAG_Properties);
    
    def draw(self, context):
        def template_item(lc_cont, text, icon, data = None, props= None):
            lc_cont = lc_cont.column(align=True);
            lc_row = lc_cont.box().row(align=True);
            lc_row.label(text=text, icon=icon);
            if (data != None): lc_row.prop(data, props,  text="");
            return lc_cont.box().column(align=True);
            
        lc_main = self.layout.column(align=False);
        
        lc_box = lc_main.box().row(align = True);
        is_mishkey_exist = "MishKey" in bpy.context.window_manager.keyconfigs.keys();
        btn_name = "ReInstall MishKey" if (is_mishkey_exist) else "Install MishKey";
        lc_btn = lc_box.operator("m7a.megabag_button", text=btn_name, icon="IMPORT")
        lc_btn.option = "REINSTALL_MISHKEY" if (is_mishkey_exist) else "INSTALL_MISHKEY";
        lc_btn_description(lc_btn, "Install Keymap: MishKey");
        
        if (is_mishkey_exist):
            lc_btn = lc_box.operator("m7a.megabag_button", text="", icon="TRASH");
            lc_btn.option = "UNINSTALL_MISHKEY";
            lc_btn_description(lc_btn, "Remove Keymap: MishKey");
            
        lc_box.separator();
        lc_btn = lc_box.operator("m7a.megabag_button", text="Set Props", icon="TOOL_SETTINGS");
        lc_btn.option = "SET_MISHKEY_PROPS";
        lc_btn_description(lc_btn, "Set 3DMish's properties in blender, like ''Navigation'', add corrections in ''Interface'' ...");
        
        lc_main.separator();
        
        lc_box = template_item(lc_main, text="3D View:", icon="VIEW3D", data=self.m7a_megabag_props, props="view3d_update");
        lc_box_row = lc_box.row(align=True);
        lc_box_row.active = self.m7a_megabag_props.view3d_update;
        lc_box_row.prop(self.m7a_megabag_props, "view3d_compact_menu",  text="Compact Menu");
        lc_box_row.prop(self.m7a_megabag_props, "view3d_tool_header",  text="Tool Settings");
        lc_box_row.prop(self.m7a_megabag_props, "view3d_quick_pack",  text="Quick Pack");
        
        lc_box = template_item(lc_main, text="Modifiers:", icon="MODIFIER", data=self.m7a_megabag_props, props="modifiers_update");
        lc_box_row = lc_box.row(align=True);
        lc_box_row.active = self.m7a_megabag_props.modifiers_update;
        lc_box_row.prop(self.m7a_megabag_props, "modifiers_options",  text="Modifiers Options");
        if ver_more(3,0,0):
            lc_box_row.prop(self.m7a_megabag_props, "modifiers_m7a_pack",  text="M7A Modifiers");
            if (bpy.context.region.width > 400): lc_box_row.label(text=" ");
        
        lc_box = template_item(lc_main, text="Text Edit:", icon="TEXT", data=self.m7a_megabag_props, props="text_editor_update");
        lc_box_row = lc_box.row(align=True);
        lc_box_row.active = self.m7a_megabag_props.text_editor_update;
        lc_box_row.prop(self.m7a_megabag_props, "text_editor_info",  text="Info");
        lc_box_row.prop(self.m7a_megabag_props, "text_editor_file",  text="File");
        lc_box_row.prop(self.m7a_megabag_props, "text_editor_icons", text="Icon Viewer");
        
        lc_box = template_item(lc_main, text="Dope Sheet:", icon="ACTION", data=self.m7a_megabag_props, props="dope_sheet_update");
        lc_box_row = lc_box.row(align=True);
        lc_box_row.active = self.m7a_megabag_props.dope_sheet_update;
        lc_box_row.prop(self.m7a_megabag_props, "dope_compact_menu",  text="Compact Menu");
        lc_box_row.prop(self.m7a_megabag_props, "dope_play_pause",  text="Show (Play/Pause)");
        if (bpy.context.region.width > 400): lc_box_row.label(text=" ");
        
class M7A_Icon_Select(Operator):
    bl_idname      = "m7a.icon_select";
    bl_label       = "";
    bl_description = "Select the Icon";
    bl_options     = {'INTERNAL'}

    icon: StringProperty();
    option: StringProperty();

    @classmethod
    def description(cls, context, properties):
        if (properties.option == "CLEAR"): return "Clear history";

    def execute(self, context):
        if (self.option == "CLEAR"):
            m7a_text_editor.bl_conf["HISTORY"] = [];
        else:
            context.window_manager.clipboard = self.icon;
            bl_conf["SELECTED"] = self.icon;
            if (self.icon not in m7a_text_editor.bl_conf["HISTORY"]):
                m7a_text_editor.bl_conf["HISTORY"].append(self.icon);
            self.report({'INFO'}, self.icon);

        return {'FINISHED'}
        
class M7A_OBJECT_Apply(Operator):
    bl_idname      = 'm7a.object_apply';
    bl_label       = "Apply";
    bl_description = 'Apply Transforms';
    
    props: EnumProperty(
        items = [
            ("", "        Apply", ""),
            
            ("loc",          "Location",                 "Apply Location"),
            ("rot",          "Rotation",                 "Apply Rotation"),
            ("scale",        "Scale",                    "Apply Scale"),
            ("all",          "All Transforms",           "Apply All Transforms"),
            ("r&s",          "Rotation & Scale",         "Apply Rotation & Scale"),
            
            ("", "        Apply to Deltas", ""),
            
            ("loc_deltas",   "Location to Deltas",       "Apply Location to Deltas"),
            ("rot_deltas",   "Rotation to Deltas",       "Apply Rotation to Deltas"),
            ("scale_deltas", "Scale to Deltas",          "Apply Scale to Deltas"),
            ("all_deltas",   "All Transforms to Deltas", "Apply All Transforms to Deltas"),
            
            ("", "        Visual Apply", ""),
            
            ("visual",       "Visual Transform",         "Apply Visual Transform"),
            ("visual_gtm",   "Visual Geometry to Mesh",  "Apply Visual Geometry to Mesh"),
            ("instance",     "Make Instance Real",       "Make Instance Real"),
        ]
    );
    
    def execute(self, context):
        if (self.props in ["loc", "rot", "scale", "all", "r&s"]):
            bpy.ops.object.transform_apply(
                location = True if (self.props in ["loc", "all"]) else False,
                rotation = True if (self.props in ["rot", "all", "r&s"]) else False,
                scale    = True if (self.props in ["scale", "all", "r&s"]) else False,
            );
        elif (self.props in ["loc_deltas", "rot_deltas", "scale_deltas", "all_deltas"]):
            bpy.ops.object.transforms_to_deltas(
                mode = "LOC"   if (self.props in ["loc_deltas"]) else 
                       "ROT"   if (self.props in ["rot_deltas"]) else 
                       "SCALE" if (self.props in ["scale_deltas"]) else "ALL"
            );
        elif (self.props in ["visual"]):     bpy.ops.object.visual_transform_apply();
        elif (self.props in ["visual_gtm"]): bpy.ops.object.convert(target='MESH');
        elif (self.props in ["instance"]):   bpy.ops.object.duplicates_make_real();
            
        return {'FINISHED'};

class M7A_EDIT_Falloff(bpy.types.Operator):
	bl_idname		= 'm7a.edit_falloff';
	bl_label		= 'Edit Falloff';
	bl_description  = '';
    
	type: bpy.props.StringProperty();
	
	def execute(self, context):
		bpy.context.scene.tool_settings.proportional_edit_falloff = self.type;
		return {'FINISHED'}

classes = [
    M7A_MEGABAG_Button, M7A_MEGABAG_Properties, M7A_MEGABAG_Preferences, M7A_Icon_Select, 
];

def register():
    for cls in [M7A_OBJECT_Apply, M7A_EDIT_Falloff]: bpy.utils.register_class(cls);
    
    for cls in classes: bpy.utils.register_class(cls);
    

def unregister():
    for cls in [M7A_OBJECT_Apply, M7A_EDIT_Falloff]: bpy.utils.unregister_class(cls);
        
    for cls in classes: bpy.utils.unregister_class(cls);
