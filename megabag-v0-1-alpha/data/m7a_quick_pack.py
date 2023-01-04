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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/m7a_quick_pack");

from bpy_sys import *;
from m7a_quick_pack_meshes import m7a_meshes;
from bpy.types import Panel, Menu, Operator, Scene as lc_manager;
from bpy.props import BoolProperty, StringProperty, IntProperty, EnumProperty;

if (ver_less(2,80,0)): import m7a_props_v1 as m7a_rem;
else: import m7a_props_v2 as m7a_rem;

import m7a_mesh, m7a_empty, m7a_camera, m7a_curve, m7a_keys, m7a_custom_properties;

if (ver_more(2,78,0)): import bpy.utils.previews;
lc_prew = bpy.utils.previews.new();

bl_conf = {
    "subcategory": [],
    "tmp_items": [],
}

class M7A_VIEW3D_PT_QUICK_Pack(Panel):
    bl_space_type  = 'VIEW_3D';
    bl_region_type = 'UI' if ver_more(2,80,0) else "TOOLS";
    bl_category    = "Quick Pack";
    bl_label       = "Quick Pack";
    
    def draw(self, context):
        lc_space_data = context.space_data;
        lc_tool_settings = context.tool_settings;
        
        lc_main = self.layout.column(align = True);
        lc_scene = context.scene;
        a_obj = context.active_object;
        
        def lc_label(lc_layout, label, icon, asset = True, delete = True):
            lc_row = lc_layout.row(align = True);
            lc_row.label(text=label, icon=icon);
            if not (a_obj.type in {"EMPTY", "ARMATURE"}) and not (context.mode.split("_")[0] in {"EDIT", "PAINT", "SCULPT"}):
                if (ver_more(3,0,0)): lc_row.menu("VIEW3D_MT_object_convert", text="", icon="MAT_SPHERE_SKY");
                else: lc_row.operator_menu_enum("object.convert", "target", text="", icon="MAT_SPHERE_SKY")
                
            if (ver_more(3,0,0)):
                if (asset) and not (context.mode.split("_")[0] in {"EDIT", "PAINT"}):
                    lc_row.separator();
                    if not (a_obj.asset_data): lc_row.operator("asset.mark", text="", icon="ASSET_MANAGER", emboss=False);
                    else: lc_row.operator("asset.clear", text="", icon="ASSET_MANAGER", depress=True).set_fake_user = False;
            
            lc_row_append = lc_row.row(align = True);
            
            if (delete):
                lc_row_del = lc_row.row(align = True);
                lc_row_del.separator();
                lc_row_del.operator("object.delete", text="", icon="TRASH" if (ver_more(3,0,0)) else "X", emboss=False);
                lc_row_del.active = not (context.selected_objects == []);
            return lc_row_append;
                        
        
        if (context.active_object != None):
            if (context.mode in {"OBJECT"}):
                
                lc_main.row(align=True).prop(context.scene, "m7a_megabag_show", expand=True);
                lc_main.separator();
                    
                if (context.scene.m7a_megabag_show == "props"):
                    lc_btn_row = lc_main.row(align = True);
                    
                    if (a_obj.type == "MESH"):
                        lc_main_row = lc_label(lc_main, "Mesh", icon="MESH_DATA");
                        lc_main_row.separator();
                        lc_btn = lc_main_row.operator("object.mode_set", text="", icon="EDITMODE_HLT", emboss=False);
                        lc_btn.mode='EDIT'; lc_btn.toggle=False;
                        lc_main.separator();
                        
                        m7a_mesh.draw_properties(self, context, lc_main);
                        
                    elif (a_obj.type == "CURVE"):
                        lc_main_row = lc_label(lc_main, "Curve", icon="CURVE_DATA");
                        lc_main_row.separator();
                        lc_btn = lc_main_row.operator("object.mode_set", text="", icon="OUTLINER_DATA_CURVE", emboss=False);
                        lc_btn.mode='EDIT'; lc_btn.toggle=False;
                        lc_main.separator();
                        
                        m7a_curve.draw_properties(self, context, lc_main);
                        
                    elif (a_obj.type == "GPENCIL"):
                        lc_main_row = lc_label(lc_main, "G-Pencil", icon="GP_SELECT_POINTS");
                        lc_main_row.separator();
                        lc_btn = lc_main_row.operator("object.mode_set", text="", icon="GREASEPENCIL", emboss=False);
                        lc_btn.mode='PAINT_GPENCIL'; lc_btn.toggle=False;
                        lc_main.separator();
                        
                    elif (a_obj.type == "EMPTY"):
                        lc_label(lc_main, "Empty", icon="OUTLINER_DATA_EMPTY");
                        lc_main.separator();
                                  
                        m7a_empty.draw_properties(self, context, lc_main);
                        
                    elif (a_obj.type == "ARMATURE"):
                        lc_main_row = lc_label(lc_main, "Armature", icon="OUTLINER_DATA_ARMATURE");
                        lc_main_row.separator();
                        lc_btn = lc_main_row.operator("object.mode_set", text="", icon="ARMATURE_DATA", emboss=False);
                        lc_btn.mode='POSE'; lc_btn.toggle=False;
                        lc_main.separator();
                        
                    elif (a_obj.type == "META"):
                        lc_label(lc_main, "Meta", icon="META_DATA");
                        lc_main.separator();
                        
                    elif (a_obj.type == "SURFACE"):
                        lc_label(lc_main, "Surface", icon="SURFACE_DATA");
                        lc_main.separator();
                        
                        lc_main.prop(context.active_object.data, "resolution_u", text="Prew. U");
                        lc_main.prop(context.active_object.data, "resolution_v", text="Prew. V");
                        lc_main.separator();
                        lc_main.prop(context.active_object.data, "render_resolution_u", text="Render. U");
                        lc_main.prop(context.active_object.data, "render_resolution_v", text="Render. V");
                        
                    elif (a_obj.type == "CAMERA"):
                        lc_main_row = lc_label(lc_main, "Camera", icon="CAMERA_DATA");
                        
                        if (lc_space_data.region_3d.view_perspective == 'CAMERA'):
                            lc_main_row.separator();
                            lc_main_row.prop(
                                lc_space_data, "lock_camera", text="",
                                icon="CON_CAMERASOLVER" if (ver_more(3,0,0)) else "OUTLINER_OB_CAMERA",
                                emboss=lc_space_data.lock_camera
                            );
                        lc_main.separator();
                        
                        m7a_camera.draw_properties(self, context, lc_main);
                        
                    lc_main.separator();
                    
                    m7a_keys.draw_properties(self, context, lc_main);
                    lc_main.separator();
                    m7a_custom_properties.draw_properties(self, context, lc_main);
                        
                else: m7a_object_transform(lc_main, context);
                    
            elif (context.mode in {"PAINT_GPENCIL", "EDIT_GPENCIL", "SCULPT_GPENCIL"}):
                
                lc_main.row(align=True).prop(context.scene, "m7a_megabag_show", expand=True);
                lc_main.separator();
                    
                if (context.scene.m7a_megabag_show == "props"):
                    lc_main_row = lc_label(lc_main, "G-Pencil", icon="GP_SELECT_POINTS", asset=False);
                    lc_main_row.separator();
                    if (context.mode in {"PAINT_GPENCIL"}):
                        lc_btn = lc_main_row.operator("object.mode_set", text="", icon="EDITMODE_HLT", emboss=False);
                        lc_btn.mode='EDIT_GPENCIL'; lc_btn.toggle=False;
                        lc_main_row.separator();
                        lc_btn = lc_main_row.operator("object.mode_set", text="", icon="SCULPTMODE_HLT", emboss=False);
                        lc_btn.mode='SCULPT_GPENCIL'; lc_btn.toggle=False;
                    elif (context.mode in {"EDIT_GPENCIL", "SCULPT_GPENCIL"}):
                        lc_main_row.separator();
                        lc_btn = lc_main_row.operator("object.mode_set", text="", icon="GREASEPENCIL", emboss=False);
                        lc_btn.mode='PAINT_GPENCIL'; lc_btn.toggle=False;
                        if (context.mode in {"EDIT_GPENCIL"}):
                            lc_main_row.separator();
                            lc_btn = lc_main_row.operator("object.mode_set", text="", icon="SCULPTMODE_HLT", emboss=False);
                            lc_btn.mode='SCULPT_GPENCIL'; lc_btn.toggle=False;
                        if (context.mode in {"SCULPT_GPENCIL"}):
                            lc_main_row.separator();
                            lc_btn = lc_main_row.operator("object.mode_set", text="", icon="EDITMODE_HLT", emboss=False);
                            lc_btn.mode='EDIT_GPENCIL'; lc_btn.toggle=False;
                    lc_main_row.separator();
                    lc_btn = lc_main_row.operator("object.mode_set", text="", icon="OBJECT_DATA", emboss=False);
                    lc_btn.mode='OBJECT'; lc_btn.toggle=False;
                    
                    lc_main.separator();
                    
                    lc_row = lc_main.row(align = True);
                    lc_row.operator("ed.undo", icon="LOOP_BACK", text="Undo");
                    lc_row.operator("ed.redo", icon="LOOP_FORWARDS", text="Redo");
                    
                    if (context.scene.camera):
                        lc_main.separator();
                        lc_main.operator(
                            "m7a.megabag_button", 
                            text = "X Flip Active Camera", 
                            icon = "SCREEN_BACK",
                            depress = context.scene.camera.scale.x < 0,
                        ).option = "FLIP_ACTIVE_CAMERA";
                    
                    lc_main.separator();
                    
                    lc_btn_row = lc_main.row(align = True);
                    
                    if (a_obj.mode == 'SCULPT_GPENCIL') or (a_obj.mode == 'EDIT_GPENCIL') or (a_obj.mode == 'PAINT_GPENCIL'):
                        lc_btn_row.prop(bpy.data.grease_pencils[a_obj.data.name], "stroke_depth_order", icon='NODE_COMPOSITING', text='');
                    if (a_obj.mode == 'EDIT_GPENCIL'):
                        lc_btn_row.operator('gpencil.snap_cursor_to_selected', icon='PIVOT_CURSOR', text='');
                        
                    lc_btn_row = lc_main.row(align = True);
                    lc_btn_row.prop(context.space_data.overlay, "use_gpencil_onion_skin", icon='MATFLUID'); 
                    #lc_btn_row.prop(context.space_data.overlay, "gpencil_fade_layer"); 
                    gpl = bpy.data.grease_pencils[a_obj.data.name].layers[context.active_gpencil_layer.info]
                    lc_btn_row.prop(gpl, "use_onion_skinning", text="Layer Onion Skinning" if (context.region.width > 300) else "Layer Oni-S",
                        icon='ONIONSKIN_ON' if gpl.use_onion_skinning else 'ONIONSKIN_OFF',
                        emboss=True,
                    );
                            
                    #lc_main.separator();
                    
                    #lc_btn_row = lc_main.row(align = True);
                    
                    #is_active = True if (a_obj.mode == 'PAINT_GPENCIL') else False;
                    #lc_btn_row.operator('object.mode_set', icon='GREASEPENCIL', depress=is_active, text='Pencil').mode = "PAINT_GPENCIL";
                        
                    #is_active = True if (a_obj.mode == 'EDIT_GPENCIL') else False;
                    #lc_btn_row.operator('object.mode_set', icon='EDITMODE_HLT', depress=is_active, text='Edit').mode = "EDIT_GPENCIL";
                    
                    #is_active = True if (a_obj.mode == 'SCULPT_GPENCIL') else False;
                    #lc_main.operator('object.mode_set', icon='SCULPTMODE_HLT', depress=is_active, text='Sculpt').mode = "SCULPT_GPENCIL";
                    
                    if (context.mode in {'PAINT_GPENCIL'}):
                        lc_main.separator();
                        lc_main.prop(context.scene.tool_settings, "use_gpencil_draw_onback", icon='MOD_OPACITY')
                        lc_main.prop(context.scene.tool_settings.gpencil_paint.brush.gpencil_settings, "active_smooth_factor", icon='MOD_SMOOTH')
                        lc_btn_row = lc_main.row(align = True);
                        lc_btn_row.prop(context.scene.tool_settings.gpencil_paint.brush.gpencil_settings, "use_settings_stabilizer", icon='MOD_SMOOTH', text='')
                        lc_btn_row.prop(bpy.data.brushes['Pencil'], "smooth_stroke_radius")
                        lc_main.prop(context.scene.tool_settings.gpencil_paint.brush.gpencil_settings, "simplify_factor", icon='GP_ONLY_SELECTED')
                        
                    if (context.mode in {'EDIT_GPENCIL'}):
                        lc_main.separator();
                        lc_btn_row = lc_main.row(align = True);
                        lc_btn_row.operator('gpencil.stroke_arrange', icon='FULLSCREEN_ENTER', text='Top').direction = "TOP";
                        lc_btn_row.operator('gpencil.stroke_arrange', text='Up').direction = "UP";
                        lc_btn_row = lc_main.row(align = True);
                        lc_btn_row.operator('gpencil.stroke_arrange', icon='FULLSCREEN_EXIT', text='Bottom').direction = "BOTTOM";
                        lc_btn_row.operator('gpencil.stroke_arrange', text='Down').direction = "DOWN";
                            
                        lc_main.separator();
                        
                        lc_row = lc_main.row(align = True);
                        if (context.region.width > 140):
                            lc_row.operator("transform.translate", text="Move", icon="OBJECT_ORIGIN" if (ver_more(3,0,0)) else "MAN_TRANS");
                            if (context.region.width > 210):
                                lc_row.operator("transform.rotate", text="Rotate", icon="ORIENTATION_GIMBAL" if (ver_more(3,0,0)) else "MAN_ROT");
                                lc_row.operator("transform.resize", text="Scale", icon="TRANSFORM_ORIGINS" if (ver_more(3,0,0)) else "MAN_SCALE");
                            else:
                                lc_row.operator("transform.rotate", text="", icon="ORIENTATION_GIMBAL" if (ver_more(3,0,0)) else "MAN_ROT");
                                lc_row.operator("transform.resize", text="", icon="TRANSFORM_ORIGINS" if (ver_more(3,0,0)) else "MAN_SCALE");
                        else:
                            lc_row.operator("transform.translate", text=" ", icon="OBJECT_ORIGIN" if (ver_more(3,0,0)) else "MAN_TRANS");
                            lc_row.operator("transform.rotate", text=" ", icon="ORIENTATION_GIMBAL" if (ver_more(3,0,0)) else "MAN_ROT");
                            lc_row.operator("transform.resize", text=" ", icon="TRANSFORM_ORIGINS" if (ver_more(3,0,0)) else "MAN_SCALE");
                                            
                        if (False):
                            lc_main.separator();
                            
                            lc_btn_row = lc_main.row(align = True);
                            lc_btn_row.operator('gpencil.duplicate_move', text='', icon='DUPLICATE');
                            
                            lc_btn = lc_btn_row.operator('m7a.megabag_button', text='gCopy', icon='COPYDOWN');
                            lc_btn_description(lc_btn, "Global copy selected Grease Pencil points and strokes");
                            lc_btn.option = 'GREASE_PAENCIL_COPY';
                            
                            lc_btn_cont = lc_btn_row.row(align = True); lc_btn_cont.enabled = gp_is_buffer();
                            lc_btn = lc_btn_cont.operator('m7a.megabag_button', text='gPaste', icon='PASTEDOWN');
                            lc_btn_description(lc_btn, "Global paste already copied grease pencil points and strokes to active layer");
                            lc_btn.option = 'GREASE_PAENCIL_PASTE';
                            
                            lc_btn_row.menu("VIEW3D_MT_edit_gpencil_delete", text='', icon="TRASH" if (ver_more(3,0,0)) else "X");
                        
                        lc_main.separator();
                        
                        lc_btn_row = lc_main.row(align = True);
                        lc_btn_row.prop(context.scene.tool_settings, "use_proportional_edit", text='')
                        lc_btn_row.prop(context.scene.tool_settings, "use_proportional_connected", icon='BLANK1');
                            
                        is_active = True if (context.scene.tool_settings.proportional_edit_falloff == 'SMOOTH') else False;
                        lc_btn_row.operator('m7a.edit_falloff', icon='SMOOTHCURVE', depress=is_active, text='').type = 'SMOOTH';
                            
                        is_active = True if (context.scene.tool_settings.proportional_edit_falloff == 'SHARP') else False;
                        lc_btn_row.operator('m7a.edit_falloff', icon='SHARPCURVE', depress=is_active, text='').type = 'SHARP';
                        
                        lc_btn_row = lc_main.row(align = True);
                        lc_btn = lc_btn_row.operator("m7a.megabag_button", text = "", icon = "TRACKING_BACKWARDS_SINGLE");
                        lc_btn.option = "CHANGE_PROP_SIZE"; lc_btn.value = -0.01;
                        lc_btn_row.prop(context.scene.tool_settings, "proportional_size", text='');
                        lc_row_btn = lc_btn_row.row(align = True);
                        lc_btn = lc_row_btn.operator("m7a.megabag_button", text = "", icon = "TRACKING_FORWARDS_SINGLE");
                        lc_btn.option = "CHANGE_PROP_SIZE"; lc_btn.value = 0.01;
                        lc_row_btn.ui_units_x = 1.3;
                        lc_btn_row.prop_with_popover(context.scene.tool_settings, "proportional_edit_falloff", text="", icon_only=True, panel="VIEW3D_PT_proportional_edit");
                        
                    if (context.mode in {'SCULPT_GPENCIL', 'EDIT_GPENCIL'}):
                        lc_main.separator();
                            
                        lc_btn_row = lc_main.row(align = True);
                        lc_btn_row.operator("gpencil.select_all", text='', icon='SELECT_SET').action='SELECT';
                        lc_btn_row.operator("gpencil.select_linked");
                        lc_btn_row.operator("gpencil.select_all", text='', icon='SELECT_INTERSECT').action='INVERT';
                        lc_btn_row.operator("gpencil.select_all", text='', icon='X').action='DESELECT';
                        
                    if (context.mode in {'SCULPT_GPENCIL'}):
                        lc_main.separator();
                        lc_btn_row = lc_main.row(align = True);
                        brush = lc_tool_settings.gpencil_sculpt_paint.brush;
                        tool = brush.gpencil_sculpt_tool;
                        is_active = True if (tool == 'SMOOTH') else False;
                        lc_btn_row.operator("wm.tool_set_by_id", text='Smooth', depress=is_active, icon='GPBRUSH_SMOOTH').name="builtin_brush.Smooth";
                        is_active = True if (tool == 'GRAB') else False;
                        lc_btn_row.operator("wm.tool_set_by_id", text='Grab', depress=is_active, icon='GPBRUSH_GRAB').name="builtin_brush.Grab";
                else: m7a_object_transform(lc_main, context);
            
            elif (context.mode in {'POSE'}):
                lc_main.row(align=True).prop(context.scene, "m7a_megabag_show", expand=True);
                lc_main.separator();
                
                if (context.scene.m7a_megabag_show == "props"):
                    lc_main_row = lc_label(lc_main, "Pose", icon="ARMATURE_DATA", asset=False);
                    lc_main_row.separator();
                    lc_btn = lc_main_row.operator("object.mode_set", text="", icon="OUTLINER_DATA_ARMATURE", emboss=False);
                    lc_btn.mode='OBJECT'; lc_btn.toggle=False;
                    lc_main.separator();
                    
                    lc_main.operator("pose.transforms_clear", text="Clear Pose", icon="PANEL_CLOSE");
                    
                    lc_main.separator();
                    
                    lc_main.operator("anim.keyframe_insert_menu", icon="PANEL_CLOSE");
                    lc_main_row = lc_main.row(align = True);
                    lc_main_row.operator("pose.copy", text="Copy Pose", icon="COPYDOWN");
                    lc_btn = lc_main_row.row(align = True);
                    lc_btn.operator("pose.paste", text="Paste", icon="PASTEDOWN").flipped = False;
                    lc_btn.scale_x = 0.6;
                    lc_main_row.operator("pose.paste", text="", icon="PASTEFLIPDOWN").flipped = True;
                    
                    lc_main.separator();
                    lc_main_row = lc_main.row(align = True);
                    
                    lc_btn_row = lc_main_row.row(align = True);
                    lc_btn_row.prop(context.scene, "m7a_megabag_keep_pose", text="", icon="ARMATURE_DATA");
                    lc_btn_row.scale_y = 2;
                    
                    lc_main_col = lc_main_row.column(align = True);
                    lc_btn = lc_main_col.operator("m7a.megabag_button", text="Mute Anim Bones", icon="ZOOM_SELECTED");
                    lc_btn.option = "MUTE_ANIM_BONES";
                    lc_btn_description(lc_btn, "Mute selected bones animation");
                    
                    lc_btn = lc_main_col.operator("m7a.megabag_button", text="Isolate Anim Bones", icon="ZOOM_SELECTED");
                    lc_btn.option = "ISOLATE_ANIM_BONES";
                    lc_btn_description(lc_btn, "Mute not selected bones animation");
                    
                    lc_btn_row = lc_main_row.row(align = True);
                    lc_btn = lc_btn_row.operator("m7a.megabag_button", text="", icon="ZOOM_PREVIOUS");
                    lc_btn.option = "ALL_ANIM_BONES";
                    lc_btn_description(lc_btn, "Unmute all bones");
                    lc_btn_row.scale_y = 2;
                        
                    lc_main.separator();
                    m7a_custom_properties.draw_properties(self, context, lc_main);
                    
                else:
                    lc_btns = lc_main.column(align = True);
                    lc_btns.active = context.active_bone.use_connect == False;
                    m7a_obj_transform(lc_btns, "Location:", "transform.translate", "OBJECT_ORIGIN", "location", "lock_location", context.active_pose_bone);
                    lc_main.separator();
                    lc_rot = m7a_obj_transform(lc_main, "Rotation:", "transform.rotate", "ORIENTATION_GIMBAL", "rotation_euler", "lock_rotation", context.active_pose_bone);
                        
                    lc_rot.use_property_split = True;
                    lc_main_row = lc_rot.row(align = True);
                        
                    lc_row_col = lc_main_row.column(align = True);
                    lc_row_col.ui_units_x = 0.7;
                    lc_row_col.label(text=""); 
                    lc_main_row.prop(context.active_pose_bone, "rotation_mode", text="");
                    lc_main_row.operator("pose.quaternions_flip", text="", icon="GRAPH", emboss=False);  
                    lc_main.use_property_split = False;
                        
                    lc_main.separator();
                    m7a_obj_transform(lc_main, "Scale:", "transform.resize", "TRANSFORM_ORIGINS", "scale", "lock_scale", context.active_pose_bone);
                    
            elif (context.mode in {"PAINT_VERTEX"}):
                lc_main.row(align=True).prop(context.scene, "m7a_megabag_show", expand=True);
                lc_main.separator();
                lc_main_row = lc_label(lc_main, "Mesh: Paint Vertex", icon="VPAINT_HLT", asset=False);
                lc_main_row.separator();
                lc_btn = lc_main_row.operator("object.mode_set", text="", icon="OBJECT_DATA", emboss=False);
                lc_btn.mode='OBJECT'; lc_btn.toggle=False;
                lc_main.separator();
                
                if (context.scene.m7a_megabag_show == "props"):
                    lc_main.operator("paint.vertex_color_invert");
                    
                    lc_main.separator();
                    m7a_custom_properties.draw_properties(self, context, lc_main);
                    
                else: m7a_object_transform(lc_main, context);
                
            elif (context.mode in {"EDIT_CURVE"}):
                lc_main.row(align=True).prop(context.scene, "m7a_megabag_show", expand=True);
                lc_main.separator();
                lc_main_row = lc_label(lc_main, "Curve", icon="CURVE_DATA");
                lc_main_row.separator();
                lc_btn = lc_main_row.operator("object.mode_set", text="", icon="MOD_CURVE", emboss=False);
                lc_btn.mode='OBJECT'; lc_btn.toggle=False;
                lc_main.separator();
                
                if (context.scene.m7a_megabag_show == "props"):
                    m7a_curve.draw_properties(self, context, lc_main);
                else: m7a_object_transform(lc_main, context);
                
            elif (context.mode in {"EDIT_ARMATURE"}):
                lc_main.row(align=True).prop(context.scene, "m7a_megabag_show", expand=True);
                lc_main.separator();
                
                if (context.scene.m7a_megabag_show == "props"):
                    pass
                else:
                    m7a_obj_transform(lc_main, "Head:", "transform.translate", "OBJECT_ORIGIN", "head", "", context.active_bone);
                    
                    lc_main.separator();
                    
                    m7a_obj_transform(lc_main, "Tail:", "transform.translate", "OBJECT_ORIGIN", "tail", "", context.active_bone);
                    
                    lc_main.separator();
                    
                    lc_main.prop(context.active_bone, "roll");
                    lc_main.prop(context.active_bone, "length");
                    
                    lc_main.separator();
                    
                    lc_row = lc_main.row(align = True);
                    lc_row.prop(a_obj.data, "display_type", text='');
                    
                    if (a_obj.data.display_type == 'BBONE'):
                        lc_row.operator("transform.transform", text='', icon='RESTRICT_SELECT_ON').mode="BONE_SIZE";
                        
                        lc_main.prop(context.active_bone, "bbone_x", text="X");
                        lc_main.prop(context.active_bone, "bbone_z", text="Z");
                        
            elif (context.mode in {"EDIT_MESH"}):
                lc_main.row(align=True).prop(context.scene, "m7a_megabag_show", expand=True);
                lc_main.separator();
                lc_main_row = lc_label(lc_main, "Mesh", icon="MESH_DATA");
                lc_main_row.separator();
                lc_btn = lc_main_row.operator("object.mode_set", text="", icon="OBJECT_DATAMODE", emboss=False);
                lc_btn.mode='OBJECT'; lc_btn.toggle=False;
                lc_main.separator();
                
                if (context.scene.m7a_megabag_show == "props"):
                    if (lc_scene.m7a_megabag_category not in {'simple', 'scripts', 'other'}):
                        lc_cont = lc_split_row(lc_main, 140);
                    else: lc_cont = lc_main;
                    lc_cont.prop(lc_scene, "m7a_megabag_category", text="");
                    if (lc_scene.m7a_megabag_category not in {'humans'}):
                        lc_cont_x(lc_cont, 8).prop(lc_scene, "m7a_megabag_subcategory", text="");
                        
                    if (lc_scene.m7a_megabag_category not in {'simple', 'scripts', 'other'}):
                        if (lc_scene.m7a_megabag_category in {'clothes'}):
                            lc_main.prop(lc_scene, "m7a_megabag_parts", text="");
                        else:
                            lc_cont = lc_split_row(lc_main, 140);
                            lc_cont_x(lc_cont, 7).prop(lc_scene, "m7a_megabag_type", text="");
                            lc_cont.prop(lc_scene, "m7a_megabag_parts", text="");
                    
                    if (ver_less(2,80,0)): lc_main.separator();
                    lc_main.template_icon_view(lc_scene, "m7a_megabag_viewer", show_labels = True);
                    
                    lc_row = lc_main.row(align = True);
                    if (lc_scene.m7a_megabag_category in {'scripts'}) or (lc_scene.m7a_megabag_subcategory in {'script'}):
                        lc_label = "Run Script"; lc_option = "RUN_SCRIPT_IN_OBJECT";
                    else:
                        lc_label = "Add Mesh in Object"; lc_option = "ADD_MESH_IN_OBJECT";
                    if (ver_more(2,80,0)):
                        lc_row.operator("m7a.megabag_button", text=lc_label, icon="BACK").option = lc_option;
                        lc_row.operator("m7a.quickpack_info", text="", icon="QUESTION");
                    else:
                        lc_row.operator("m7a.quickpack_info", text="", icon="QUESTION");
                        lc_row.operator("m7a.megabag_button", text=lc_label, icon="FORWARD").option = lc_option;
                
                    lc_main.separator();
                    lc_row = lc_main.row(align = True);
                    if (context.region.width > 140):
                        lc_row.operator("transform.translate", text="Move", icon="OBJECT_ORIGIN" if (ver_more(3,0,0)) else "MAN_TRANS");
                        if (context.region.width > 210):
                            lc_row.operator("transform.rotate", text="Rotate", icon="ORIENTATION_GIMBAL" if (ver_more(3,0,0)) else "MAN_ROT");
                            lc_row.operator("transform.resize", text="Scale", icon="TRANSFORM_ORIGINS" if (ver_more(3,0,0)) else "MAN_SCALE");
                        else:
                            lc_row.operator("transform.rotate", text="", icon="ORIENTATION_GIMBAL" if (ver_more(3,0,0)) else "MAN_ROT");
                            lc_row.operator("transform.resize", text="", icon="TRANSFORM_ORIGINS" if (ver_more(3,0,0)) else "MAN_SCALE");
                    else:
                        lc_row.operator("transform.translate", text=" ", icon="OBJECT_ORIGIN" if (ver_more(3,0,0)) else "MAN_TRANS");
                        lc_row.operator("transform.rotate", text=" ", icon="ORIENTATION_GIMBAL" if (ver_more(3,0,0)) else "MAN_ROT");
                        lc_row.operator("transform.resize", text=" ", icon="TRANSFORM_ORIGINS" if (ver_more(3,0,0)) else "MAN_SCALE");
                    
                    lc_row = lc_main.row(align = True);
                    if (ver_more(3,0,0)): lc_row.prop(bpy_preferences().view, 'gizmo_size', text='Gismo Size:');
                    else: lc_row.prop(bpy_preferences().view, 'manipulator_size', text='Gismo Size:');
                    lc_btn = lc_row.operator("m7a.megabag_button", text="", icon="X");
                    lc_btn.option = "RESET_GISMO_SIZE";
                    lc_btn_description(lc_btn, 'Reset Gismo Size');
                    
                    lc_main.separator();
                    
                    lc_row = lc_main.row(align = True);
                    lc_row.operator("mesh.symmetrize", icon="MOD_MIRROR");
                    lc_row = lc_row.row(align = True);
                    lc_row.menu("VIEW3D_MT_edit_mesh_normals", icon="NORMALS_FACE" if (ver_more(3,0,0)) else "SNAP_NORMAL");
                    lc_row.scale_x = 0.9;
                    
                    lc_row = lc_main.row(align = True);
                    lc_row.operator("mesh.separate", icon="NLA_PUSHDOWN", text="Separate Selected").type = 'SELECTED';
                    lc_row.operator("mesh.separate", icon="MATERIAL_DATA", text="").type = 'MATERIAL';
                    lc_row.operator("mesh.separate", icon="STICKY_UVS_DISABLE", text="").type = 'LOOSE';
                    
                    lc_main.separator();
                    
                    lc_row = lc_main.row(align = True);
                    lc_row.operator_menu_enum("mesh.merge", "type", text="Merge", icon="AUTOMERGE_ON");
                    lc_row.operator("mesh.merge", text="", icon="CENTER_ONLY" if (ver_more(3,0,0)) else "FULLSCREEN_EXIT").type="CENTER";
                    lc_row.operator("mesh.remove_doubles", text="", icon="CON_DISTLIMIT" if (ver_more(3,0,0)) else "ARROW_LEFTRIGHT");
                    lc_row.separator();
                    if (ver_more(3,0,0)): lc_row.operator("mesh.edge_split", text="", icon="MOD_EDGESPLIT").type = 'EDGE';
                    else: lc_row.operator("mesh.edge_split", text="", icon="MOD_EDGESPLIT");
                    
                    lc_main.separator();
                    
                    lc_main.operator("transform.shrink_fatten", icon="CON_SHRINKWRAP" if (ver_more(3,0,0)) else "FULLSCREEN_EXIT");
                    
                    lc_main.separator();
                    
                    lc_row = lc_main.row(align = True);
                    lc_row.operator("mesh.mark_sharp");
                    lc_row.operator("mesh.mark_sharp", icon="X", text="").clear = True;
                                        
                    lc_main.separator();

                    lc_row = lc_main.row(align = True);
                    lc_row.menu("VIEW3D_MT_edit_mesh_delete", icon="TRASH" if (ver_more(3,0,0)) else "X");
                    lc_row.prop(context.active_object, "display_type", text="", icon="VIS_SEL_10" if ver_more(3,0,0) else "RESTRICT_VIEW_OFF");
                    
                    lc_main.separator();
                    
                    m7a_mesh.draw_properties(self, context, lc_main);
                else:
                    pass
                
        else:
            lc_main.separator();
            lc_row = lc_main.row(align = True);
            lc_row.alignment = "CENTER";
            lc_row.label(text="No selected objects.");
            
def m7a_object_transform(lc_main, context):
    m7a_obj_transform(
        lc_main, "Location:", "transform.translate", 
        "OBJECT_ORIGIN" if (ver_more(3,0,0)) else "MAN_TRANS", 
        "location", "lock_location"
    );
    lc_main.separator();
    lc_rot = m7a_obj_transform(
        lc_main, "Rotation:", "transform.rotate", 
        "ORIENTATION_GIMBAL" if (ver_more(3,0,0)) else "MAN_ROT", 
        "rotation_euler", "lock_rotation"
    );
                        
    if (ver_more(3,0,0)): lc_rot.use_property_split = True;
    lc_main_row = lc_rot.row(align = True);
                        
    lc_row_col = lc_main_row.column(align = True);
    lc_width(lc_row_col, 0.7, 0.1);
    lc_row_col.label(text=""); 
    lc_main_row.prop(context.active_object, "rotation_mode", text="");
    lc_main_row.label(text="", icon="BLANK1"); 
    if (ver_more(3,0,0)): lc_main.use_property_split = False;
                        
    lc_main.separator();
    m7a_obj_transform(
        lc_main, "Scale:", "transform.resize", 
        "TRANSFORM_ORIGINS" if (ver_more(3,0,0)) else "MAN_SCALE", 
        "scale", "lock_scale"
    );
    lc_main.separator();
    m7a_obj_transform(lc_main, "Dimensions:", "", "CUBE" if (ver_more(3,0,0)) else "BBOX", "dimensions", "");
    
def m7a_obj_transform(lc_main, label, action_id, icon, path_id, lock_id, path = ""):
    #lc_main = lc_main.box().column(align = True);
    lc_row = lc_main.row(align = True);
    lc_row.label(text=label, icon=icon);
    if not (action_id == ""):
        lc_row.operator(
            action_id, text="", 
            icon="RESTRICT_SELECT_ON" if (ver_more(3,0,0)) else "RESTRICT_SELECT_OFF", 
            emboss=False
        );
    
    if (path == ""): path = bpy.context.active_object;
    
    def item(id, w = False, id_w = "lock_rotation_w"):
        lc_main_row = lc_main.row(align = True); 
        
        if (ver_more(3,0,0)): 
            lc_row_col = lc_main_row.column(align = True);
            lc_width(lc_row_col, 0.7, 0.1);
            if (w == True): lc_row_col.label(text="W:");
            lc_row_col.label(text="X:"); lc_row_col.label(text="Y:"); lc_row_col.label(text="Z:");
        
        if not (lock_id == ""): 
            lc_row_col = lc_main_row.column(align = True);
            lc_width(lc_row_col, 1, 1);
            if (w == True):
                lc_btn = lc_row_col.operator("m7a.megabag_button", text="", icon="PANEL_CLOSE")
                lc_btn.option = "CLEAR_"+str(id).upper()+"_W";
                lc_btn_description(lc_btn, "Clear " + str(id) + " [w]");
            lc_btn = lc_row_col.operator("m7a.megabag_button", text="", icon="PANEL_CLOSE");
            lc_btn.option = "CLEAR_"+str(id).upper()+"_X";
            lc_btn_description(lc_btn, "Clear " + str(id) + " [x]");
            lc_btn = lc_row_col.operator("m7a.megabag_button", text="", icon="PANEL_CLOSE");
            lc_btn.option = "CLEAR_"+str(id).upper()+"_Y";
            lc_btn_description(lc_btn, "Clear " + str(id) + " [y]");
            lc_btn = lc_row_col.operator("m7a.megabag_button", text="", icon="PANEL_CLOSE");
            lc_btn.option = "CLEAR_"+str(id).upper()+"_Z";
            lc_btn_description(lc_btn, "Clear " + str(id) + " [z]");
               
        if (lock_id == ""): 
            lc_row = lc_main_row.column(align = True);
            lc_row.prop(path, id, text="");
        else:
            if (ver_more(3,0,0)):
                lc_row = lc_main_row.row(align = True);
                lc_row.use_property_split = True;
                lc_row.prop(path, id, text="");
            else:
                lc_row = lc_main_row.column(align = True);
                lc_row.prop(path, id, text="");
                
        if not (lock_id == ""): 
            if (ver_more(3,0,0)):
                lc_row.use_property_decorate = False;
                lc_roc = lc_row.column(align = True);
            else: lc_roc = lc_main_row.column(align = True);
            if (ver_more(3,0,0)):
                if (w == True): lc_roc.prop(path, id_w, text="", emboss=False, icon='DECORATE_UNLOCKED');
                lc_roc.prop(path, lock_id, text="", emboss=False, icon='DECORATE_UNLOCKED');
            else:
                if (w == True): lc_roc.prop(path, id_w, text="", icon="UNLOCKED");
                lc_roc.prop(path, lock_id, text="", icon='UNLOCKED');
                
    if (path_id == "rotation_euler"):
        if (path.rotation_mode == 'QUATERNION'):
            item("rotation_quaternion", True);
        elif (path.rotation_mode == 'AXIS_ANGLE'):
            item("rotation_axis_angle", True);
        else: item(path_id);
    else: item(path_id)
    
    return lc_main;

class M7A_VIEW3D_QP_BTN_Info(Operator):
    bl_idname       = 'm7a.quickpack_info';
    bl_label        = 'Info';
    bl_description  = 'Info about items in Quick Pack';
    
    @staticmethod
    def draw(self, context):
        lc_main = self.layout.column(align = True);
        lc_main.label(text="Commercial Info:", icon="QUESTION");
        lc_main.separator(); lc_icon = "DOT" if ver_more(2,80,0) else "LAYER_ACTIVE";
        lc_main.label(text=" All   meshes  in   this   ''Quick Pack''  modeled", icon=lc_icon);
        lc_main.label(text="  by   3DMish   (Mish7913),     under   CC0   Licence");
        lc_main.label(text="  [Public Domain], it's absolutly free for commercial");
        lc_main.label(text="  and non-commercial use, fill free to use it...");
    
    def invoke(self, context, event):
        context.window_manager.invoke_popup(self, width=265);
        return {'RUNNING_MODAL'}
        
    def execute(self, context): return {'FINISHED'};

def m7a_quick_pack_set_subcategory(self, context):
    global bl_conf;
    
    if (hasattr(context.scene, "m7a_megabag_category")):
        category = context.scene.m7a_megabag_category;
    
        if (category in ['a_birds']):
            bl_conf["subcategory"] = [
                ("", "-----", ""),
                ("chicken", "Chicken", "Mesh list of chicken's parts"),
                ("duck",    "Duck",    "Mesh list of duck's parts"),
                ("goose",   "Goose",   "Mesh list of goose's parts"),
                ("swan",    "Swan",    "Mesh list of swan's parts"),
                
                ("", "----", ""),
                ("sparrow", "Sparrow", "Mesh list of sparrow's parts"),
                ("eagle",   "Eagle",   "Mesh list of eagle's parts"),
                ("hawk",    "Hawk",    "Mesh list of hawk's parts"),
                ("heron",   "Heron",   "Mesh list of heron's parts"),
                ("penguin", "Penguin", "Mesh list of penguin's parts"),
                ("ostrich", "Ostrich", "Mesh list of ostrich's parts"),
                
                ("", "Parrots", ""),
                ("budgerigar",  "Budgerigar",  "Mesh list of budgerigar's parts"),
                ("blue_macaw",  "Blue Macaw",  "Mesh list of macaw's parts"),
                ("red_macaw",   "Red Macaw",   "Mesh list of macaw's parts"),
                ("cockatoo",    "Cockatoo",    "Mesh list of cockatoo's parts"),
            ];
            
        elif (category in ['a_cattles']):
            bl_conf["subcategory"] = [
                ("", "Farm Cattles", ""),
                ("cow",   "Cow",   "Mesh list of cow's parts"),
                ("goat",  "Goat",  "Mesh list of goat's parts"),
                ("horse", "Horse", "Mesh list of horse's parts"),
                ("pony",  "Pony",  "Mesh list of pony's parts"),
                ("sheep", "Sheep", "Mesh list of sheep's parts"),
                
                ("", "Wild Cattles", ""),
                ("antelope", "Antelope", "Mesh list of antelope's parts"),
                ("camel",    "Camel",    "Mesh list of camel's parts"),
                ("deer",     "Deer",     "Mesh list of pony's parts"),
                ("elephant", "Elephant", "Mesh list of elephant's parts"),
            ];
            
        elif (category in ['a_beasts']):
            bl_conf["subcategory"] = [
                ("", "Cats", ""),
                ("cat",     "Cat",     "Mesh list of cat's parts"),
                ("cheetah", "Cheetah", "Mesh list of cheetah's parts"),
                ("leopard", "Leopard", "Mesh list of leopard's parts"),
                ("lion",    "Lion",    "Mesh list of lion's parts"),
                ("tigger",  "Tigger",  "Mesh list of tigger's parts"),
                
                ("", "Dogs", ""),
                ("dog",    "Dog",    "Mesh list of dog's parts"),
                ("coyote", "Coyote", "Mesh list of coyote's parts"),
                ("fox",    "Fox",    "Mesh list of fox's parts"),
                ("wolf",   "Wolf",   "Mesh list of wolf's parts"),
                
                ("", "Beras", ""),
                ("brown_bear",   "Brown Bear",   "Mesh list of bear's parts"),
                ("grizzly_bear", "Grizzly Bear", "Mesh list of bear's parts"),
                ("polar_bear",   "Polar Bear",   "Mesh list of bear's parts"),
                ("panda",        "Panda",        "Mesh list of panda's parts"),
            ];
            
        elif (category in ['a_rodent']):
            bl_conf["subcategory"] = [
                ("", "Rodents", ""),
                ("mouse", "Mouse", "Mesh list of mouse's parts"),
                ("rat",   "Rat",   "Mesh list of rat's parts"),
            ];
            
        elif (category in ['a_reptiles']):
            bl_conf["subcategory"] = [
                ("", "Snakes", ""),
                ("cobra", "Cobra", "Mesh list of cobra's parts"),
            ];
            
        elif (category in ['a_insects']):
            bl_conf["subcategory"] = [
                ("", "------", ""),
                ("ant", "Ant", "Mesh list of ant's parts"),
                
                ("", "Bugs", ""),
                ("ladybug", "Ladybug", "Mesh list of ladybug's parts"),
                
                ("", "Spiders", ""),
                ("tarantula", "Tarantula", "Mesh list of tarantula's parts"),
                
                ("", "------", ""),
                ("butterfly", "Butterfly", "Mesh list of butterfly's parts"),
                ("bee",       "Bee",       "Mesh list of bee's parts"),
                ("fly",       "Fly",       "Mesh list of fly's parts"),
            ];
            
        elif (category in ['clothes']):
            bl_conf["subcategory"] = [
                ("", "Clothes", ""),
                ("mesh",   "Meshes",  "Mesh list of clothes's parts"),
                ("script", "Scripts", "Script list of clothes effect"),
            ];
            
        elif (category in ['simple']):
            bl_conf["subcategory"] = [
                ("", "Simple Meshes", ""),
                ("geometric",  "Geometric",  "Mesh list of geometric figures objects"),
            ];
            
        elif (category in ['scripts']):
            bl_conf["subcategory"] = [
                ("", "Scripts", ""),
                ("all",  "All",  "All Scripts"),
            ];
            
        elif (category in ['other']):
            bl_conf["subcategory"] = [
                ("", "Furnitures", ""),
                ("handle",  "Handle",  "Mesh list of handles"),
                ("keyhole", "Keyhole", "Mesh list of keyholes"),
                
                ("", "Technology", ""),
                ("wheel",  "Wheel",  "Mesh list of wheels"),
            ];
            
        else: bl_conf["subcategory"] = [];
    else: bl_conf["subcategory"] = [];
    
    m7a_megabag_viewer_upd(self, context);

def m7a_quick_pack_get_subcategory(self, context): global bl_conf; return bl_conf["subcategory"];

def m7a_quick_pack_get_items(self, context):
    global bl_conf; result = [];
    
    category = context.scene.m7a_megabag_category;
    subcategory = context.scene.m7a_megabag_subcategory;
    type = context.scene.m7a_megabag_type;
    parts = context.scene.m7a_megabag_parts;
    
    def add_item(view_list, items):
        items = list(items); items.sort();
        for item in items:
            image = data_path + "/m7a_img/" + item[1];
            if (image in lc_prew): thumb = lc_prew[image];
            else: thumb = lc_prew.load(image, image, 'IMAGE');
            view_list.append( (item[1], item[2], item[3], thumb.icon_id, item[0]) );
        
    if (category in m7a_meshes.keys()):
        if (category in {'humans'}):
            if (type in m7a_meshes[category].keys()):
                if (parts in m7a_meshes[category][type].keys()):
                    if (m7a_meshes[category][type][parts] != []):
                        add_item(result, m7a_meshes[category][type][parts]);
        elif (category in {'clothes'}):
            if (subcategory in m7a_meshes[category].keys()):
                if (parts in m7a_meshes[category][subcategory].keys()):
                    if (m7a_meshes[category][subcategory][parts] != []):
                        add_item(result, m7a_meshes[category][subcategory][parts]);
        elif (category in {'simple', 'scripts', 'other'}):
            if (subcategory in m7a_meshes[category].keys()):
                if (m7a_meshes[category][subcategory] != []):
                    add_item(result, m7a_meshes[category][subcategory]);
        else:
            if (subcategory in m7a_meshes[category].keys()):
                if (type in m7a_meshes[category][subcategory].keys()):
                    if (parts in m7a_meshes[category][subcategory][type].keys()):
                        if (m7a_meshes[category][subcategory][type][parts] != []):
                            add_item(result, m7a_meshes[category][subcategory][type][parts]);
    
    bl_conf["tmp_items"] = result;
    return result;
    
def m7a_quick_pack_get_parts(self, context):
    global bl_conf; result = [];
    
    category = context.scene.m7a_megabag_category;
    subcategory = context.scene.m7a_megabag_subcategory;
    type = context.scene.m7a_megabag_type;
    
    if (category in m7a_meshes.keys()):
        if (category in {'humans'}):
            if (type in m7a_meshes[category].keys()):
                for key in m7a_meshes[category][type].keys():
                    if (m7a_meshes[category][type][key] != []):
                        label = (key[0:1].upper()+key[1:]).replace("Base_forms", "Base Forms");
                        result.append( (key, label, 'Mesh list of '+key) );
        elif (category in {'clothes'}):
            if (subcategory in m7a_meshes[category].keys()):
                for key in m7a_meshes[category][subcategory].keys():
                    if (m7a_meshes[category][subcategory][key] != []):
                        label = (key[0:1].upper()+key[1:]).replace("Base_forms", "Base Forms");
                        result.append( (key, label, 'Mesh list of '+key) );
        else:
            if (subcategory in m7a_meshes[category].keys()):
                if (type in m7a_meshes[category][subcategory].keys()):
                    for key in m7a_meshes[category][subcategory][type].keys():
                        if (m7a_meshes[category][subcategory][type][key] != []):
                            label = (key[0:1].upper()+key[1:]).replace("Base_forms", "Base Forms");
                            result.append( (key, label, 'Mesh list of '+key) );
        
    return result;
    
def m7a_get_list_remember_objects(self):
    result = "";
    if (len(m7a_rem.bl_conf["OBJECT"]) > 0):
        for i, obj in enumerate(m7a_rem.bl_conf["OBJECT"], start = 0):
            try: result += ", " + obj.name if (i != 0) else obj.name; i += 1;
            except: del m7a_rem.bl_conf["OBJECT"][i];
    return result;

class M7A_OBJECT_MT_ADD_Prop(Menu):
    bl_idname      = 'M7A_OBJECT_MT_ADD_Prop';
    bl_label       = 'ADD Property';
    bl_description = 'Add custom property to object';
    
    @staticmethod
    def draw(self, context):
        lc_main = self.layout.column(align = True);
        lc_main.operator("wm.properties_add", text="to Object").data_path = "object";
        lc_main.operator("wm.properties_add", text="to Data").data_path = "object.data";
        if (context.object.type == 'ARMATURE') and (context.selected_pose_bones) and (context.active_pose_bone):
            lc_main.operator("wm.properties_add", text="to Bone").data_path = "active_pose_bone";

def m7a_megabag_viewer_upd(self, context):
    global bl_conf;
    
    if (context.scene.m7a_megabag_viewer == ''):
        if not (bl_conf["tmp_items"] == []):
            context.scene.m7a_megabag_viewer = bl_conf["tmp_items"][0][0];

classes = (
    M7A_VIEW3D_PT_QUICK_Pack, M7A_VIEW3D_QP_BTN_Info, M7A_OBJECT_MT_ADD_Prop,
);

def register():
    for cls in classes:
        try: bpy.utils.register_class(cls);
        except: pass
    
    lc_manager.m7a_megabag_category = EnumProperty(
        name="Category",
        items=[
            ("", "Humans", ""),
            ("humans",   "Humans",            "Mesh list of human's body parts"),
            
            ("", "Animals", ""),
            ("a_birds",    "Birds",           "Mesh list of animals: bird's body parts"),
            ("a_cattles",  "Cattles",         "Mesh list of animals: cattle`'s body parts"),
            ("a_beasts",   "Beasts",          "Mesh list of animals: beast's body parts"),
            ("a_rodent",   "Rodents",         "Mesh list of animals: rodent's body parts"),
            ("a_reptiles", "Reptiles",        "Mesh list of animals: reptiles body parts"),
            ("a_insects",  "Insects",         "Mesh list of animals: insect's body parts"),
            
            ("", "Other", ""),
            ("simple",     "Simple Meshes",   "Mesh list of simple figures"),
            ("clothes",    "Clothes",         "Mesh list of clothe's parts"),
            ("scripts",    "Python Scripts",  "Scripts list"),
            ("other",      "Other Stuff",     "Mesh list of other stuff"),
        ], 
        default="humans",
        update=m7a_quick_pack_set_subcategory,
    );
    
    lc_manager.m7a_megabag_subcategory = EnumProperty(
        name="SubCategory", items=m7a_quick_pack_get_subcategory,
        update=m7a_megabag_viewer_upd,
    );
    
    lc_manager.m7a_megabag_type = EnumProperty(
        items=[("male", "Male", "Male"), ("female", "Female", "Female")],
        default="male", name="",
        update=m7a_megabag_viewer_upd,
    );
    
    lc_manager.m7a_megabag_show = EnumProperty(
        items=[("transform", "Transform", "Transform"), ("props", "Properties", "Properties")],
    );
    
    lc_manager.m7a_megabag_parts        = EnumProperty(items=m7a_quick_pack_get_parts, name="");
    lc_manager.m7a_megabag_viewer       = EnumProperty(items=m7a_quick_pack_get_items, name="");
    
    lc_manager.m7a_megabag_memory_keys  = StringProperty(get=m7a_get_list_remember_objects);
    
    lc_manager.m7a_megabag_show_keys    = BoolProperty(name="Keyframes");
    lc_manager.m7a_megabag_shape_keys   = BoolProperty(name="Shape Keys");
    lc_manager.m7a_megabag_show_props   = BoolProperty(name="Custom Properties");
    lc_manager.m7a_megabag_keep_pose    = BoolProperty(name="Keep Pose", default=True);
    

def unregister():
    for cls in classes:
        try: bpy.utils.unregister_class(cls);
        except: pass
    
    r_remove_attr(lc_manager, "m7a_megabag_shape_keys");
    r_remove_attr(lc_manager, "m7a_megabag_keep_pose");
    r_remove_attr(lc_manager, "m7a_megabag_show_props");
    r_remove_attr(lc_manager, "m7a_megabag_memory_keys");
    r_remove_attr(lc_manager, "m7a_megabag_category");
    r_remove_attr(lc_manager, "m7a_megabag_subcategory");
    r_remove_attr(lc_manager, "m7a_megabag_type");
    r_remove_attr(lc_manager, "m7a_megabag_parts");
    r_remove_attr(lc_manager, "m7a_megabag_viewer");
    r_remove_attr(lc_manager, "m7a_megabag_show");
    r_remove_attr(lc_manager, "m7a_megabag_custom_props");
