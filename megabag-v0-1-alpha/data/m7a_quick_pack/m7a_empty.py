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

def draw_properties(self, context, lc_main):
    lc_main.prop(context.active_object, "empty_display_type", text="");
    lc_main.prop(context.active_object, "empty_display_size");
    if (context.active_object.empty_display_type == 'IMAGE'):
        lc_main.separator();
        lc_main.template_ID(context.active_object, "data", open="image.open", unlink="object.unlink_data");
        if (context.active_object.data):
            lc_main.separator();
            lc_main.prop(context.active_object.data, "source", text="");
    
    if not (context.active_object.field == None):
        lc_main.separator();
        lc_main_row = lc_main.row(align = True);
        lc_main_row.prop(context.active_object.field, "type", text="");
        
        if (context.active_object.field.type not in {'NONE', 'GUIDE', 'TEXTURE'}):
            lc_btn = lc_main_row.row(align = True);
            lc_btn.prop(context.active_object.field, "shape", text="");
            lc_btn.scale_x = 0.5;
        
        if (context.active_object.field.type not in {'NONE'}):
            
            if (context.active_object.field.type in {'TEXTURE'}):
                lc_main.separator();
            
                lc_main.row().template_ID(context.active_object.field, "texture", new="texture.new");
            
            if (context.active_object.field.type not in {'GUIDE', 'DRAG'}):
                lc_main.separator();
            
                lc_main.prop(context.active_object.field, "strength");
            
            if (context.active_object.field.type in {'TURBULENCE'}):
                lc_main.separator();
            
                lc_main.prop(context.active_object.field, "size");
                
            if (context.active_object.field.type not in {'GUIDE', 'DRAG', 'HARMONIC', 'TEXTURE'}):
                lc_main.prop(context.active_object.field, "inflow");
                
            if (context.active_object.field.type not in {'GUIDE'}):
                lc_main.separator();
                
                lc_main_row = lc_main.row(align = True);
                lc_main_row.prop(context.active_object.field, "apply_to_location", toggle=True);
                if (context.active_object.field.type not in {'TEXTURE'}):
                    lc_main_row.prop(context.active_object.field, "apply_to_location", toggle=True);
                
            if (context.active_object.field.type not in {'GUIDE', 'FLUID_FLOW', 'TEXTURE'}):
                lc_main.separator();
                
                lc_main.prop(context.active_object.field, "noise");
                lc_main.prop(context.active_object.field, "seed");
                
                lc_main.separator();
                
                lc_main.prop(context.active_object.field, "use_absorption", toggle=True);
                
                lc_main.separator();
                
                lc_main.prop(context.active_object.field, "wind_factor");
            
            if (context.active_object.field.type in {'GUIDE'}):
                lc_main.separator();
            
                lc_main.prop(context.active_object.field, "guide_free");
                lc_main.prop(context.active_object.field, "falloff_power");
                
                lc_main.separator();

                lc_main_row = lc_main.row(align = True);
                lc_main_row.prop(context.active_object.field, "use_guide_path_add", toggle=True);
                lc_main_row.prop(context.active_object.field, "use_guide_path_weight", toggle=True);
                
                lc_main.separator();
            
                lc_main.prop(context.active_object.field, "guide_clump_amount");
                lc_main.prop(context.active_object.field, "guide_clump_shape");
                
                lc_main.separator();
            
                lc_main.prop(context.active_object.field, "guide_minimum");
                lc_main_row = lc_main.row(align = True);
                lc_main_row.prop(context.active_object.field, "use_max_distance", text="");
                lc_btn = lc_main_row.row(align = True);
                lc_btn.prop(context.active_object.field, "distance_max");
                lc_btn.active = context.active_object.field.use_max_distance;
