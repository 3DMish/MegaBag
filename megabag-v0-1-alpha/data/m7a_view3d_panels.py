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
Vi3D = "VIEW3D_PT_";

bl_conf = {
    "VIEW3D_PT_tools_transform": None, "VIEW3D_PT_tools_object": None, "VIEW3D_PT_tools_add_object": None,
    "VIEW3D_PT_tools_relations": None, "VIEW3D_PT_tools_animation": None, "VIEW3D_PT_tools_rigid_body": None,
    "VIEW3D_PT_tools_transform_mesh": None, "VIEW3D_PT_tools_meshedit": None, "VIEW3D_PT_tools_meshweight": None,
    "VIEW3D_PT_tools_add_mesh_edit": None, "VIEW3D_PT_tools_shading": None, "VIEW3D_PT_tools_projectpaint": None,
    "VIEW3D_PT_tools_meshedit_options": None, "VIEW3D_PT_tools_transform_curve": None, "VIEW3D_PT_tools_curveedit": None,
    "VIEW3D_PT_tools_add_curve_edit": None, "VIEW3D_PT_tools_curveedit_options_stroke": None,
    "VIEW3D_PT_tools_transform_surface": None, "VIEW3D_PT_tools_surfaceedit": None, "VIEW3D_PT_tools_add_surface_edit": None,
    "VIEW3D_PT_tools_textedit": None, "VIEW3D_PT_tools_armatureedit": None, "VIEW3D_PT_tools_armatureedit_transform": None,
    "VIEW3D_PT_tools_armatureedit_options": None, "VIEW3D_PT_tools_mballedit": None, "VIEW3D_PT_tools_add_mball_edit": None,
    "VIEW3D_PT_tools_latticeedit": None, "VIEW3D_PT_tools_posemode": None, "VIEW3D_PT_tools_posemode_options": None,
    "VIEW3D_PT_imapaint_tools_missing": None, "VIEW3D_PT_tools_brush": None, "VIEW3D_PT_slots_projectpaint": None,
    "VIEW3D_PT_stencil_projectpaint": None, "VIEW3D_PT_tools_brush_overlay": None, "VIEW3D_PT_tools_brush_texture": None,
    "VIEW3D_PT_tools_mask_texture": None, "VIEW3D_PT_tools_brush_stroke": None, "VIEW3D_PT_tools_brush_curve": None,
    "VIEW3D_PT_sculpt_dyntopo": None, "VIEW3D_PT_sculpt_options": None, "VIEW3D_PT_sculpt_symmetry": None,
    "VIEW3D_PT_tools_brush_appearance": None, "VIEW3D_PT_tools_weightpaint": None, "VIEW3D_PT_tools_weightpaint_options": None,
    "VIEW3D_PT_tools_vertexpaint": None, "VIEW3D_PT_tools_imagepaint_external": None, "VIEW3D_PT_tools_uvs": None,
    "VIEW3D_PT_tools_imagepaint_symmetry": None, "VIEW3D_PT_tools_particlemode": None, "VIEW3D_PT_tools_history": None,
    "VIEW3D_PT_tools_grease_pencil": None, "VIEW3D_PT_tools_grease_pencil_draw": None, "VIEW3D_PT_tools_grease_pencil_edit": None,
    "VIEW3D_PT_tools_grease_pencil_interpolate": None, "VIEW3D_PT_tools_grease_pencil_sculpt": None,
    "VIEW3D_PT_tools_grease_pencil_brush": None, "VIEW3D_PT_tools_grease_pencil_brushcurves": None,
}

class VIEW3D_PT_tools_transform(Panel):
    bl_space_type  = 'VIEW_3D';
    bl_region_type = 'TOOLS';
    bl_category    = "Tools";
    bl_label       = "Tools";

    def draw(self, context):
        lc_main = self.layout.column(align=True);
        lc_width = context.region.width;
        lc_obj = context.active_object;
                        
        lc_cont = lc_split_row(lc_main, 170);
        lc_cont.scale_y = 1.5;
        lc_cont.operator("transform.translate", text="Move", icon="OBJECT_ORIGIN" if (ver_more(2,90,0)) else "MAN_TRANS");
        lc_cont.operator("transform.rotate", text="Rotate", icon="ORIENTATION_GIMBAL" if (ver_more(2,90,0)) else "MAN_ROT");
        
        if (lc_width >= 170) and (lc_width <= 300) and (context.mode in {"OBJECT"}):
            lc_cont = lc_main.row(align=True);
            lc_cont.scale_y = 1.5;
            lc_text = "Scale";
        elif (context.mode in {"EDIT_MESH"}):
            lc_text = "Scale" if (context.region.width <= 170) or (context.region.width > 300) else "";
        else: lc_text = "Scale";
        
        lc_cont.operator("transform.resize", text=lc_text, icon="TRANSFORM_ORIGINS" if (ver_more(2,90,0)) else "MAN_SCALE");
        
        if (context.mode in {"OBJECT"}):
            lc_cont.operator("transform.mirror", text="Mirror", icon="MOD_MIRROR");
            
        if (context.mode in {"EDIT_MESH"}):
            
            lc_cont = lc_split_row(lc_main, 170);
            
            lc_cont_btn = lc_cont.row(align=True);
            lc_cont_btn.scale_y = 1.5;
            lc_cont_btn.operator("transform.shrink_fatten", text="Shrink/Fatten", icon="SPHERECURVE");
            
            lc_cont_btn = lc_cont.row(align=True);
            lc_cont_btn.scale_x = 0.8;
            lc_cont_btn.scale_y = 1.5;
            lc_cont_btn.operator("transform.push_pull", text="Push/Pull", icon="SMOOTHCURVE");
            
        lc_main.separator();
        
        lc_main.prop(lc_obj, "draw_type", text="", icon="VISIBLE_IPO_ON");
        
        if (context.mode in {"OBJECT"}):
            lc_main.separator();
        
            lc_cont = lc_split_row(lc_main, 140);
            lc_cont.operator_menu_enum("object.origin_set", "type", text="Set Origin");
            lc_cont.menu("VIEW3D_MT_object_apply", text="Apply");
            
            lc_main.separator();
            
            lc_cont = lc_split_row(lc_main, 140);
            lc_cont_x(lc_cont, 6.5).operator("object.duplicate_move", text="Duplicate");
            lc_text = "Duplicate Linked" if (context.region.width <= 140) or (context.region.width > 160) else "Dup. Linked";
            lc_cont.operator("object.duplicate_move_linked", text=lc_text);
            
            lc_cont = lc_split_row(lc_main, 140);
            lc_cont.operator("object.join");
            lc_cont.operator("object.delete");

            lc_main.separator();
            
            lc_cont = lc_split_row(lc_main, 140);
            lc_text = "Shade Smooth" if (context.region.width <= 140) or (context.region.width > 180) else "Smooth";
            lc_cont.operator("object.shade_smooth", text=lc_text);
            lc_text = "Shade Flat" if (context.region.width <= 140) or (context.region.width > 180) else "Flat";
            lc_cont_x(lc_cont, 8).operator("object.shade_flat", text=lc_text);
            
        elif (context.mode in {"EDIT_MESH"}):
            lc_main.separator();
            
            lc_cont = lc_split_row(lc_main, 140);
            lc_cont.operator("mesh.duplicate_move", text="Duplicate");
            lc_cont.menu("VIEW3D_MT_edit_mesh_delete", text="Delete");

            lc_main.separator();
            
            lc_cont = lc_split_row(lc_main, 140);
            lc_text = "Shade Smooth" if (context.region.width < 140) or (context.region.width > 180) else "Smooth";
            lc_cont.operator("mesh.faces_shade_smooth", text=lc_text);
            lc_text = "Shade Flat" if (context.region.width < 140) or (context.region.width > 180) else "Flat";
            lc_cont_x(lc_cont, 8).operator("mesh.faces_shade_flat", text=lc_text);

            lc_main.separator();
            
            lc_main.label(text="Edit Mesh:");
            
            lc_cont = lc_split_row(lc_main, 150);
            lc_cont.menu("VIEW3D_MT_menu_extrude", text="Extrude");
            lc_cont.operator("view3d.edit_mesh_extrude_move_normal", text="Extrude", icon="MOD_SOLIDIFY");
            
            lc_cont = lc_split_row(lc_main, 185);
            lc_cont.operator("mesh.subdivide", icon="MOD_SUBSURF");
            lc_cont.operator("mesh.unsubdivide", icon="MOD_DECIM");
            
            lc_cont = lc_split_row(lc_main, 185);
            
            lc_btn = lc_cont.operator("mesh.knife_tool", text="Knife");
            lc_btn.use_occlude_geometry = True;
            lc_btn.only_selected = False;
            
            lc_text = "Select" if (context.region.width < 185) or (context.region.width > 220) else "";
            lc_btn = lc_cont.operator("mesh.knife_tool", text=lc_text, icon="RADIOBUT_OFF");
            lc_btn.use_occlude_geometry = False;
            lc_btn.only_selected = True;
            
            lc_text = "Project" if (context.region.width < 185) or (context.region.width > 220) else "";
            lc_cont.operator("mesh.knife_project", text=lc_text, icon="RADIOBUT_ON");
            
            lc_cont = lc_split_row(lc_main, 200);
            lc_cont_x(lc_cont, 8).operator("mesh.inset", text="Inset Faces");
            lc_cont.operator("mesh.edge_face_add");
            
            lc_cont = lc_split_row(lc_main, 200);
            lc_cont.operator("mesh.loopcut_slide");
            lc_cont_x(lc_cont, 5).operator("mesh.spin");
            
            lc_main.separator();
            
            lc_cont = lc_split_row(lc_main, 190);
            lc_cont.operator("mesh.vertices_smooth", text="Smooth");
            lc_cont_x(lc_cont, 8).operator("mesh.noise");
            lc_cont.operator("transform.vertex_random", text="Random");
            
class M7A_VIEW3D_MT_MENU_extrude(Menu):
    bl_idname       = 'VIEW3D_MT_menu_extrude';
    bl_label        = 'Extrude';
    bl_description  = '';
    
    @staticmethod
    def draw(self, context):
        lc_main = self.layout.column();
        lc_main.menu("VIEW3D_MT_edit_mesh_extrude", text="Extrude");
        lc_main.separator();
        lc_main.operator("view3d.edit_mesh_extrude_move_normal", text="Extrude Region");
        lc_main.operator("view3d.edit_mesh_extrude_individual_move", text="Extrude Individual");
        
class VIEW3D_PT_tools_grease_pencil(Panel):
    bl_space_type  = 'VIEW_3D';
    bl_region_type = 'TOOLS';
    bl_category    = "Grease Pencil";
    bl_label       = "Grease Pencil";

    @classmethod
    def poll(cls, context):
        if (ver_more(2,79,0)): return True;
        else: return False;
        
    def draw(self, context):
        lc_main = self.layout.column(align=True);
        lc_tool_settings = context.tool_settings;
        
        lc_icon = "VISIBLE_IPO_ON" if (context.space_data.show_grease_pencil) else "VISIBLE_IPO_OFF";
        lc_main.prop(context.space_data, "show_grease_pencil", text="Show Grease Pencil", icon=lc_icon, toggle=True);
        
        lc_main.separator();
        
        lc_row = lc_main.row(align=True);
        lc_row.operator("gpencil.draw", icon='GREASEPENCIL', text="Draw").mode = 'DRAW';
        lc_row.operator("gpencil.draw", icon='FORCE_CURVE', text="Erase").mode = 'ERASER';

        lc_row = lc_main.row(align=True);
        lc_row.operator("gpencil.draw", icon='LINE_DATA', text="Line").mode = 'DRAW_STRAIGHT';
        lc_row.operator("gpencil.draw", icon='MESH_DATA', text="Poly").mode = 'DRAW_POLY';

        lc_main.separator();
        
        lc_row = lc_main.row(align=True);
        lc_row.operator("gpencil.blank_frame_add", icon='NEW');
        lc_row.operator("gpencil.active_frames_delete_all", icon='X', text="");

        lc_main.separator();
        
        lc_row = lc_main.row(align=True);
        lc_row.prop(lc_tool_settings, "use_gpencil_additive_drawing", text="Additive", toggle=True);
        lc_row.prop(lc_tool_settings, "use_gpencil_continuous_drawing", text="Continuous", toggle=True);
        lc_main.prop(lc_tool_settings, "use_gpencil_draw_onback", text="Draw on Back", toggle=True);

        lc_main.separator();
        
        if (context.space_data.type == 'VIEW_3D'):
            propname = "gpencil_stroke_placement_view3d";
        elif (context.space_data.type == 'SEQUENCE_EDITOR'):
            propname = "gpencil_stroke_placement_sequencer_preview";
        elif (context.space_data.type == 'IMAGE_EDITOR'):
            propname = "gpencil_stroke_placement_image_editor";
        else: propname = "gpencil_stroke_placement_view2d";
        
        lc_main.label(text="Stroke Placement:");
        if (context.region.width < 140): lc_cont = lc_main;
        else: lc_cont = lc_main.row(align=True);
        lc_cont.prop_enum(lc_tool_settings, propname, 'VIEW');
        lc_cont.prop_enum(lc_tool_settings, propname, 'CURSOR');

        if (context.space_data.type == 'VIEW_3D'):
            if (context.region.width < 140): lc_cont = lc_main;
            else: lc_cont = lc_main.row(align=True);
            lc_cont.prop_enum(lc_tool_settings, propname, 'SURFACE');
            lc_cont.prop_enum(lc_tool_settings, propname, 'STROKE');

cls_list = [
    Vi3D+"tools_transform",                 Vi3D+"tools_object",                    Vi3D+"tools_add_object",
    Vi3D+"tools_relations",                 Vi3D+"tools_animation",                 Vi3D+"tools_rigid_body",
    Vi3D+"tools_transform_mesh",            Vi3D+"tools_meshedit",                  Vi3D+"tools_meshweight",
    Vi3D+"tools_add_mesh_edit",             Vi3D+"tools_shading",                   Vi3D+"tools_uvs",
    Vi3D+"tools_meshedit_options",          Vi3D+"tools_transform_curve",           Vi3D+"tools_curveedit",
    Vi3D+"tools_add_curve_edit",            Vi3D+"tools_curveedit_options_stroke",  Vi3D+"tools_transform_surface",
    Vi3D+"tools_surfaceedit",               Vi3D+"tools_add_surface_edit",          Vi3D+"tools_textedit",
    Vi3D+"tools_armatureedit",              Vi3D+"tools_armatureedit_transform",    Vi3D+"tools_armatureedit_options",
    Vi3D+"tools_mballedit",                 Vi3D+"tools_add_mball_edit",            Vi3D+"tools_latticeedit",
    Vi3D+"tools_posemode",                  Vi3D+"tools_posemode_options",          Vi3D+"imapaint_tools_missing",
    Vi3D+"tools_brush",                     Vi3D+"slots_projectpaint",              Vi3D+"stencil_projectpaint",
    Vi3D+"tools_brush_overlay",             Vi3D+"tools_brush_texture",             Vi3D+"tools_mask_texture",
    Vi3D+"tools_brush_stroke",              Vi3D+"tools_brush_curve",               Vi3D+"sculpt_dyntopo",
    Vi3D+"sculpt_options",                  Vi3D+"sculpt_symmetry",                 Vi3D+"tools_brush_appearance",
    Vi3D+"tools_weightpaint",               Vi3D+"tools_weightpaint_options",       Vi3D+"tools_vertexpaint",
    Vi3D+"tools_imagepaint_external",       Vi3D+"tools_imagepaint_symmetry",       Vi3D+"tools_projectpaint",
    Vi3D+"tools_particlemode",              Vi3D+"tools_grease_pencil",             Vi3D+"tools_grease_pencil_draw",
    Vi3D+"tools_grease_pencil_edit",        Vi3D+"tools_grease_pencil_interpolate", Vi3D+"tools_grease_pencil_sculpt",
    Vi3D+"tools_grease_pencil_brush",       Vi3D+"tools_grease_pencil_brushcurves", Vi3D+"tools_history",                  
]

classes = (
    VIEW3D_PT_tools_transform, VIEW3D_PT_tools_grease_pencil, M7A_VIEW3D_MT_MENU_extrude
);

def register():
    global bl_conf;
    
    if (ver_less(2,79,5)):
        for cls in cls_list: r_unregister_class(bl_conf, cls);
        for cls in classes: bpy.utils.register_class(cls);

def unregister():
    global bl_conf;
    
    if (ver_less(2,79,5)):
        for cls in classes: bpy.utils.unregister_class(cls);
        for cls in cls_list: r_register_class(bl_conf, cls);
