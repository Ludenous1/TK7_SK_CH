# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>


# TODO: Change class and property names ---> Done?

#Dev Note: Always make custom properties lowercase
#Dev Note: Panel are displayed in the order they're registered


bl_info = {
    "name" : "TK7_SK_CH",
    "author" : "Ludenous",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 4),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy

from bpy.props import StringProperty, IntProperty, CollectionProperty, EnumProperty, BoolProperty

from .TK_PT import * 
from.TK_OP import *
from.TK_UI import *
from.TK_PROP import *
from.TK_PROP_FX import *

classes = (
    # ____Panels_______
    Character_Modding,

    # VIEWPORT_PT_PANEL,
    # PORTER_PT_PANEL,
    # CUSTOM_PT_PANEL,
    # SK_TOOLS_PT_PANEL,
    SK_GEN_PT_PANEL,
    SK_POSE_SNAP_PT_PANEL,
    SK_TPOSER_PT_PANEL,

    RENAMER_PT_PANEL,
    

    # SKTOOLS_PT_PANEL,

    SIMPLIFIER_PT_PANEL,

    # MESHTOOLS_PT_PANEL, 

    # ____operators_______
    SK_CH_BlenderScene,
    SK_CH_Export,
    # SK_CH_Test,
    SK_CH_Simplify,
    SK_CH_ApplyPose,

    SK_CH_BoneFix,
    # SK_CH_BoneMergeActive,
    # SK_CH_BoneMergeParent,
    SK_CH_BoneMerge,
    
    SK_CH_BoneRemove,
    SK_CH_PosMove,


    SK_CH_SK_Generator,

    SK_CH_Pose_Snapper,

    SK_CH_Tposer,
    

    Bone_Renamer_Preset_Load_Operator,
    Bone_Renamer_Preset_Add_Operator,
    Bone_Renamer_Preset_Remove_Operator,
    SK_CH_BoneRenamerListPopulate,
    LIST_OT_BoneRename_NewItem,
    LIST_OT_BoneRename_DeleteItem,

    SK_CH_BoneRenamer,
    # LIST_OT_MoveItem,



    LIST_OT_Substrng_NewItem,
    LIST_OT_Substrng_DeleteItem,

    # ____Windows_______
    # WM_OT_simplifier,
    # MATERIAL_UL_matslots_example
    # ____UILists_______
    MY_UL_BoneRenameList, 

    MY_UL_BoneSubstringList,

    # ____PropertyGroups_______
    BoneParent,


    BoneRenameListItem,
    Rename_Preset,


    BoneSubstrngListItem


    # MyProperties, ADDONNAME_PT_main_panel, ADDONNAME_OT_my_op
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
#__________________Main tools_________________________
    bpy.types.Scene.bone_mrg_enum = EnumProperty(items=Generate_Enum_for_BoneMerger)

    bpy.types.Scene.sk_to_isolate = PointerProperty(
        name='',
        description='the skeleton that you want to isolate the bones of',
        type=bpy.types.Object,
        poll=SK_hierarchy_disabler_poll
        # update=SK_hierarchy_disabler_update
        )

    bpy.types.Scene.bone_isolation_switch = BoolProperty(default = False, update=SK_hierarchy_disabler_Switch_update)

    bpy.types.Scene.bone_parent_list = CollectionProperty(type = BoneParent)

#__________________SK Generator_________________________
    bpy.types.Scene.sk_gen_char_enum = EnumProperty(items=Generate_Enum_for_Chars)
    bpy.types.Scene.sk_gen_opt1_enum = EnumProperty(items=Generate_Enum_for_SK_Gen_Opt1)
    bpy.types.Scene.sk_gen_opt2_enum = EnumProperty(items=Generate_Enum_for_SK_Gen_Opt2)


#__________________Pose snapper_________________________

    bpy.types.Scene.ps_autoscale = BoolProperty(default = True)
    bpy.types.Scene.ps_mode_enum = EnumProperty(items=Generate_Enum_for_ps_mode)


#__________________T Poser_________________________

    
    bpy.types.Scene.tp_fix_armature = BoolProperty(default = False)
    bpy.types.Scene.tp_connect_bones = BoolProperty(default = True)
    bpy.types.Scene.tp_fix_fingertips = BoolProperty(default = False)
    bpy.types.Scene.tp_tpose_spine = BoolProperty(default = False)




#______________Bone renamer list_________________________
    #Main bone name list (formerly my list and list index)
    bpy.types.Scene.bone_rename_list = CollectionProperty(type = BoneRenameListItem)
    bpy.types.Scene.bone_rename_list_index = IntProperty(name = "Index for bone_rename_list",
                                             default = 0)
    #Preset list for Bone renamer (formerly test_number and test_collection)                                  
    bpy.types.Scene.preset_enum = EnumProperty(items=Generate_Enum_from_Rename_Preset_Collection,update=BoneRenamerPresetSelection)
    bpy.types.Scene.preset_collection = CollectionProperty(type=Rename_Preset)
    
    bpy.types.Scene.bone_r_mrg = BoolProperty(default = False)


#____________________Simplifier_________________________
    #Main bone name list (formerly my list and list index)
    bpy.types.Scene.bone_substrng_list = CollectionProperty(type = BoneSubstrngListItem)
    bpy.types.Scene.bone_substrng_list_index = IntProperty(name = "Index for bone_substrng_list",
                                             default = 0)
    
    bpy.types.Scene.bone_simp_connect = BoolProperty(default = True)
    # bpy.types.Scene.bone_prsv = BoolProperty(default = False)
    bpy.types.Scene.bone_remv = BoolProperty(default = True)
    bpy.types.Scene.mesh_join = BoolProperty(default = False)
    bpy.types.Scene.clr_trnspc = BoolProperty(default = True)


    if not check_ob_in_scene in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(check_ob_in_scene)


def unregister():

    if check_ob_in_scene in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(check_ob_in_scene)

#________________Main tools______________________________
   
    del bpy.types.Scene.bone_mrg_enum 

    del bpy.types.Scene.sk_to_isolate

    del bpy.types.Scene.bone_isolation_switch 

    del bpy.types.Scene.bone_parent_list 

#_________________SK Generator___________________________
    del bpy.types.Scene.sk_gen_char_enum 
    del bpy.types.Scene.sk_gen_opt1_enum
    del bpy.types.Scene.sk_gen_opt2_enum

#__________________T Poser_________________________

    del bpy.types.Scene.tp_connect_bones
    del bpy.types.Scene.tp_fix_armature 
    del bpy.types.Scene.tp_fix_fingertips 
    del bpy.types.Scene.tp_tpose_spine 



#______________Bone renamer list_________________________
    del bpy.types.Scene.bone_rename_list
    del bpy.types.Scene.bone_rename_list_index

    del bpy.types.Scene.preset_enum 
    del bpy.types.Scene.preset_collection

    del bpy.types.Scene.bone_r_mrg 


#____________________Simplifier_________________________
    #Main bone name list (formerly my list and list index)
    del bpy.types.Scene.bone_substrng_list
    del bpy.types.Scene.bone_substrng_list_index 

    del bpy.types.Scene.bone_simp_connect
    # del bpy.types.Scene.bone_prsv
    del bpy.types.Scene.bone_remv 
    del bpy.types.Scene.mesh_join 
    del bpy.types.Scene.clr_trnspc
                            
    

    for cls in classes:
        bpy.utils.unregister_class(cls)

# if __name__ == "__main__":
#    print("___________Do something here_________")
# GenerateBoneRenamerEnumerator()