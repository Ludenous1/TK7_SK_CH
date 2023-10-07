# Contains a list of functions to be used for the operators (TK_OP.py)
# It references the functions from TK_SK_CH



# You can access context and data in functions as long as they're associated with a registered opereator

#TODO: add delete all objects confirmation message for scene setup


import bpy
import os
# from bpy import context
from pathlib import Path
import mathutils
import time

from.TK_SK_CH import *


def objectcheck(obj, Type):
    if obj.type == Type:
        pass
    else:
        raise TypeError("Expected an object of type: "+ Type)
    

def TekkenSceneSetup():
    #TODO: Make sure to remove even hidden objects and collections--->
    #TODO: Show message with user confirmation--->

    bpy.context.space_data.clip_start = 1
    bpy.context.space_data.clip_end = 1000

    # bpy.ops.object.select_all(action='DESELECT')
    # for obj in bpy.data.objects:
    #     obj.hide_viewport = False
    #     obj.select_set(True)
    # bpy.ops.object.delete() 

    # bpy.ops.object.select_all(action='SELECT')
    # bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.context.scene.unit_settings.scale_length = 0.01
    bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'



def TekkenFBXexporter(FBX_Exp_Enum):

    #TODO: No UV--->
    #TODO: Max material count--->
    #TODO: Check for mesh parts with no weights--->

    view_layer = bpy.context.view_layer
    All_Objects = bpy.data.objects

    #Prepare the viewport
    Active_Obj = bpy.context.active_object
    Selected_Objs = bpy.context.selected_objects
    Excluded_Cols, Hide_Viewport = FBX_Exporter.Unhide_All_Collections(view_layer)
    Hidden_Objects = FBX_Exporter.Unhide_All_Objs(All_Objects)
    print(Hidden_Objects)
    bpy.ops.object.select_all(action='DESELECT')



    


    #Check for unweighted verts

    #check if object has no uv

    #check for matching bone names
    
    #check for unused mats
    
    #Check scale of armature (requires a tekken reference and some tolerence)
    

    
    FBX_script_path = FBX_Exporter.Find_IO_SCENE_FBX_File()

    Imp_lines = FBX_Exporter.Read_Lines_From_export_fbx_bin(FBX_script_path)



    FBX_script_test = FBX_Exporter.export_fbx_bin_linecheck(Imp_lines)



    # filename, file_extension = os.path.splitext(bpy.path.basename(bpy.data.filepath))


    
    

    Exp_Settings = ['Mesh', 'Armature']

    Setting = Exp_Settings[int(FBX_Exp_Enum)]

    Mesh_Objs, Armature_Objs = FBX_Exporter.Sort_All_Objs(All_Objects)

    if Setting == 'Mesh':
        Export_Group = Mesh_Objs

    elif Setting == 'Armature':
        Export_Group = Armature_Objs


    for obj in Export_Group:

        filename, SK = FBX_Exporter.Select_and_Assign(obj, Setting)

        SK_Og_Name = FBX_Exporter.Root_bone_FBX_edit(SK,FBX_script_test)

        Result = FBX_Exporter.Test_SK_Type(SK)

        File_Path = os.path.join(bpy.path.abspath("//") ,filename +'.fbx')

        if Result == "glTF":
            bpy.ops.export_scene.fbx(filepath=File_Path, check_existing=True, filter_glob='*.fbx', use_selection=True, use_active_collection=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', bake_space_transform=False, object_types={'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}, use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='FACE', use_subsurf=False, use_mesh_edges=False, use_tspace=True, use_custom_props=False, add_leaf_bones=False, primary_bone_axis='X', secondary_bone_axis='-Y', use_armature_deform_only=True, armature_nodetype='NULL', bake_anim=False, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')
            
        elif Result == "PSK":
            bpy.ops.export_scene.fbx(filepath=File_Path, check_existing=True, filter_glob='*.fbx', use_selection=True, use_active_collection=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', bake_space_transform=False, object_types={'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}, use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='FACE', use_subsurf=False, use_mesh_edges=False, use_tspace=True, use_custom_props=False, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=True, armature_nodetype='NULL', bake_anim=False, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')

    # if FBX_script_test == False:
        FBX_Exporter.Armature_Object_Restore(SK, SK_Og_Name)

        bpy.ops.object.select_all(action='DESELECT')


    #Restore selected, active objects, and hidden objects
    for obj in Selected_Objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = Active_Obj
    FBX_Exporter.Rehide_All_Collections(view_layer, Excluded_Cols, Hide_Viewport)
    FBX_Exporter.Hide_Objects_back(All_Objects, Hidden_Objects)
    
    

def ApplyPose():
    
    SK = bpy.context.active_object # Skeleton of the object. Context can only be accessed through these set of functions
    
    OgMode = SK.mode

    AplPose(SK)

    bpy.ops.object.mode_set(mode=OgMode)


def Simplifier(ConnectBones = True, BoneSubstrgList = ["adj", "unused", "ctr", "roll" , "ROLL", "offset", "twist", "fix", "joint", "null"], Removebones = True, MergeMeshes = False, Remove_Trans = True):#SK = bpy.context.active_object ,TkState = 0, BonesEndingWith = ["adj", "unused", "ctr", "roll", "offset", "twist", "fix", "joint", "null"] ):
    
    print("Simplifying...")
    startTime = time.time() 
    # print('ARMATURE')
    
    # PreserveBones = 1

    # BoneSubstrgList = ["adj", "unused", "ctr", "roll", "offset", "twist", "fix", "joint", "null"]

    SK = bpy.context.active_object # Skeleton of the object. Context can only be accessed through these set of functions

    OgMode = SK.mode
    
    # objectcheck(SK, 'ARMATURE')

    # bpy.ops.wm.console_toggle()

    # if MergeMeshes == True:
    MeshObjectJoiner(SK)    

    # bpy.context.view_layer.objects.active = SK      # Make the skeleton the active object again
    print(time.time() - startTime, " After joining the meshes")

    if BoneSubstrgList!=[]:
        VertexGroupMerger(SK, BoneSubstrgList)
        print(time.time() - startTime, " After merging VGs")

    if Removebones == True and BoneSubstrgList!=[]:
        TekkenExtraBoneRemover(SK, BoneSubstrgList)
        print(time.time() - startTime, " After removing bones")


    # TekkenExtraBoneAnnihilater(SK, BoneSubstrgList)


    #bpy.ops.object.mode_set(mode='OBJECT')
    if ConnectBones == True:
        PrsvBones = False
        ArmatureStructureFixer(SK,PrsvBones)
        print(time.time() - startTime, " After connecting bones")

    #bpy.ops.object.mode_set(mode='OBJECT')
    

    MatSlotCombine(SK)
    print(time.time() - startTime, " After combining mats")

    if MergeMeshes == False:
        print("DONT JOIN!")
        MeshObjectSeparator(SK)
        print(time.time() - startTime, " After separating mesh")

    if Remove_Trans == True:
        ChangeBlendMode(SK, blndmode = 'HASHED')
        print(time.time() - startTime, " After changing blend mode")

    bpy.ops.object.mode_set(mode=OgMode)

def FixBones():
    
    SK = bpy.context.active_object # Skeleton of the object. Context can only be accessed through these set of functions
    L = mathutils.Vector((1, 0, 0))
    #L = Basis @ L

    B0 = mathutils.Vector((-0.0002, -0.9772, -0.2124))
    #B0 = Basis @ B0

    B1 = mathutils.Vector((-0.0000, -0.9588, -0.2841))
    #B1 = Basis @ B1

    N = mathutils.Vector((-0.0000, 0.0000, 1))
    #N = Basis @ N

    H = mathutils.Vector((0.0000, -1.0000, 0.0000))

    FacialBoneFixer(SK, L,B0,B1,N,H)



#Old and deprecated Tposer
# def TPoser():
#     print("HI!")
#     # ArmatureTposeFixer(context)
#     # TekkenArmatureTPoser(context)

#     # bpy.ops.object.mode_set(mode='OBJECT')


def BnRemover():
    SK = bpy.context.active_object
    BoneSubstrgList = ["adj", "unused", "ctr", "roll" , "ROLL", "offset", "twist", "fix", "joint", "null"]
    TekkenExtraBoneRemover(SK, BoneSubstrgList)


def BoneMergeActive():

# Dev notes active object is affected by active bone (active bone determines active object)

    # State = "Merge"

    # bpy.context.object.data.bones.active #active bone in object mode
    # bpy.context.selected_bones


    # bpy.context.active_pose_bone #active pose bones in pose mode
    # bpy.context.selected_pose_bones

    
    #TODO: test if bones belong to the same object--->Done through operator poll
    SK = bpy.context.active_object
    OgMode = SK.mode

    ActiveBone = bpy.context.object.data.edit_bones.active #active in edit mode
    
    Bonelst = bpy.context.selected_bones

    BoneNmlst = []
    for Sbone in bpy.context.selected_bones:
        if Sbone != ActiveBone:
            BoneNmlst.append(Sbone.name)



    # print(actvbonename)
    # print()

    BoneActiveMerger(BoneNmlst, ActiveBone)

    TekkenExtraBoneRemover(SK, BoneNmlst)
    
    # Adjuster(SK, ref)

    bpy.ops.object.mode_set(mode=OgMode)


def BoneMergeParent():

# Dev notes active object is affected by active bone (active bone determines active object)

    # State = "Merge"

    # bpy.context.object.data.bones.active #active bone in object mode
    # bpy.context.selected_bones


    # bpy.context.active_pose_bone #active pose bones in pose mode
    # bpy.context.selected_pose_bones

    
    #TODO: test if bones belong to the same object--->Done through operator poll
    SK = bpy.context.active_object
    OgMode = SK.mode

    ActiveBone = bpy.context.object.data.edit_bones.active #active in edit mode
    
    Bonelst = bpy.context.selected_bones

    BoneNmlst = []
    for Sbone in bpy.context.selected_bones:
        if Sbone.parent != None:
        # if Sbone != ActiveBone:


            BoneNmlst.append(Sbone.name)


    BoneParentMerger(BoneNmlst, ActiveBone)

    TekkenExtraBoneRemover(SK, BoneNmlst)
    # Adjuster(SK, ref)

    bpy.ops.object.mode_set(mode=OgMode)


def Renamer():
    SK = bpy.context.active_object
    # ref = SK_CH_mar_bdf_higeuncle

    # for obj in bpy.context.selected_objects:
    #     if obj != SK:
    #         ref = obj

    OgMode = SK.mode

    # ref = bpy.context.scene.objects["SK_CH_mar_bdf_higeuncle"]
    renamelist = bpy.context.scene.bone_rename_list

    BoneRenamer(SK, renamelist)
    
    if bpy.context.scene.bone_r_mrg:
        List = BoneRenamerMerger(SK)
        TekkenExtraBoneRemover(SK, List)

    bpy.ops.object.mode_set(mode=OgMode)
    
def TestAdjuster():
    SK = bpy.context.active_object

    # ref = SK_CH_mar_bdf_higeuncle
    # for obj in bpy.context.selected_objects:
    #     if obj != SK:
    #         ref = obj

    ref = bpy.context.scene.objects["SK_CH_mar_bdf_higeuncle"]

    # Adjuster(SK, ref)



def BonPosMove():
    SK = bpy.context.active_object

    # ref = SK_CH_mar_bdf_higeuncle
    for obj in bpy.context.selected_objects:
        if obj != SK and obj.type == 'ARMATURE':
            ref = obj

    # ref = bpy.context.scene.objects["SK_CH_mar_bdf_higeuncle"]

    BonePoseNamePositionMove(SK, ref)


    


def Test():
    SK = bpy.context.active_object
    BoneSubstrgList = ["adj", "unused", "ctr", "roll" , "ROLL", "offset", "twist", "fix", "joint", "null"]
    TekkenExtraBoneRemover(SK, BoneSubstrgList)





    
    # BoneSubstrgList = []
    # bpy.context.scene.my_list




#import fnmatch
# import numpy as np
def SK_Gen(Char_enum, Opt1_enum, Opt2_enum):

    Chars = ['aki', 'ann', 'arb', 'asa', 'ask', 'bob', 'bry', 'bs7', 'crz', 'dek', 'dnc', 'dra', 'dvj', 'edd', 'elz', 'fen', 'frv', 'gan', 'hei', 'hwo', 'ita', 'ja4', 'jac', 'jin', 'jul', 'kaz', 'kin', 'knm', 'kum', 'kzm', 'lar', 'law', 'lee', 'lei', 'leo', 'lil', 'ltn', 'mar', 'mig', 'mrx', 'mry', 'mrz', 'mut', 'nin', 'nsa', 'nsb', 'nsc', 'nsd', 'pan', 'pau', 'ste', 'xia', 'yhe', 'ykz', 'yos', 'zaf']
    Opts1 = ['glTF', 'Psk']
    Opts2 = ['All bones', 'Main bones only']
    BoneSubstrgList = ["offset", "null"]

    Char = Chars[int(Char_enum)]
    Opt1 = Opts1[int(Opt1_enum)]
    Opt2 = Opts2[int(Opt2_enum)]

    SK = SK_Char_Gen(Char, Opt1, Opt2)

    if Opt2 == 'Main bones only':
        TekkenExtraBoneRemover(SK, BoneSubstrgList)

    if Opt1 == 'glTF':
        glTFArmatureExpander(SK, BoneSubstrgList)


#TODO: Adjust how glTF bones look in the viewport --->DONE

        #Remove other bones
        # pass

    # if Opt1 == 'glTF':
        # ArmatureStructureFixer(SK, 1)
        # SK_Type_conversion(SK, Opt1)

def RenamerListPopulateFx():


    SK = bpy.context.active_object

    OgMode = SK.mode

    tolerance = SK_Tolerance(SK)
    print(tolerance)

    Matches=ArmatureBoneIdentifier(SK, tolerance)

    UpdatedMatches=ArmatureHandIdentifier(SK, tolerance, Matches)

    print(UpdatedMatches)

    bpy.ops.object.mode_set(mode=OgMode)

    return UpdatedMatches
        

def T_Poser(FixArmature, Connect_Bones, FixFingerTips, Tpose_Spine):
    print("Tposing...")
    startTime = time.time() 

    X_axis = mathutils.Vector((1,0,0))
    Z_axis = mathutils.Vector((0,0,1))

    Left_Arm_Bones_No_Thumb = ['L_Shoulder', 'L_Arm', 'L_ForeArm', 'L_Hand', 
    'L_Index1', 'L_Index2', 'L_Index3', 'L_Index4_null', 
    'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Middle4_null', 
    'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Ring4_null', 
    'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'L_Pinky4_null']

    Left_Thumb = ['L_Thumb1', 'L_Thumb2', 'L_Thumb3']#,'L_Thumb4_null']

    Right_Arm_Bones_No_Thumb = ['R_Shoulder', 'R_Arm', 'R_ForeArm', 'R_Hand', 
    'R_Index1', 'R_Index2', 'R_Index3', 'R_Index4_null', 
    'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Middle4_null', 
    'R_Ring1', 'R_Ring2', 'R_Ring3', 'R_Ring4_null', 
    'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'R_Pinky4_null']

    Right_Thumb = [ 'R_Thumb1', 'R_Thumb2', 'R_Thumb3']#, 'R_Thumb4_null']

    Left_Leg_Bones = ['L_UpLeg', 'L_Leg']#, 'L_Foot', 'L_Toe', 'L_Toe1_null', ]

    Right_Leg_Bones = ['R_UpLeg', 'R_Leg']#, 'R_Foot']#, 'R_Toe', 'R_Toe1_null']

    All_bones = ['L_Shoulder', 'L_Arm', 'L_ForeArm', 'L_Hand', 
    'L_Index1', 'L_Index2', 'L_Index3', 'L_Index4_null', 
    'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Middle4_null', 
    'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Ring4_null', 
    'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'L_Pinky4_null',
    'L_Thumb1', 'L_Thumb2', 'L_Thumb3','L_Thumb4_null',
    'R_Shoulder', 'R_Arm', 'R_ForeArm', 'R_Hand', 
    'R_Index1', 'R_Index2', 'R_Index3', 'R_Index4_null', 
    'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Middle4_null', 
    'R_Ring1', 'R_Ring2', 'R_Ring3', 'R_Ring4_null', 
    'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'R_Pinky4_null',
    'R_Thumb1', 'R_Thumb2', 'R_Thumb3', 'R_Thumb4_null',
    'L_UpLeg', 'L_Leg', 'L_Foot', 'L_Toe', 'L_Toe1_null', 
    'R_UpLeg', 'R_Leg', 'R_Foot', 'R_Toe', 'R_Toe1_null']


    # LimbJoints = ['L_Shoulder', 'L_Arm', 'L_ForeArm', 
    # 'R_Shoulder', 'R_Arm', 'R_ForeArm', 

    # 'L_Leg', 
    # 'R_Leg']

    LimbJoints = ['L_Shoulder', 'L_ForeArm', 
    'R_Shoulder', 'R_ForeArm', 

    'L_Leg', 
    'R_Leg']

    if Tpose_Spine == False: #Limbs only by default
    # Neck_Spines = ["Neck", "Spine1", "Spine2"]
        Neck_Spines = ["Neck"]
    elif Tpose_Spine == True:
        Neck_Spines = ["Neck", "Spine1", "Spine2"]

#    if FixFingerTips == True: 
    FingerTips = ['R_Thumb3','R_Pinky3','R_Ring3','R_Middle3', 'R_Index3', 'L_Thumb3', 'L_Pinky3', 'L_Ring3', 'L_Middle3', 'L_Index3']
    # else:
    #     FingerTips =[]
    

    # AllMainBones = (Left_Arm_Bones_No_Thumb+Left_Thumb+Right_Arm_Bones_No_Thumb+Right_Thumb, Left_Leg_Bones+Right_Leg_Bones)
    Leg_Bones = Left_Leg_Bones + Right_Leg_Bones 
    # #TekkenFBXexporter(context)

    SK = bpy.context.active_object

    OgMode = SK.mode

    bpy.ops.object.mode_set(mode='OBJECT')


    print(time.time() - startTime, " After defining all list")
    #_____I don't trust people to do the write thing so I'll apply stuff for them
    # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # AplPose(SK) 
    if FixArmature == True:
        ArmatureBoneHeadFix(SK, LimbJoints)
        #Move bone heads to a more accurate position

    if Connect_Bones == True:
        ArmatureBoneTailFix(SK,  All_bones)

    if FixFingerTips == True:
        ArmatureFingerTipTailFix(SK, FingerTips)

    Armature_T_Poser(SK, X_axis, Z_axis, Neck_Spines, Left_Arm_Bones_No_Thumb, Right_Arm_Bones_No_Thumb, Leg_Bones, Left_Thumb, Right_Thumb)

    print(time.time() - startTime, " After Armature_T_Poser")

    bpy.ops.object.mode_set(mode=OgMode)



# def AutoDetectBones():

#     SK = bpy.context.active_object

#     Max = MaxBoundingBox(SK)

#     Matches=ArmatureBoneIdentifier(SK, Max)

#     return Matches


def Pose_Snapper(autoscale, mode_enum):
    
    Triade = ["Neck",'L_Shoulder','R_Shoulder']

    Left_Hand_Bones = ['L_Hand', 
    'L_Index1', 'L_Index2', 'L_Index3', 'L_Index4_null', 
    'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Middle4_null', 
    'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Ring4_null', 
    'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'L_Pinky4_null',
    'L_Thumb1', 'L_Thumb2', 'L_Thumb3','L_Thumb4_null']

    Right_Hand_Bones = ['R_Hand',
    'R_Index1', 'R_Index2', 'R_Index3', 'R_Index4_null', 
    'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Middle4_null', 
    'R_Ring1', 'R_Ring2', 'R_Ring3', 'R_Ring4_null', 
    'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'R_Pinky4_null',
    'R_Thumb1', 'R_Thumb2', 'R_Thumb3', 'R_Thumb4_null'
    ]


    Fingers_No_Bases = [ 
    'L_Index2', 'L_Index3', 'L_Index4_null', 
    'L_Middle2', 'L_Middle3', 'L_Middle4_null', 
    'L_Ring2', 'L_Ring3', 'L_Ring4_null', 
    'L_Pinky2', 'L_Pinky3', 'L_Pinky4_null',
    'L_Thumb2', 'L_Thumb3','L_Thumb4_null',

    'R_Index2', 'R_Index3', 'R_Index4_null', 
    'R_Middle2', 'R_Middle3', 'R_Middle4_null', 
    'R_Ring2', 'R_Ring3', 'R_Ring4_null', 
    'R_Pinky2', 'R_Pinky3', 'R_Pinky4_null',
    'R_Thumb2', 'R_Thumb3', 'R_Thumb4_null'
    ]

    Fingers_Bases = [ 
    'L_Thumb1',
    'L_Index1',
    'L_Middle1', 
    'L_Ring1', 
    'L_Pinky1',

    'R_Thumb1',
    'R_Index1',
    'R_Middle1', 
    'R_Ring1', 
    'R_Pinky1', 
    ]

    Left_Leg_Bones = ['L_UpLeg', 'L_Leg']#, 'L_Foot', 'L_Toe', 'L_Toe1_null', ]

    Right_Leg_Bones = ['R_UpLeg', 'R_Leg']#, 'R_Foot']#, 'R_Toe', 'R_Toe1_null']

    SmartSnapBones = ["Head",'L_Arm', 'L_ForeArm', 'L_Hand', 
    'L_Index1', 'L_Index2', 'L_Index3', 'L_Index4_null', 
    'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Middle4_null', 
    'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Ring4_null', 
    'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'L_Pinky4_null',
    'L_Thumb1', 'L_Thumb2', 'L_Thumb3','L_Thumb4_null',
    'R_Arm', 'R_ForeArm', 'R_Hand', 
    'R_Index1', 'R_Index2', 'R_Index3', 'R_Index4_null', 
    'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Middle4_null', 
    'R_Ring1', 'R_Ring2', 'R_Ring3', 'R_Ring4_null', 
    'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'R_Pinky4_null',
    'R_Thumb1', 'R_Thumb2', 'R_Thumb3', 'R_Thumb4_null',
    'L_UpLeg', 'L_Leg', 'L_Foot',
    'R_UpLeg', 'R_Leg','R_Foot']

    SmartSnapBonesBrief = ["Head",
    'L_Arm', 'L_ForeArm', 'L_Hand',
    'R_Arm', 'R_ForeArm', 'R_Hand',
    'L_UpLeg', 'L_Leg', 'L_Foot',
    'R_UpLeg', 'R_Leg','R_Foot']


    SnapBones = ["Neck",'L_Shoulder','R_Shoulder', 'R_UpLeg', 'L_UpLeg']


    # FingerTips =[]
    FingerTips = ['R_Thumb3','R_Pinky3','R_Ring3','R_Middle3', 'R_Index3', 'L_Thumb3', 'L_Pinky3', 'L_Ring3', 'L_Middle3', 'L_Index3']

    # AllMainBones = (Left_Arm_Bones_No_Thumb+Left_Thumb+Right_Arm_Bones_No_Thumb+Right_Thumb, Left_Leg_Bones+Right_Leg_Bones)
    Leg_Bones = Left_Leg_Bones + Right_Leg_Bones 
    # #TekkenFBXexporter(context)


    SK = bpy.context.active_object

    OgMode = SK.mode

    AplPose(SK) #I don't trust people to do the write thing

    # ref = SK_CH_mar_bdf_higeuncle
    for obj in bpy.context.selected_objects:
        if obj != SK and obj.type == 'ARMATURE':
            refSK = obj

    if autoscale == True:
        ArmatureScaleAdjust(SK, refSK)

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # boneScaleInheritanceDisabler(SK)
    bonedisconnet(SK)

    if mode_enum == '0':
        Simple_Pose_Snapper(SK, refSK)
    elif mode_enum == '1':
        ArmaturePosePoints(SK, refSK,Triade, SnapBones, SmartSnapBonesBrief,  Fingers_Bases, Fingers_No_Bases)


    bpy.ops.object.mode_set(mode=OgMode)


def ArmatureMatchFixer():
    SK = bpy.context.active_object

    OgMode = SK.mode

    for obj in bpy.context.selected_objects:
        if obj != SK and obj.type == 'ARMATURE':
            refSK = obj
        
    Armature_OverHall(SK,refSK)

    bpy.ops.object.mode_set(mode=OgMode)

def VertexGroupMerger_ST(VG_List, Target, Remove_Groups):
    Object = bpy.context.active_object

    OgMode = Object.mode
    
    Vertex_Groups_Merger(Object, VG_List, Target)

    if Remove_Groups == True:
        Remove_Vertex_Groups(Object,VG_List)

        if Target in VG_List:

            Object.vertex_groups.active.name = Target

    bpy.ops.object.mode_set(mode=OgMode)

