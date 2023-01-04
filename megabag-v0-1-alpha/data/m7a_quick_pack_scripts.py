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

def transform_shrink_fatten(value):
    if ver_more(2,80,0):
        bpy.ops.transform.shrink_fatten(
            value=value, use_even_offset=False, mirror=True, use_proportional_edit=False, 
            proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
            use_proportional_projected=False
        );
    else:
        bpy.ops.transform.shrink_fatten(
            value=-value, use_even_offset=False, mirror=True, 
            proportional_edit_falloff='SMOOTH', proportional_size=1,
        );
def mesh_bevel(offset, segments = 1):
    if ver_more(2,80,0): bpy.ops.mesh.bevel(offset=offset, offset_pct=0, segments=segments);
    else: bpy.ops.mesh.bevel(offset=offset, segments=segments);

def m7a_script_add_seam(value = 0.1):
    bpy.ops.object.mode_set(mode='EDIT', toggle=False);
    bpy.ops.mesh.select_mode(type="EDGE");
    mesh_bevel(offset=0.0152637, segments=2);
    bpy.ops.mesh.select_less();
    mesh_bevel(offset=0.00647339, segments=2);
    bpy.ops.mesh.select_less();
    
    transform_shrink_fatten(-(value/14));

def m7a_script_add_jeans_seam():
    a_data = bpy.context.active_object.data;
    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False);
    bpy.ops.mesh.select_mode(type="EDGE");
    
    mesh_bevel(offset=0.141835, segments=2);
        
    bpy.ops.mesh.inset(thickness=0.0160773, depth=0, use_outset=True);
    
    bpy.ops.mesh.select_less();
    
    bpy.ops.transform.edge_slide(value=1.0, mirror=True, correct_uv=True, release_confirm=True);
    
    if ver_more(2,80,0):
        bpy.ops.transform.shrink_fatten(
            value=0.0181372, use_even_offset=False, mirror=True, use_proportional_edit=False, 
            proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
            use_proportional_projected=False
        )
    else:
        bpy.ops.transform.shrink_fatten(
            value=-0.0181372, use_even_offset=False, mirror=True, 
            proportional_edit_falloff='SMOOTH', proportional_size=1,
        );
    
    bpy.ops.mesh.bevel(offset=0.00485736, offset_pct=0, segments=1);
        
    bpy.ops.mesh.region_to_loop();
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
    
    edge_main = None;
    for edge in a_data.edges:
        if (edge.select == True):
            edge_main = edge;
            break;
    
    if (edge_main != None):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False);
        bpy.ops.mesh.select_all(action='DESELECT');
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
        edge_main.select = True;
        bpy.ops.object.mode_set(mode='EDIT', toggle=False);
        
        bpy.ops.mesh.loop_multi_select(ring=False);
        
        bpy.ops.mesh.bevel(offset=0.000120806, offset_pct=0);
        
        bpy.ops.mesh.region_to_loop();
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
        
        edge_main = None;
        for edge in a_data.edges:
            if (edge.select == True):
                edge_main = edge;
                break;
                
        edge_second = None;
        for i in range(0, len(a_data.edges)):
            if (a_data.edges[len(a_data.edges)-i-1].select == True):
                edge_second = a_data.edges[len(a_data.edges)-i-1];
                break;
                
        if (edge_main != None) and (edge_second != None):
        
            bpy.ops.object.mode_set(mode='EDIT', toggle=False);
            bpy.ops.mesh.select_all(action='DESELECT');
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
            edge_main.select = True;
            bpy.ops.object.mode_set(mode='EDIT', toggle=False);
            
            bpy.ops.mesh.loop_multi_select(ring=False);
            bpy.ops.transform.edge_slide(value=-0.97137, mirror=True, correct_uv=True, release_confirm=True);
            bpy.ops.transform.shrink_fatten(
                value=0.00657137, use_even_offset=False, mirror=True, use_proportional_edit=False, 
                proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
                use_proportional_projected=False
            );
            
            bpy.ops.mesh.select_all(action='DESELECT');
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
            edge_main.select = True; edge_second.select = True;
            bpy.ops.object.mode_set(mode='EDIT', toggle=False);
            
            bpy.ops.mesh.loop_multi_select(ring=False);
            
            bpy.ops.mesh.loop_to_region();
            bpy.ops.mesh.inset(thickness=0.00913552, depth=0);
            
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
            
            edge_main = [];
            for edge in a_data.edges:
                if (edge.select == True):
                    edge_main.append(edge);
                    
            if (edge_main != []):
            
                bpy.ops.object.mode_set(mode='EDIT', toggle=False);
                
                bpy.ops.mesh.region_to_loop();
                
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False);
                
                for edge in edge_main:
                    if (edge.select == True):
                        edge.select = False;
                    else:
                        edge.select = True;
                
                bpy.ops.object.mode_set(mode='EDIT', toggle=False);
                
                bpy.ops.mesh.select_nth(skip=1, nth=1);
                
                bpy.ops.transform.shrink_fatten(
                    value=0.022322, use_even_offset=False, mirror=True, 
                    use_proportional_edit=False, proportional_edit_falloff='SMOOTH', 
                    proportional_size=1, use_proportional_connected=False, use_proportional_projected=False
                );
