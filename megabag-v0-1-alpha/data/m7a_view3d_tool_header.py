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

bl_conf = {
    "VIEW3D_HT_tool_header": None,
}

class M7A_VIEW3D_HT_Tools(Header):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_HEADER'
    
    def draw(self, context):
        lc_space_data = context.space_data;
        lc_tool_settings = context.tool_settings;
        
        lc_main = self.layout.row(align = True);
        
        lc_main.operator("ed.undo", icon="LOOP_BACK", text="");
        lc_main.operator("ed.redo", icon="LOOP_FORWARDS", text="");
        lc_main.separator();

        if (context.mode in {"OBJECT"}):
            if not (context.active_object == None):
                if (context.active_object.type in ["MESH", "CURVE", "ARMATURE"]):
                    if (context.active_object.type in ["MESH"]): lc_main.label(text="Mesh:", icon="MESH_DATA");
                    elif (context.active_object.type in ["CURVE"]): lc_main.label(text="Curve:", icon="CURVE_DATA");
                    elif (context.active_object.type in ["ARMATURE"]): lc_main.label(text="Armature:", icon="ARMATURE_DATA");
                    lc_main.separator_spacer();
                    lc_main.operator_menu_enum("object.origin_set", text="Set Origin", property="type");
                    lc_main.operator_menu_enum("m7a.object_apply", "props", icon="NONE");
                    lc_main.separator();

                    lc_main.operator("object.duplicate_move", text="", icon_value=lc_icon("DUP_MOVE"));
                    lc_main.operator("object.duplicate_move_linked", text="", icon_value=lc_icon("DUPLICATE_LINKED"));
                    
                    lc_btn = lc_main.row(align = True);
                    lc_btn.operator("object.join", icon="FORCE_LENNARDJONES", text="");
                    lc_btn.active = len(context.selected_objects) > 1;
                
                    if (context.active_object.type in {"MESH", "ARMATURE"}):
                        lc_main.separator();
                        lc_row = lc_main.row(align = True);
                        lc_row.ui_units_x = 4.5;
                        lc_row.prop(context.active_object, "display_type", text="", icon="VIS_SEL_10");
                    elif (context.active_object.type == "CURVE"):
                        lc_main.separator();
                        lc_row = lc_main.row(align = True);
                        lc_row.ui_units_x = 5.5;
                        lc_row.prop(context.active_object.data, "dimensions", expand=True);
                
                elif (context.active_object.type == "CAMERA"):
                    lc_main.label(text="Camera:", icon="CAMERA_DATA");
                    lc_main.separator_spacer();
                    lc_main.prop(context.active_object.data, "type", text="");
                    if (context.active_object.data.type != "ORTHO"):
                        lc_main.prop(context.active_object.data, "lens", text="");
                    #lc_main.separator_spacer();
                    #lc_main.prop(context.active_object.data.dof, "use_dof", toggle=True);
                    #if (context.active_object.data.dof.use_dof == True):
                    #    lc_row = lc_main.row(align = True);
                    #    lc_row.ui_units_x = 7;
                    #    lc_row.prop(context.active_object.data.dof, "focus_distance");
                    #    lc_row = lc_main.row(align = True);
                    #    lc_row.ui_units_x = 5;
                    #    lc_row.prop(context.active_object.data.dof, "aperture_fstop");
                    #    lc_main.prop(context.active_object.data, "show_limits", toggle=True);
                    
                elif (context.active_object.type == "EMPTY"):
                    lc_main.label(text="Empty:", icon="EMPTY_AXIS");
                        
                    lc_main.separator_spacer();
                                
                    lc_row = lc_main.row(align = True);
                    lc_row.ui_units_x = 5.5;
                    lc_row.prop(context.active_object, "empty_display_type", text="");
                    lc_main.separator();
                    lc_main.prop(context.active_object, "empty_display_size", text="Size");
                    if (context.active_object.empty_display_type == 'IMAGE'):
                        lc_main.separator();
                        lc_main.template_ID(context.active_object, "data", open="image.open", unlink="object.unlink_data");
                        if (context.active_object.data):
                            lc_main.separator();
                            lc_main.prop(context.active_object.data, "source", text="");
                                                                
                elif (context.active_object.type == "LIGHT"):
                    lc_main.label(text="Light:", icon="LIGHT");
                    lc_main.prop(context.active_object.data, "type", expand=True, text="");
                    lc_main.separator();
                    lc_main.prop(context.active_object.data, "use_shadow", text="SHADOW", toggle=True);
                    lc_main.separator_spacer();
                    lc_row = lc_main.row(align = True);
                    lc_row.ui_units_x = 2;
                    lc_row.prop(context.active_object.data, "color", text="");
                    lc_row = lc_main.row(align = True);
                    lc_row.ui_units_x = 5;
                    lc_row.prop(context.active_object.data, "energy", text="Power");
                    lc_row = lc_main.row(align = True);
                    lc_row.ui_units_x = 6;
                    lc_row.prop(context.active_object.data, "shadow_soft_size", text="Radius");
                
                elif (context.active_object.type == "LIGHT_PROBE"):
                    lc_main.label(text="Light Probe:", icon="OUTLINER_DATA_LIGHTPROBE");
                    lc_main.separator_spacer();
                    if (context.active_object.data.type in {"CUBEMAP"}):
                        lc_main.prop(context.active_object.data, "influence_type", text="");
                        lc_main.separator();
                    lc_main.prop(context.active_object.data, "influence_distance", text="");
                    lc_main.separator();
                    lc_main.prop(context.active_object.data, "falloff", text="");
                    lc_main.separator();
                    if (context.active_object.data.type in {"CUBEMAP", "GRID"}):
                        lc_main.prop(context.active_object.data, "intensity", text="");
                        lc_main.separator();
                        if (context.active_object.data.type in {"GRID"}):
                            lc_row = lc_main.row(align = True);
                            lc_row.ui_units_x = 7;
                            lc_row.prop(context.active_object.data, "grid_resolution_x", text="");
                            lc_row.prop(context.active_object.data, "grid_resolution_y", text="");
                            lc_row.prop(context.active_object.data, "grid_resolution_z", text="");
                            lc_row.separator();
                        lc_row = lc_main.row(align = True);
                        lc_row.ui_units_x = 7;
                        lc_row.prop(context.active_object.data, "clip_start", text="");
                        lc_row.prop(context.active_object.data, "clip_end", text="");
                    elif (context.active_object.data.type in {"PLANAR"}):
                        lc_main.prop(context.active_object.data, "clip_start", text="");
                        
                elif (context.active_object.type == "SPEAKER"):
                    lc_main.label(text="Speaker:", icon="OUTLINER_DATA_SPEAKER");
                    lc_main.separator_spacer();
                    lc_main.template_ID(context.active_object.data, "sound", open="sound.open_mono");
                    lc_main.prop(context.active_object.data, "volume");
                    
                elif (context.active_object.type == "LATTICE"):
                    lc_main.label(text="Lattice:", icon="OUTLINER_DATA_LATTICE");
                    lc_main.separator_spacer();
                    lc_row = lc_main.row(align = True);
                    lc_row.ui_units_x = 10;
                    lc_row.prop(context.active_object.data, "points_u");
                    lc_row.prop(context.active_object.data, "points_v");
                    lc_row.prop(context.active_object.data, "points_w");
                        
                elif (context.active_object.type == "GPENCIL"):
                    lc_main.label(text="gPencil:", icon="STROKE");
                    
                    lc_main.separator_spacer();
                    
                    lc_main.operator_menu_enum("object.origin_set", "type", text="Set Origin");
                    lc_main.operator_menu_enum("m7a.object_apply", "props", icon="NONE");
                    
                    lc_main.separator();
                    
                    lc_row = lc_main.row(align = True);
                    lc_row.ui_units_x = 6;
                    lc_row.prop(bpy.data.grease_pencils[context.active_object.data.name], "stroke_depth_order", icon='NODE_COMPOSITING', text='');
                                
                elif (context.active_object.type == "SURFACE"):
                    lc_main.label(text="Surface:", icon="SURFACE_DATA");
                    
                    lc_main.separator_spacer();
                    
                    lc_box = lc_main.box().row(align = True);
                    lc_box.label(text="  Cyclic:");
                    lc_row = lc_box.row(align = True);
                    lc_row.ui_units_x = 2.5;
                    lc_row.prop(context.active_object.data.splines[0], "use_cyclic_u", text="U", toggle=True);
                    lc_row.prop(context.active_object.data.splines[0], "use_cyclic_v", text="V", toggle=True);
                    
        
        elif (context.mode in {"EDIT_MESH"}):
            lc_main.label(text="Mesh:", icon="MESH_DATA");
            lc_main.separator_spacer();
            lc_main.operator("mesh.intersect_boolean", icon="MOD_BOOLEAN", text="");
            lc_main.operator("mesh.blend_from_shape", text="", icon="SHAPEKEY_DATA");
            lc_main.operator("mesh.subdivide", icon="MOD_SUBSURF", text="").smoothness=1;
            lc_main.operator("mesh.unsubdivide", text="", icon="MOD_DECIM").iterations = 2;
            lc_main.operator("mesh.vertices_smooth", icon="MOD_SMOOTH", text="").factor=0.5;
            
            lc_main.separator();
            lc_main.operator("view3d.edit_mesh_extrude_move_shrink_fatten", text="", icon_value=lc_icon("EXTRUDE_NORMALS"));
            lc_btn = lc_main.operator("view3d.edit_mesh_extrude_move_normal", text="", icon_value=lc_icon("EXTRUDE_INTERSECT"));
            lc_btn.dissolve_and_intersect = True;
            lc_main.operator("mesh.inset", text="", icon_value=lc_icon("INSET"));
            
            if (context.region.width > 840): 
                lc_main.separator();
                lc_btn = lc_main.operator("mesh.quads_convert_to_tris", text="", icon="MOD_TRIANGULATE");
                lc_btn.quad_method="BEAUTY"; lc_btn.ngon_method="BEAUTY";
                lc_main.operator("mesh.tris_convert_to_quads", text="", icon_value=lc_icon("TO_QUADS"));
                
            if (context.region.width > 750): 
                lc_main.separator();
                lc_main.operator_menu_enum("mesh.merge", "type", text="Merge", icon="AUTOMERGE_ON");
                if (context.region.width > 860): lc_main.operator("mesh.merge", text="", icon="CENTER_ONLY").type="CENTER";
                lc_main.operator("mesh.remove_doubles", text="", icon="CON_DISTLIMIT");
                if (context.region.width > 800): lc_main.operator("mesh.edge_split", text="", icon="MOD_EDGESPLIT").type = 'EDGE';
            
            if (context.region.width > 820): 
                lc_main.separator();
                lc_main.menu("VIEW3D_MT_hook", text="", icon="HOOK");
            
            lc_main.separator();
            lc_main.operator("mesh.knife_tool", text="", icon_value=lc_icon("KNIFE"));
            
            lc_main.separator();
            lc_main.operator("mesh.edge_face_add", text="", icon="FACE_MAPS");
            if (context.region.width > 680): lc_main.operator("mesh.fill_grid", text="", icon_value=lc_icon("FILL_GRID"));
            if (context.region.width > 650): lc_main.operator("mesh.fill", text="", icon_value=lc_icon("FILL"));
            lc_main.operator("mesh.bridge_edge_loops", text="", icon_value=lc_icon("BRIDGE"));
            
            lc_main.separator();
            lc_btn = lc_main.operator("m7a.megabag_button", text="", icon_value=lc_icon("X0"));
            lc_btn.option = "SNAP_POINT_CENTER_X";
            lc_btn_description(lc_btn, "Snap selected points to zero .x");
            
        
        elif (context.mode in {"EDIT_ARMATURE"}):
            lc_main.label(text="Armature:", icon="OUTLINER_DATA_ARMATURE");
            lc_main.separator_spacer();
            lc_main.operator("armature.bone_primitive_add", icon="BONE_DATA", text="ADD");
            lc_main.separator();
            lc_main.operator("armature.subdivide", icon="IPO_QUAD", text="");
            lc_main.operator("armature.switch_direction", icon="UV_SYNC_SELECT", text="");
            lc_main.operator("armature.extrude_move", icon="PARTICLES", text="");
            lc_main.separator();
            lc_main.operator("armature.symmetrize", icon="MOD_MIRROR", text="");
            lc_main.menu("VIEW3D_MT_edit_armature_names");
        
        elif (context.mode in {"EDIT_CURVE"}):
            lc_main.label(text="Curve:", icon="CURVE_DATA");
            lc_main.separator_spacer();
            lc_main.operator_menu_enum("curve.spline_type_set", "type", text="Type", icon="FCURVE");
            lc_main.separator();
            lc_main.operator_menu_enum("curve.handle_type_set", "type", text="Handle Type", icon="CURVE_BEZCURVE");
            lc_main.separator();
            lc_main.operator("curve.subdivide", icon="PARTICLE_POINT", text="");
            lc_main.operator("curve.switch_direction", icon="CURVE_PATH", text="");
            lc_main.operator("curve.make_segment", icon="IPO_LINEAR", text="");
            lc_main.operator("curve.smooth", icon="MOD_SMOOTH", text="");
            lc_main.separator();
            lc_main.operator("curve.select_linked", icon="GP_SELECT_POINTS", text="");
            lc_main.separator();
            lc_main.menu("VIEW3D_MT_hook");
            
        elif (context.mode in {"PAINT_GPENCIL"}):
            lc_main.label(text="gPencil:", icon="OUTLINER_DATA_GP_LAYER");
            lc_main.separator_spacer();
            
            brush = lc_tool_settings.gpencil_paint.brush;
            lc_gp_settings = brush.gpencil_settings;
            material = lc_gp_settings.material;
            tool = brush.gpencil_tool;
            
            if not lc_gp_settings.use_material_pin:
                material = context.object.active_material;
            
            icon_id = 0; txt_ma = "";
            
            if material:
                material.id_data.preview_ensure();
                if material.id_data.preview:
                    icon_id = material.id_data.preview.icon_id;
                    txt_ma = material.name;
            
            if (tool not in {"ERASE"}):
                lc_main.separator();
                
                if (tool not in {"TINT"}):
                    lc_main.prop_enum(lc_tool_settings.gpencil_paint, "color_mode", 'MATERIAL',    text="", icon='MATERIAL');
                    lc_main.prop_enum(lc_tool_settings.gpencil_paint, "color_mode", 'VERTEXCOLOR', text="", icon='VPAINT_HLT');
            
                lc_row = lc_main.row(align = True);
                if (lc_tool_settings.gpencil_paint.color_mode == 'VERTEXCOLOR') or \
                  (lc_gp_settings.brush_draw_mode == 'VERTEXCOLOR') or \
                    (tool in {"TINT"}):
                    lc_row.ui_units_x = 5
                    lc_row.prop(brush, "color", text="");
                    lc_row.prop(brush, "secondary_color", text="");
                    if (tool not in {"TINT"}):
                        lc_row_btn = lc_main.row(align = True);
                        lc_row_btn.ui_units_x = 1;
                        lc_row_btn.popover(panel="TOPBAR_PT_gpencil_materials", text=txt_ma);
                else:
                    lc_row.ui_units_x = 6;
                    lc_row.popover(panel="TOPBAR_PT_gpencil_materials", text=txt_ma, icon_value=icon_id);
                #lc_main.prop(lc_gp_settings, "pin_draw_mode", text="");
            
            if (tool in {"DRAW", "ERASE", "TINT"}):
                if (tool in {"ERASE"}):
                    lc_main.separator();
                    lc_main.prop(lc_gp_settings, "eraser_mode", expand=True);
                    
                lc_main.separator();
                
                lc_row = lc_main.row(align = True);
                lc_row.ui_units_x = 5;
                lc_row.prop(brush, "size", text="Radius")
                lc_main.prop(lc_gp_settings, "use_pressure", text="", icon='STYLUS_PRESSURE');
                
                lc_main.separator();
                
                lc_row = lc_main.row(align = True);
                lc_row.ui_units_x = 5;
                lc_row.prop(lc_gp_settings, "pen_strength", slider=True);
                lc_main.prop(lc_gp_settings, "use_strength_pressure", text="", icon='STYLUS_PRESSURE');
            elif (tool in {"FILL"}):
                lc_main.separator();
                lc_main.prop(lc_gp_settings, "fill_direction", text="", expand=True);
                lc_main.separator();
                lc_row = lc_main.row(align = True);
                lc_row.ui_units_x = 18;
                lc_row.prop(lc_gp_settings, "fill_factor", slider=True);
                lc_row.prop(lc_gp_settings, "dilate", slider=True);
                lc_row.prop(brush, "size", slider=True);
        
        if (context.mode in {'SCULPT_GPENCIL'}):
            lc_main.label(text="gPencil:", icon="OUTLINER_DATA_GP_LAYER");
            lc_main.separator_spacer();
            
            brush = lc_tool_settings.gpencil_sculpt_paint.brush;
            gp_settings = brush.gpencil_settings;
            tool = brush.gpencil_sculpt_tool;
            
            lc_main.prop(brush, "size", slider=True);
            lc_sub = lc_main.row(align=True);
            lc_sub.enabled = tool not in {'GRAB', 'CLONE'};
            lc_sub.prop(gp_settings, "use_pressure", text="");
            
            lc_main.separator();
            
            lc_main.prop(brush, "strength", slider=True);
            lc_main.prop(brush, "use_pressure_strength", text="");
            
            lc_main.separator();
            
            if tool in {'THICKNESS', 'STRENGTH', 'PINCH', 'TWIST'}:
                lc_main.separator();
                lc_main.prop(gp_settings, "direction", expand=True, text="");
            
        
        elif (context.mode in {"PAINT_VERTEX"}):
            lc_main.template_ID_preview(context.tool_settings.vertex_paint, "brush", rows=3, cols=8, hide_buttons=True);
            lc_main.separator();
            
            lc_row = lc_main.row(align = True);
            lc_row.ui_units_x = 4;
            lc_row.operator("paint.vertex_color_set", text="", icon_value=lc_icon("COLOR_FILL"));
            lc_row.prop(context.tool_settings.vertex_paint.brush, "color", text="");
            lc_main.separator();
            
            lc_row = lc_main.row(align = True);
            lc_row.ui_units_x = 4.5;
            lc_row.prop(context.tool_settings.vertex_paint.brush, "blend", text="");
            lc_main.separator();
            
            lc_row = lc_main.row(align = True);
            if (context.region.width < 800): lc_row.ui_units_x = 5;
            lc_row.prop(lc_tool_settings.unified_paint_settings, "size", slider=True);
            lc_main.prop(lc_tool_settings.vertex_paint.brush, "use_pressure_size", text="", slider=True);
            lc_main.separator();
            
            lc_row = lc_main.row(align = True);
            if (context.region.width < 800): lc_row.ui_units_x = 5;
            lc_row.prop(lc_tool_settings.vertex_paint.brush, "strength");
            lc_main.prop(lc_tool_settings.vertex_paint.brush, "use_pressure_strength", text="");
        
        elif (context.mode in {"PAINT_WEIGHT"}):
            lc_row = lc_main.row(align = True);
            lc_row.prop(lc_tool_settings.unified_paint_settings, "weight", text="Weight");
            lc_row.prop(lc_tool_settings.unified_paint_settings, "size", text="Radius");
            lc_row.prop(lc_tool_settings.vertex_paint.brush, "use_pressure_size", text="", slider=True);
            if (context.region.width < 800): lc_row.ui_units_x = 12;
            lc_main.separator();
            lc_row = lc_main.row(align = True);
            if (context.region.width < 800): lc_row.ui_units_x = 5;
            lc_row.prop(lc_tool_settings.vertex_paint.brush, "strength");
            lc_main.prop(lc_tool_settings.vertex_paint.brush, "use_pressure_strength", text="");
            
            lc_main.separator_spacer();
        
        if (context.mode in {"SCULPT"}):
            lc_main.label(text="Mesh:", icon="MESH_DATA");
            lc_main.separator_spacer();
            lc_main.template_ID_preview(context.tool_settings.sculpt, "brush", rows=3, cols=8, hide_buttons=True);
            lc_row = lc_main.row(align = True);
            
            if (context.region.width < 800): lc_row.ui_units_x = 5;
            lc_row.prop(context.tool_settings.unified_paint_settings, "size", slider=True);
            lc_main.prop(context.tool_settings.sculpt.brush, "use_pressure_size", text="");
            
            lc_main.separator();
            
            lc_row = lc_main.row(align = True);
            if (context.region.width < 800): lc_row.ui_units_x = 5;
            lc_row.prop(context.tool_settings.unified_paint_settings, "strength");
            lc_main.prop(context.tool_settings.sculpt.brush, "use_pressure_strength", text="");
            
            lc_main.separator();
            
            if (context.tool_settings.sculpt.brush.direction != "DEFAULT"):
                lc_main.prop(context.tool_settings.sculpt.brush, "direction", expand=True, text="");
                
        elif (context.mode in {"EDIT_GPENCIL"}):
            lc_main.label(text="gPencil:", icon="OUTLINER_DATA_GREASEPENCIL");
            lc_main.separator_spacer();
            
            lc_main.operator("gpencil.stroke_subdivide", icon="MOD_SUBSURF", text="").only_selected = True;
            lc_main.operator("gpencil.stroke_smooth", icon="MOD_SMOOTH", text="").only_selected = True;
            lc_main.separator();
            lc_main.menu("VIEW3D_MT_gpencil_simplify");
            lc_main.separator();
            lc_main.operator("gpencil.stroke_merge", icon="CENTER_ONLY", text="");
            lc_main.separator();
            lc_main.menu("GPENCIL_MT_move_to_layer");
            lc_main.separator();
            lc_main.operator("gpencil.duplicate_move", icon="DUPLICATE", text="");
            lc_main.operator("gpencil.copy", icon="COPYDOWN", text="");
            lc_main.operator("gpencil.paste", icon="PASTEDOWN", text="").type = "ACTIVE";
            lc_main.operator("gpencil.paste", icon="PASTEDOWN", text="").type = "LAYER";
            lc_main.separator();
            lc_main.operator("gpencil.stroke_flip", icon="CURVE_PATH", text="");
            
        else: pass
        
        lc_main.separator_spacer();
        
        def lc_mirror(icon = 0):
            if (icon == 0): lc_main.label(icon='MOD_MIRROR');
            lc_row = lc_main.row(align = True);
            lc_row.ui_units_x = 0.8;
            return lc_row;
            
        if (context.mode == 'EDIT_ARMATURE'):
            lc_mirror().prop(context.object.data, "use_mirror_x", text="X", toggle=True);
            lc_main.separator();
        elif (context.mode == 'POSE'):
            lc_mirror().prop(context.object.pose, "use_mirror_x", text="X", toggle=True);
            lc_main.separator();
        elif (context.mode in {'EDIT_MESH', 'PAINT_WEIGHT', 'SCULPT', 'PAINT_VERTEX', 'PAINT_TEXTURE'}):
            lc_mirror(0).prop(context.object, "use_mesh_mirror_x", text="X", toggle=True);
            lc_mirror(1).prop(context.object, "use_mesh_mirror_y", text="Y", toggle=True);
            lc_mirror(2).prop(context.object, "use_mesh_mirror_z", text="Z", toggle=True);
            if (context.mode == 'SCULPT'):
                lc_main.popover(panel="VIEW3D_PT_sculpt_symmetry_for_topbar", text="");
            lc_main.separator();
            
        popover_kw = {"space_type": 'VIEW_3D', "region_type": 'UI', "category": "Tool"};

        #if (context.mode == 'SCULPT'):
            #lc_main.separator();
            #lc_main.popover_group(context=".sculpt_mode", **popover_kw);
        if (context.mode == 'PAINT_VERTEX'):
            lc_main.popover(panel="VIEW3D_PT_tools_vertexpaint_symmetry_for_topbar", text="");
            lc_main.popover_group(context=".vertexpaint", **popover_kw);
        elif (context.mode == 'PAINT_WEIGHT'):
            lc_main.popover(panel="VIEW3D_PT_tools_weightpaint_symmetry_for_topbar", text="");
            lc_main.separator();
            lc_main.popover_group(context=".weightpaint", **popover_kw);
        elif (context.mode == 'PAINT_TEXTURE'):lc_main.popover_group(context=".imagepaint",    **popover_kw);
        elif (context.mode == 'EDIT_TEXT'):    lc_main.popover_group(context=".text_edit",     **popover_kw);
        elif (context.mode == 'EDIT_ARMATURE'):lc_main.popover_group(context=".armature_edit", **popover_kw);
        elif (context.mode == 'EDIT_METABALL'):lc_main.popover_group(context=".mball_edit",    **popover_kw);
        elif (context.mode == 'EDIT_LATTICE'): lc_main.popover_group(context=".lattice_edit",  **popover_kw);
        elif (context.mode == 'EDIT_CURVE'):   lc_main.popover_group(context=".curve_edit",    **popover_kw);
        elif (context.mode == 'EDIT_MESH'):
            lc_main.prop(lc_tool_settings, "use_mesh_automerge", text="");
            lc_main.separator();
            lc_main.popover_group(context=".mesh_edit", **popover_kw);
        elif (context.mode == 'POSE'):     lc_main.popover_group(context=".posemode",     **popover_kw);
        elif (context.mode == 'PARTICLE'): lc_main.popover_group(context=".particlemode", **popover_kw);
        elif (context.mode == 'OBJECT'):   lc_main.popover_group(context=".objectmode",   **popover_kw);
        
        if (context.mode in {"EDIT_GPENCIL"}):
            lc_main.operator("gpencil.snap_cursor_to_selected", text="", icon="PIVOT_CURSOR");
        else:
            lc_main.operator("view3d.snap_cursor_to_selected", text="", icon="PIVOT_CURSOR");
        lc_main.operator("view3d.snap_cursor_to_center",   text="", icon="CURSOR");
        

classes = (
    M7A_VIEW3D_HT_Tools,
);

def register():
    global bl_conf;
    
    r_unregister_class(bl_conf, "VIEW3D_HT_tool_header");
    
    for cls in classes:
        try: bpy.utils.register_class(cls);
        except: pass
    
def unregister():
    global bl_conf;
    
    for cls in classes:
        try: bpy.utils.unregister_class(cls);
        except: pass
    
    r_register_class(bl_conf, "VIEW3D_HT_tool_header");
