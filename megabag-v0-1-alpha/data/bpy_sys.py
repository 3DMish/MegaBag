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

import bpy, os, sys, pickle;


data_path = os.path.dirname(os.path.abspath(__file__));

def ver_less(v1, v2, v3): return True if ((v1, v2, v3) >  bpy.app.version) else False;
def ver_more(v1, v2, v3): return True if ((v1, v2, v3) <= bpy.app.version) else False;

if (ver_more(2,78,0)): import bpy.utils.previews;
lc_prew = bpy.utils.previews.new();

def m7a_load_icon(image):
    if (image in lc_prew): thumb = lc_prew[image];
    else: thumb = lc_prew.load(image, image, 'IMAGE');
    return thumb.icon_id;

def lc_icon(code):
    path = data_path + "/m7a_icons/";
    images = {
        "KNIFE":             m7a_load_icon(path + "m7a_knife" + ".png"),
        "LOOP_CUT":          m7a_load_icon(path + "m7a_loop_cut" + ".png"),
        "INSET":             m7a_load_icon(path + "m7a_inset" + ".png"),
        "EXTRUDE":           m7a_load_icon(path + "m7a_extrude" + ".png"),
        "EXTRUDE_NORMALS":   m7a_load_icon(path + "m7a_extrude_normals" + ".png"),
        "EDGE_SLIDE":        m7a_load_icon(path + "m7a_edge_slide" + ".png"),
        "VERTEX_SLIDE":      m7a_load_icon(path + "m7a_vertex_slide" + ".png"),
        "X0":                m7a_load_icon(path + "m7a_x0" + ".png"),
        "FILL":              m7a_load_icon(path + "m7a_fill" + ".png"),
        "FILL_GRID":         m7a_load_icon(path + "m7a_fill_grid" + ".png"),
        "VIEW_3D":           m7a_load_icon(path + "m7a_view3d" + ".png"),
        "TO_QUADS":          m7a_load_icon(path + "m7a_to_quads" + ".png"),
        "BIRD":              m7a_load_icon(path + "m7a_bird" + ".png"),
        "EXTRUDE_INTERSECT": m7a_load_icon(path + "m7a_extrude_intersect" + ".png"),
        "FROSTING":          m7a_load_icon(path + "m7a_frosting" + ".png"),
        "FLOWER":            m7a_load_icon(path + "m7a_flower" + ".png"),
        "SPRINKLES":         m7a_load_icon(path + "m7a_sprinkles" + ".png"),
        "CHERRY":            m7a_load_icon(path + "m7a_cherry" + ".png"),
        "LIGHTNING":         m7a_load_icon(path + "m7a_lightning" + ".png"),
        "BEADS_WIREFRAME":   m7a_load_icon(path + "m7a_beads_wireframe" + ".png"),
        "ELECTRIC":          m7a_load_icon(path + "m7a_electric" + ".png"),
        "CIRCLE_ARRAY":      m7a_load_icon(path + "m7a_circle_array" + ".png"),
        "BRIDGE":            m7a_load_icon(path + "m7a_bridge" + ".png"),
        "DUPLICATE":         m7a_load_icon(path + "m7a_duplicate" + ".png"),
        "DUPLICATE_LINKED":  m7a_load_icon(path + "m7a_duplicate_linked" + ".png"),
        "MALE":              m7a_load_icon(path + "m7a_male" + ".png"),
        "FEMALE":            m7a_load_icon(path + "m7a_female" + ".png"),
        "DEL_KEYS":          m7a_load_icon(path + "m7a_delete_keys" + ".png"),
        "DUP_MOVE":          m7a_load_icon(path + "m7a_duplicate_move" + ".png"),
        "COLOR_FILL":        m7a_load_icon(path + "m7a_to_fill" + ".png"),
        }
    if code in images: return images[code];
    else: return 0;
    
def lc_split_row(lc_cont, width):
    if (bpy.context.region.width > width):
        lc_cont = lc_cont.row(align=True);
    else: lc_cont = lc_cont.column(align=True);
    return lc_cont;
            
def lc_cont_x(lc_cont, width):
    lc_cont_btn = lc_cont.row(align=True);
    lc_width(lc_cont_btn, width);
    return lc_cont_btn;

def bpy_preferences(path = "", name = ""):
    if (path == "addons"):
        if (ver_more(2, 80, 0)):
            if (name in bpy.context.preferences.addons.keys()):
                return bpy.context.preferences.addons[name].preferences;
            else: return None;
        else:
            if (name in bpy.context.user_preferences.addons.keys()):
                return bpy.context.user_preferences.addons[name].preferences;
            else: return None;
        
    else:
        if (ver_more(2, 80, 0)): return bpy.context.preferences;
        else: return bpy.context.user_preferences;

def bpy_temp(): return bpy_preferences().filepaths.temporary_directory;

def gp_buffer_path(): return bpy_temp() + "m7a_gp_data";

def gp_set_buffer(data):
    gp_file = open(gp_buffer_path(), "wb");
    pickle.dump(gp_file, data);
    gp_file.close();
    
def gp_get_buffer():
    gp_file = open(gp_buffer_path(), "rb");
    result = pickle.load(gp_file);
    gp_file.close();
    return result;
    
def gp_is_buffer(): return True if (os.path.exists(gp_buffer_path())) else False;

def lc_btn_description(lc_btn, description):
    if (ver_more(2,80,0)): lc_btn.desc = description;

def lc_width(lc_element, width, width_x = 0):
    if (ver_more(2, 80, 0)): lc_element.ui_units_x = width;
    else: lc_element.scale_x = width/10 if (width_x == 0) else width_x;
        
def r_remove_attr(cont, name):
    if (hasattr(cont, name)): delattr(cont, name);

def r_register_class(cont, name):
    if not (hasattr(bpy.types, name)):
        if (cont[name] != None):
            bpy.utils.register_class(cont[name]);
            
def r_unregister_class(cont, name):
    if (hasattr(bpy.types, name)):
        if not (cont == None): cont[name] = getattr(bpy.types, name);
        bpy.utils.unregister_class(getattr(bpy.types, name));    
