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
    lc_main_row = lc_main.row(align = True);
    lc_main_row.prop(context.active_object.data, "type", text="");
    
    if (context.active_object.data.type == 'PERSP'):
        lc_main_row.prop(context.active_object.data, "lens_unit", text="");
        
        lc_main.separator();
        
        if (context.active_object.data.lens_unit == 'MILLIMETERS'):
            lc_main.prop(context.active_object.data, "lens");
        else:
            lc_main.prop(context.active_object.data, "angle");
        
    lc_main.separator();
    
    lc_main_row = lc_main.box().row(align = True);
    lc_btn = lc_main_row.row(); lc_btn.label(text="Shift:"); lc_btn.scale_x = 0.15;
    lc_main_row.prop(context.active_object.data, "shift_x", text="X");
    lc_main_row.prop(context.active_object.data, "shift_y", text="Y");
    
    lc_main.separator();
    
    lc_main.prop(context.active_object.data.dof, "use_dof", toggle=True);
    if (context.active_object.data.dof.use_dof == True):
        lc_main.prop(context.active_object.data.dof, "focus_distance");
        lc_main_row = lc_main.row(align = True);
        lc_main_row.prop(context.active_object.data.dof, "aperture_fstop");
        lc_main_row.prop(context.active_object.data, "show_limits", toggle=True);

    lc_main.separator();
    
    lc_main.prop(context.active_object.data, "show_safe_areas", toggle=True);
    if (context.active_object.data.show_safe_areas == True):
        lc_main_row = lc_main.row(align = False);
        lc_main_col = lc_main_row.column(align = True);
        lc_main_col.prop(context.scene.safe_areas, "title", text="");
        lc_main_col = lc_main_row.column(align = True);
        lc_main_col.prop(context.scene.safe_areas, "action", text="");
