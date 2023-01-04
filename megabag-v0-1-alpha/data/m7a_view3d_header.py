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
    "VIEW3D_HT_header": None,
    "VIEW3D_HT_MENU_types_add": {
        "OBJECT":        "VIEW3D_MT_add"               if (ver_more(3,0,0)) else "INFO_MT_add",
        "EDIT_MESH":     "VIEW3D_MT_mesh_add"          if (ver_more(3,0,0)) else "INFO_MT_mesh_add",
        "EDIT_CURVE":    "VIEW3D_MT_curve_add"         if (ver_more(3,0,0)) else "INFO_MT_add",
        "EDIT_SURFACE":  "VIEW3D_MT_surface_add"       if (ver_more(3,0,0)) else "INFO_MT_surface_add",
        "EDIT_METABALL": "VIEW3D_MT_metaball_add"      if (ver_more(3,0,0)) else "INFO_MT_metaball_add",
        "EDIT_ARMATURE": "TOPBAR_MT_edit_armature_add" if (ver_more(3,0,0)) else "INFO_MT_edit_armature_add",
    },
}

class VIEW3D_HT_header(Header):
    bl_space_type = 'VIEW_3D';
    bl_region_type = 'HEADER';
    
    def draw(self, context):
        lc_obj = context.active_object;
        lc_space_data = context.space_data;
        lc_tool_settings = context.tool_settings;
        lc_mode = context.object.mode if (lc_obj) else "NONE";
        lc_obj_mode = 'OBJECT' if lc_obj is None else lc_obj.mode;
        lc_item_mode = bpy.types.Object.bl_rna.properties["mode"].enum_items[lc_obj_mode];
        lc_item_cont = bpy.types.Object.bl_rna.properties["mode"].translation_context;
        
        lc_main = self.layout.row(align = True);
        lc_main.template_header();
        
        lc_main.separator();
        
        if (ver_more(2,90,0)):
            lc_row = lc_main.row(align = True);
            lc_row.ui_units_x = 5.5;
            lc_row.operator_menu_enum(
                "object.mode_set", "mode",
                text=bpy.app.translations.pgettext_iface(lc_item_mode.name, lc_item_cont),
                icon=lc_item_mode.icon,
            );
            lc_row.active = True if (lc_obj) else False;
            
            lc_main.separator();
            lc_main.template_header_3D_mode();
            
            if context.mode in ['PAINT_GPENCIL']:
                lc_main.prop(lc_tool_settings, "use_gpencil_draw_onback", text="", icon="MOD_OPACITY");
                lc_main.prop(lc_tool_settings, "use_gpencil_automerge_strokes", text="");
                lc_main.prop(lc_tool_settings, "use_gpencil_weight_data_add", text="", icon="WPAINT_HLT");
                lc_main.prop(lc_tool_settings, "use_gpencil_draw_additive", text="", icon="FREEZE");
                lc_main.separator();
                
            if (hasattr(bpy_preferences("addons", "megabag").m7a_megabag_props, "view3d_compact_menu")):
                if (bpy_preferences("addons", "megabag").m7a_megabag_props.view3d_compact_menu):
                    if (context.mode in {"EDIT_MESH", "PAINT_WEIGHT", "PAINT_VERTEX", "PAINT_TEXTURE"}):
                        lc_main.separator();
                    lc_main.menu("M7A_VIEW3D_MT_Menu");
                else:
                    if (context.mode in {"EDIT_MESH", "PAINT_WEIGHT", "PAINT_VERTEX", "PAINT_TEXTURE"}):
                        lc_main.separator();
                    m7a_view_menu(lc_main, lc_obj_mode, context.mode, lc_obj);
            else:
                lc_main.separator();
                m7a_view_menu(lc_main, lc_obj_mode, context.mode, lc_obj);
        else:
            
            if (hasattr(bpy.types.Scene, "m7a_megabag_properties")):
                if (context.scene.m7a_megabag_properties.view3d_compact_menu == True):
                    lc_main.separator();
                    lc_main.menu("M7A_VIEW3D_MT_Menu");
                else:
                    lc_main.separator();
                    m7a_view_menu(lc_main, lc_obj_mode, context.mode, lc_obj);
            else:
                lc_main.separator();
                m7a_view_menu(lc_main, lc_obj_mode, context.mode, lc_obj);
            
            #lc_main.separator();
            lc_row = lc_main.row(align = False);
            lc_row.template_header_3D();
            
            #lc_row = lc_main.row(align = True);
            #lc_row.operator("mesh.select_mode", text="", icon="VERTEXSEL").type = "VERT";
            #lc_row.operator("mesh.select_mode", text="", icon="EDGESEL").type = "EDGE";
            #lc_row.operator("mesh.select_mode", text="", icon="FACESEL").type = "FACE";
        
        
        if (ver_more(3,0,0)):
            lc_main.separator_spacer();
            
            if (lc_obj_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL'}) or (lc_mode in {"POSE"}):
                lc_row = lc_main.row(align = True);
                lc_row.ui_units_x = 4
                lc_row.prop_with_popover(
                    context.scene.transform_orientation_slots[0],
                    "type", text="",
                    panel="VIEW3D_PT_transform_orientations",
                );
                lc_main.separator();
                
            if (lc_obj_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL', 'SCULPT_GPENCIL'}) or (lc_mode in {"POSE"}):
                lc_main.prop(lc_tool_settings, "transform_pivot_point", text="", icon_only=True);
            
            lc_main.separator();
            
            if context.mode in ['PAINT_GPENCIL', 'SCULPT_GPENCIL']:
                if context.mode in ['PAINT_GPENCIL']:
                    lc_main.prop_with_popover(lc_tool_settings, "gpencil_stroke_placement_view3d", text="", panel="VIEW3D_PT_gpencil_origin");
                    lc_main.separator();
                    
                lc_main.prop_with_popover(lc_tool_settings.gpencil_sculpt, "lock_axis", text="", panel="VIEW3D_PT_gpencil_lock");
                lc_main.separator();
                
                if context.mode in ['PAINT_GPENCIL']:
                    if context.workspace.tools.from_space_view3d_mode(context.mode).idname == "builtin_brush.Draw":
                        settings = lc_tool_settings.gpencil_sculpt.guide;
                        lc_row = lc_main.row(align=True)
                        lc_row.prop(settings, "use_guide", text="", icon='GRID');
                        lc_sub = lc_row.row(align=True)
                        lc_sub.active = settings.use_guide;
                        lc_sub.popover(
                            panel="VIEW3D_PT_gpencil_guide",
                            text="Guides",
                        );
                
            if context.mode not in ['PAINT_GPENCIL', 'SCULPT']:
                lc_main.prop(lc_tool_settings, "use_snap", text="");
                snap_items = bpy.types.ToolSettings.bl_rna.properties["snap_elements"].enum_items;
                snap_elements = lc_tool_settings.snap_elements;
                if len(snap_elements) == 1:
                    for i in snap_elements:
                        lc_main.popover(panel="VIEW3D_PT_snapping", text="", icon=snap_items[i].icon);
                else:
                    lc_main.popover(panel="VIEW3D_PT_snapping", icon="NONE");
                del snap_items, snap_elements;
                lc_main.separator();
            
                if (lc_mode == "OBJECT"):
                    lc_attr = "use_proportional_edit_objects";
                    lc_main.prop(lc_tool_settings, lc_attr, icon_only=True);
                else:
                    lc_attr = "use_proportional_edit";
                    if (lc_tool_settings.use_proportional_edit):
                        if (lc_tool_settings.use_proportional_connected): icon = 'PROP_CON';
                        elif (lc_tool_settings.use_proportional_projected): icon = 'PROP_PROJECTED';
                        else: icon = 'PROP_ON';
                    else: icon = 'PROP_OFF';
                    lc_main.prop(lc_tool_settings, lc_attr, icon_only=True, icon=icon);
            
                lc_row = lc_main.row(align = True);
                if (ver_more(3,0,0)): lc_row.active = getattr(lc_tool_settings, lc_attr)
                lc_row.prop_with_popover(
                    lc_tool_settings, "proportional_edit_falloff",
                    text="", icon_only=True,
                    panel="VIEW3D_PT_proportional_edit",
                );
                del lc_attr;
        
        else:
            # proportional edit
            
            if context.gpencil_data and context.gpencil_data.use_stroke_edit_mode or \
                lc_obj_mode in {'EDIT', 'PARTICLE_EDIT'}:
                lc_main.separator();
                lc_row = lc_main.row(align=True)
                lc_row.prop(lc_tool_settings, "proportional_edit", icon_only=True);
                lc_ror = lc_row.row(align=True);
                lc_ror.prop(lc_tool_settings, "proportional_edit_falloff", icon_only=True);
                lc_ror.active = lc_tool_settings.proportional_edit != 'DISABLED';
                
            elif lc_obj_mode == 'OBJECT':
                lc_main.separator();
                lc_row = lc_main.row(align=True);
                lc_row.prop(lc_tool_settings, "use_proportional_edit_objects", icon_only=True);
                lc_ror = lc_row.row(align=True);
                lc_ror.prop(lc_tool_settings, "proportional_edit_falloff", icon_only=True);
                lc_ror.active = lc_tool_settings.use_proportional_edit_objects;
                
            # snap element
            
            lc_main.separator();
            lc_snap_element = lc_tool_settings.snap_element;
            
            lc_row = lc_main.row(align = True);
            lc_row.prop(lc_tool_settings, "use_snap", text="");
            lc_row.prop(lc_tool_settings, "snap_element", icon_only=True);
            if (lc_snap_element == 'INCREMENT'):
                lc_row.prop(lc_tool_settings, "use_snap_grid_absolute", text="");
            else:
                lc_row.prop(lc_tool_settings, "snap_target", text="");
                if obj:
                    if (lc_mode == 'EDIT'):
                        lc_row.prop(lc_tool_settings, "use_snap_self", text="");
                    if (lc_mode in {'OBJECT', 'POSE', 'EDIT'}) and (snap_element != 'VOLUME'):
                        lc_row.prop(lc_tool_settings, "use_snap_align_rotation", text="");

            if (lc_snap_element == 'VOLUME'):
                lc_row.prop(lc_tool_settings, "use_snap_peel_object", text="");
            elif (lc_snap_element == 'FACE'):
                lc_row.prop(lc_tool_settings, "use_snap_project", text="");
            
            del lc_snap_element;
            
        
        if (lc_space_data.region_3d.view_perspective == 'CAMERA'):
            lc_main.separator();
            lc_main.prop(
                lc_space_data, "lock_camera", text="",
                icon="CON_CAMERASOLVER" if (ver_more(3,0,0)) else "OUTLINER_OB_CAMERA",
            );
            
        if (ver_more(3,0,0)):
            lc_main.separator_spacer();
        
            lc_main.popover(panel="VIEW3D_PT_object_type_visibility",
                            icon_value=lc_space_data.icon_from_show_object_viewport, 
                            text="");
            lc_main.separator();
            
            lc_main.prop(lc_space_data, "show_gizmo", text="", toggle=True, icon='GIZMO');
            lc_row = lc_main.row(align = True);
            lc_row.active = lc_space_data.show_gizmo;
            lc_row.popover(panel="VIEW3D_PT_gizmo_display", text="");
            lc_main.separator();
            
            lc_main.prop(lc_space_data.overlay, "show_overlays", icon='OVERLAY', text="");
            lc_row = lc_main.row(align = True);
            lc_row.active = lc_space_data.overlay.show_overlays;
            lc_row.popover(panel="VIEW3D_PT_overlay", text="");
            lc_main.separator();
            
            if (lc_mode in {"POSE"}):
                depressed = lc_space_data.overlay.show_xray_bone;
            elif (lc_space_data.shading.type == 'WIREFRAME'):
                depressed = lc_space_data.shading.show_xray_wireframe
            else: depressed = lc_space_data.shading.show_xray;
            
            lc_main.operator("view3d.toggle_xray", text="", icon='XRAY', depress=depressed);
            lc_main.separator();
            
            lc_row = lc_main.row(align = True);
            lc_row.prop(lc_space_data.shading, "type", text="", expand=True);
            lc_row.popover(panel="VIEW3D_PT_shading", text="");
            
            #lc_main.separator();
            #lc_main.popover(panel="M7A_VIEW3D_HEADER_Panel", text="", icon="TOOL_SETTINGS");
        
        del lc_obj,  lc_mode, lc_obj_mode, lc_item_mode, lc_item_cont;
        del lc_tool_settings, lc_space_data;

class M7A_VIEW3D_MT_Menu(Menu):
    bl_idname      = 'M7A_VIEW3D_MT_Menu';
    bl_label       = 'Menu';
    bl_description = '3D View Panel Menu';
    
    @staticmethod
    def draw(self, context):
        lc_main = self.layout.column(align = True);
        lc_mode = bpy.context.object.mode if (context.active_object) else "NONE";
        
        m7a_view_menu(lc_main, lc_mode, context.mode, context.active_object, True);

def m7a_view_menu(lc_main, lc_mode, lc_mode_string, a_obj, compact=False):
    global bl_conf;
    lc_tool_settings = bpy.context.scene.tool_settings
    
    lc_main.menu("VIEW3D_MT_view");
    
    if (compact) and (lc_mode_string != 'PAINT_TEXTURE'): lc_main.separator();
    
    if (ver_more(3,0,0)): is_gpencil = a_obj and a_obj.mode.find('_GPENCIL') > 0;
    else: is_gpencil = bpy.context.gpencil_data and bpy.context.gpencil_data.use_stroke_edit_mode;
    
    if (is_gpencil):
        if (ver_more(3,0,0)):
            if lc_mode_string not in {'PAINT_GPENCIL', 'WEIGHT_GPENCIL'}:
                lc_main.menu("VIEW3D_MT_select_gpencil");
                if (a_obj and a_obj.mode == 'VERTEX_GPENCIL'):
                    lc_main.menu("VIEW3D_MT_paint_gpencil");
                elif (a_obj and a_obj.mode == 'EDIT_GPENCIL'):
                    lc_main.menu("VIEW3D_MT_edit_gpencil");
                    lc_main.menu("VIEW3D_MT_edit_gpencil_stroke");
                    lc_main.menu("VIEW3D_MT_edit_gpencil_point");
            elif (a_obj and a_obj.mode == 'PAINT_GPENCIL'):
                lc_main.menu("VIEW3D_MT_draw_gpencil");
            elif (a_obj and a_obj.mode == 'WEIGHT_GPENCIL'):
                lc_main.menu("VIEW3D_MT_weight_gpencil");
        else:
            lc_main.menu("VIEW3D_MT_select_gpencil");
    
    elif (lc_mode_string != 'SCULPT'):
        lc_main.menu("VIEW3D_MT_select_%s" % lc_mode_string.lower());
        
        for menu in bl_conf["VIEW3D_HT_MENU_types_add"].keys():
            if (lc_mode_string in {menu}):
                lc_main.menu(bl_conf["VIEW3D_HT_MENU_types_add"][menu], text="Add");
                
        if (lc_mode_string == 'EDIT_MESH'):
            lc_main.menu("VIEW3D_MT_edit_mesh");
            lc_main.menu("VIEW3D_MT_edit_mesh_vertices");
            lc_main.menu("VIEW3D_MT_edit_mesh_edges");
            lc_main.menu("VIEW3D_MT_edit_mesh_faces");
            lc_main.menu("VIEW3D_MT_uv_map", text="UV");
        elif (lc_mode_string in {'EDIT_CURVE', 'EDIT_SURFACE'}):
            lc_main.menu("VIEW3D_MT_edit_curve_ctrlpoints");
            lc_main.menu("VIEW3D_MT_edit_curve_segments");
        elif (lc_mode_string != 'PAINT_TEXTURE'):
            lc_main.menu("VIEW3D_MT_%s" % lc_mode_string.lower());
        elif (lc_mode_string in {'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE'}):
            if a_obj.data.use_paint_mask:
                lc_main.menu("VIEW3D_MT_select_paint_mask");
            elif a_obj.data.use_paint_mask_vertex and lc_mode_string in {'PAINT_WEIGHT', 'PAINT_VERTEX'}:
                lc_main.menu("VIEW3D_MT_select_paint_mask_vertex");
    else:
        if (ver_more(3,0,0)):
            lc_main.menu("VIEW3D_MT_sculpt");
            lc_main.menu("VIEW3D_MT_mask");
            lc_main.menu("VIEW3D_MT_face_sets");
        else:
            if (lc_mode_string in {'SCULPT', 'PAINT_VERTEX', 'PAINT_WEIGHT', 'PAINT_TEXTURE'}):
                lc_main.menu("VIEW3D_MT_brush");
            if (lc_mode_string == 'SCULPT'):
                lc_main.menu("VIEW3D_MT_hide_mask");
                
        if (lc_mode_string == 'OBJECT'):
            lc_main.menu("VIEW3D_MT_object");

classes = (
    VIEW3D_HT_header, M7A_VIEW3D_MT_Menu,
);

def register():
    global bl_conf;
    
    if (ver_more(3,0,0)):
        r_unregister_class(bl_conf, "VIEW3D_HT_header");
        for cls in classes:
            try: bpy.utils.register_class(cls);
            except: pass
    
def unregister():
    global bl_conf;
    
    if (ver_more(3,0,0)):
        for cls in classes:
            try: bpy.utils.unregister_class(cls);
            except: pass
        r_register_class(bl_conf, "VIEW3D_HT_header");
