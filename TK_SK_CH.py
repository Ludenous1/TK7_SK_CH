# Contains all the Skeleton related tools needed to simplify, rename, edit, and pose skeletons along with their associated meshes 
# In essence, this file has all the core functionality that this addon relies on
# This file is only referenced by the functions in TK_FX

import bpy
from bpy import context
import fnmatch
import mathutils
import math
from math import isclose
import numpy as np
import os
import addon_utils
  

# To expand compatability beyond Tekken 7
Bonedict = {
        'Hip': 'Hip',
        'Spine1': 'Spine1', 
        'Spine2': 'Spine2', 
        'Neck': 'Neck', 
        'Head': 'Head', 
        'L_Shoulder': 'L_Shoulder', 
        'L_Arm': 'L_Arm', 
        'L_ForeArm': 'L_ForeArm', 
        'L_Hand': 'L_Hand', 
        'L_Thumb1': 'L_Thumb1', 
        'L_Thumb2': 'L_Thumb2', 
        'L_Thumb3': 'L_Thumb3', 
        'L_Thumb4_null': 'L_Thumb4_null', 
        'L_Index1': 'L_Index1', 
        'L_Index2': 'L_Index2', 
        'L_Index3': 'L_Index3', 
        'L_Index4_null': 'L_Index4_null', 
        'L_Middle1': 'L_Middle1', 
        'L_Middle2': 'L_Middle2', 
        'L_Middle3': 'L_Middle3', 
        'L_Middle4_null': 'L_Middle4_null', 
        'L_Ring1': 'L_Ring1', 
        'L_Ring2': 'L_Ring2', 
        'L_Ring3': 'L_Ring3', 
        'L_Ring4_null': 'L_Ring4_null', 
        'L_Pinky1': 'L_Pinky1', 
        'L_Pinky2': 'L_Pinky2', 
        'L_Pinky3': 'L_Pinky3', 
        'L_Pinky4_null': 'L_Pinky4_null', 
        'R_Shoulder': 'R_Shoulder', 
        'R_Arm': 'R_Arm', 
        'R_ForeArm': 'R_ForeArm', 
        'R_Hand': 'R_Hand', 
        'R_Thumb1': 'R_Thumb1', 
        'R_Thumb2': 'R_Thumb2', 
        'R_Thumb3': 'R_Thumb3', 
        'R_Thumb4_null': 'R_Thumb4_null', 
        'R_Index1': 'R_Index1', 
        'R_Index2': 'R_Index2', 
        'R_Index3': 'R_Index3', 
        'R_Index4_null': 'R_Index4_null', 
        'R_Middle1': 'R_Middle1', 
        'R_Middle2': 'R_Middle2', 
        'R_Middle3': 'R_Middle3', 
        'R_Middle4_null': 'R_Middle4_null', 
        'R_Ring1': 'R_Ring1', 
        'R_Ring2': 'R_Ring2', 
        'R_Ring3': 'R_Ring3', 
        'R_Ring4_null': 'R_Ring4_null', 
        'R_Pinky1': 'R_Pinky1', 
        'R_Pinky2': 'R_Pinky2', 
        'R_Pinky3': 'R_Pinky3', 
        'R_Pinky4_null': 'R_Pinky4_null', 
        'L_UpLeg': 'L_UpLeg', 
        'L_Leg': 'L_Leg', 
        'L_Foot': 'L_Foot', 
        'L_Toe': 'L_Toe', 
        'L_Toe1_null': 'L_Toe1_null', 
        'R_UpLeg': 'R_UpLeg', 
        'R_Leg': 'R_Leg', 
        'R_Foot': 'R_Foot', 
        'R_Toe': 'R_Toe', 
        'R_Toe1_null': 'R_Toe1_null'
    }

#___________________For the FBX exporter__________________


def Find_IO_SCENE_FBX_File():
    for mod in addon_utils.modules():
        mod_info = addon_utils.module_bl_info(mod)
        if(mod_info['name'] == 'FBX format'):
            mod_path = os.path.dirname(mod.__file__)

            return os.path.join(mod_path, "export_fbx_bin.py")

    raise FileNotFoundError("Could not find the addon io_scene_fbx")


def Read_Lines_From_export_fbx_bin(filepath):
    
    ImportantLines = []
    Indices = []
    
    with open(filepath,"r") as f:
        Counter = 0
        lines = f.readlines()
        for Lindx,line in enumerate(lines):
            if "elif ob_obj.type == 'EMPTY' or ob_obj.type == 'ARMATURE':" in line:
                ImportantLines.append(lines[Lindx].strip())
                ImportantLines.append(lines[Lindx+1].strip())
                ImportantLines.append(lines[Lindx+2].strip())
                
                break
                
#                print(lines[Lindx][15], lines[Lindx+1], lines[Lindx+2])
#            ConvLine = LineInfoConverterForRenamerPresets(line)
#            if len(ConvLine) == 2:
#                context.scene.bone_rename_list.add()
#                bpy.context.scene.bone_rename_list[Counter].Current_Name = ConvLine[0]
#                bpy.context.scene.bone_rename_list[Counter].New_Name = ConvLine[1]
#                Counter +=1 

#C:\Program Files\Blender Foundation\Blender 3.2\3.2\scripts\addons\io_scene_fbx

#elif ob_obj.type == 'EMPTY' or ob_obj.type == 'ARMATURE':

    return ImportantLines

def export_fbx_bin_linecheck(lines):
    count = 0
    for line in lines:
        if line.startswith('#'):
            count += 1
            
    if count == 0 and len(lines) == 3:
        #Not touched
        return False
    
    elif count == 3 and len(lines) == 3:
        return True
    
    elif count == 0 and len(lines) == 0:
        #Incase user deletes the lines completely
        return True

    else:
        raise Exception("Something is missing / wrong with the built-in FBX exporter")   


def Root_bone_FBX_edit(SK,FBX_script_test):
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    SKDict = {bone.name: bone for bone in  SK.data.edit_bones}
    
    if FBX_script_test == True:
        if "MODEL_00" in SKDict:
            pass
        else:
            SK.data.edit_bones.new("MODEL_00")
            
        for bone in SK.data.edit_bones:
            if bone.parent == None and bone.name != "MODEL_00":
                bone.parent = SKDict["MODEL_00"]
                    
#        pass
    elif FBX_script_test == False:
        if "MODEL_00" in SKDict:
            SK.data.edit_bones.remove(SKDict["MODEL_00"])

        SK.name = "MODEL_00"

    bpy.ops.object.mode_set(mode='OBJECT')
    
    
def Test_SK_Type(SK):
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    SKDict = {bone.name: bone for bone in  SK.data.edit_bones}
        
    if ("Spine1" not in SKDict) or ("Spine2" not in SKDict):
        raise Exception("The skeleton is missing the Spine1 and / or Spine2 bone(s)")
    else:
        RefVec =   SKDict["Spine1"].head - SKDict["Spine2"].head
        
        if isclose(RefVec.dot(SKDict["Spine1"].vector),0,abs_tol=0.0001):
            print("PSK")
            Result = "PSK"
            
        else:
            print("glTF")
            Result = "glTF"
            
             
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return Result

#    isclose(QuatVec.length, 0,abs_tol = 0.0001)




#_________________________________________________________




# OG SK_CH starts here
#___________________Shared Functions________________







#___________________________________________________________________



#__________________________SK_Gen____________________
#Converts PSK to glTF without using a reference skeleton 

#Concept:
#B: bone axis matrix  (3x3)
#R: Rotation Matrix (3x3)
#l: local vector (3x1)
#g: global vector (3x1)

#g = B @ l
#l = B^(-1) @ g 
#r = R @ B^(-1) @ g  where r is the rotated vector about local axis in terms of the local axis
#r' = B @ R @ B^(-1) @ g where r' is the rotated vector about local axis in terms of the global axis
#F = B @ R @ B^(-1) @ B = B @ R 

#Z rotation matrix (3x3) about the z axis (pointing towards the eye) and where o is the angle clockwise from the x-axis to y-axis :
#[[cos(o), -sin(o), 0],[sin(o), cos(o), 0],[0,0,1]]




def BoneMatrixConverter(BoneMatrix,Type):
   #Function that takes in the bone matrix and converts it into the type mentioned in "Type"
   MainMatrix = mathutils.Matrix(BoneMatrix)
   B = MainMatrix.to_3x3()

   if Type == 'glTF':
      o = -1.57 # -Psk to glTF;+glTF to Psk
#    elif Type == "GLTFtoPSK":
#       o = 1.57 # -Psk to glTF;+glTF to Psk
   else:
      o = 0
    #   print("No change")

   R =  mathutils.Matrix([[math.cos(o), -math.sin(o), 0],[math.sin(o), math.cos(o), 0],[0,0,1]])
   F = B @ R
   NewMat = F.to_4x4()
   v0 = NewMat[0] + mathutils.Vector([0,0,0,BoneMatrix[0][3]])
   v1 = NewMat[1] + mathutils.Vector([0,0,0,BoneMatrix[1][3]])
   v2 = NewMat[2] + mathutils.Vector([0,0,0,BoneMatrix[2][3]])

   NewMat[0] = v0
   NewMat[1] = v1
   NewMat[2] = v2

   return NewMat

def SK_Type_conversion(SK, Type):
   bpy.ops.object.mode_set(mode='EDIT')

   for bone in reversed(SK.data.edit_bones):


      NewMatrix = BoneMatrixConverter(bone.matrix, Type)

      bone.matrix = NewMatrix

      bpy.ops.object.editmode_toggle()
      bpy.ops.object.editmode_toggle()

   bpy.ops.object.mode_set(mode='OBJECT')  





#Script that generates and stores all the bone information for all Tekken chars. 
#It is meant to be used on "All_Face_SKs.blend" which contains the PSK skeletons for all chars.
#It generates a text file for each character. 
#Each line within a text file contains the information pertaining a single bone.
#The bone information are organized as follows: "Bone_Name"/Matrix(...)/"Parent_Name"
#If a bone has no parent, the bone parent name would be blank. i.e. ""


#This script is used for the face Sks of all chars selected in object mode

#Dev note: Bone roll is misleading as it doesn't always reflect the bone axis

def GetAddonsFolderName_SK_CH_Gen():
    addon_folder = None
    
    for mod in addon_utils.modules():
        if mod.bl_info.get('name') == "TK7_SK_CH":
            addon_folder = os.path.dirname(mod.__file__)
            break
    
    if addon_folder is None:
        raise Exception("Could not retrieve the TK7_SK_CH addon path.")
    
    if len(addon_folder.split(os.sep)) > 1:
        addon_folder = os.path.basename(os.path.normpath(addon_folder))
    
    print(addon_folder)
    return addon_folder

def GetAddonsFolderPath_SK_CH_Gen():
    addon_folder_path = None
    
    for mod in addon_utils.modules():
        if mod.bl_info.get('name') == "TK7_SK_CH":
            addon_folder_path = os.path.dirname(mod.__file__)
            break
    
    if addon_folder_path is None:
        raise Exception("Could not retrieve the TK7_SK_CH addon path.")
    
    return addon_folder_path

def ReadSKdatafile(char):
    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path="addons")
    AddonFolderPath = GetAddonsFolderPath_SK_CH_Gen()

    #Function that reads the SK data files and returns a list with the lines
    File = + 'SK_CH_'+ char + '.txt'
    # GlobalPath = directory+'/'+AddonFolder+'/'+Path

    GlobalPath = os.path.join(AddonFolderPath, 'Skeletons', File)
    print(GlobalPath)
    with open(GlobalPath) as f:
        lines = f.readlines()
        
    return lines

def LineInfoConverter(line):
#Function that cleans up the bone string data into a more blender friendly format 
    Elements = line.split('///')
    BoneName = Elements[0]

    MatrixElements = Elements[1].split(',')[:]
    BoneMatrix =  mathutils.Matrix(((float(MatrixElements[0]),float(MatrixElements[1]),float(MatrixElements[2]),float(MatrixElements[3])),(float(MatrixElements[4]),float(MatrixElements[5]),float(MatrixElements[6]),float(MatrixElements[7])),(float(MatrixElements[8]),float(MatrixElements[9]),float(MatrixElements[10]),float(MatrixElements[11])),(float(MatrixElements[12]),float(MatrixElements[13]),float(MatrixElements[14]),float(MatrixElements[15]))))


    ParenName = Elements[2].split('\n')[0]
    # Elements[2]=ParenName

    ConvertedLine = [BoneName, BoneMatrix, ParenName]
    return ConvertedLine


# def ExtractLineInformation(lines):
#     for line in lines:
#         line.split('/')


def SK_Char_Gen(Char, Opt1, Opt2):
    # Chars = ['aki', 'ann', 'arb', 'asa', 'ask', 'bob', 'bry', 'bs7', 'crz', 'dek', 'dnc', 'dra', 'dvj', 'edd', 'elz', 'fen', 'frv', 'gan', 'hei', 'hwo', 'ita', 'ja4', 'jac', 'jac', 'jin', 'jul', 'kaz', 'kin', 'knm', 'kum', 'kzm', 'lar', 'law', 'lee', 'lei', 'leo', 'lil', 'ltn', 'mar', 'mig', 'mrx', 'mut', 'nin', 'nsa', 'nsb', 'nsc', 'nsd', 'pan', 'pau', 'ste', 'xia', 'yhe', 'ykz', 'yos', 'zaf']
    # Opts1 = ['glTF', 'Psk']
    # Opts2 = ['All bones', 'Main bones only']

    bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)) # Create a new skeleton

    SK = bpy.context.active_object
    
    # print(SK.name)
    length = 0.05

    # Char = Chars[int(Char_enum)]
    SK.name = Char

    lines =  ReadSKdatafile(Char)

    bpy.ops.object.mode_set(mode='EDIT')


    for line in lines:
        
        ProperLine = LineInfoConverter(line)
        print(ProperLine[0] , ProperLine[2])
        
        SK.data.edit_bones.new(ProperLine[0])
        # if bone 
        SK.data.edit_bones[ProperLine[0]].length = length
        FinalMat = BoneMatrixConverter(mathutils.Matrix(ProperLine[1]),Opt1)
        SK.data.edit_bones[ProperLine[0]].matrix = FinalMat
        # SK.data.edit_bones[ProperLine[0]].matrix = mathutils.Matrix(ProperLine[1])
        if ProperLine[2] != "":
            Parent = SK.data.edit_bones[ProperLine[2]]
            SK.data.edit_bones[ProperLine[0]].parent = Parent
            # print(SK.data.edit_bones[ProperLine[2]].name, SK.data.edit_bones[ProperLine[2]].parent)

    Bone = SK.data.edit_bones["Bone"]
    SK.data.edit_bones.remove(Bone)

    bpy.ops.object.mode_set(mode='OBJECT')
    SK.scale = mathutils.Vector((100.0, 100.0, 100.0))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


    return SK



#_________________________________________



#___________________Bone Renamer____________________

def BoneRenamer(SK, list):
# tries to find nearby mathcing bones between two skeletons and then rename them
 
# TODO: Test this code again cause I think mathcing works here--->Done (It doesn't)
# TODO: Fix matching--->Done via pose.bones instead of data.bones
# TODO: Skip renaming for facial bones--->Done 
# TODO: Skip renaming for booba bones--->

    bpy.ops.object.mode_set(mode='OBJECT')
    # obj = SK #context.object #self.Skeleton
    for bone in SK.data.bones:
        name = bone.name
        for item in list:
            if name == item.Current_Name:
                bone.name = item.New_Name

    bpy.ops.object.mode_set(mode='OBJECT')


def BoneRenamerMerger(SK):

    MergedboneNames = []

    bpy.ops.object.mode_set(mode='OBJECT')
    for bone in SK.data.bones:
        BoneName = bone.name

        if "." in BoneName:
            Elements = BoneName.split('.')
            # print(Elements[0], Elements[1])

            try:
                Parent = SK.data.bones[Elements[0]] # Check if the bone exists to begin with
                
                for mesh in SK.children:

                    bpy.context.view_layer.objects.active = mesh

                    MeshVGMerger(Parent.name, bone.name, mesh)
                    MergedboneNames.append(bone.name)

                bpy.context.view_layer.objects.active = SK  
            except:
                pass

    return MergedboneNames
    

def TekkenExtraBoneAnnihilater(SK, BoneSubstrgList):
# A function meant to test if setting the bone property to 0 would anhilate it. It did.

    
    obj = SK #context.object #self.Skeleton

    bpy.ops.object.mode_set(mode='EDIT')
    
    for bone in obj.data.edit_bones:
        
        BoneName = bone
        for name in BoneSubstrgList:
            try:
#                print(bone)
                if bone.name.find(name)!=-1:#"*offset") or fnmatch.fnmatchcase(bone.name, "*null") or fnmatch.fnmatchcase(bone.name, "*group") or fnmatch.fnmatchcase(bone.name, "*BASE"):
#                if fnmatch.fnmatchcase(bone.name, name):#"*offset") or fnmatch.fnmatchcase(bone.name, "*null") or fnmatch.fnmatchcase(bone.name, "*group") or fnmatch.fnmatchcase(bone.name, "*BASE"):
                     print(BoneName.name,name)
                     bone.tail = bone.head
                     break
            except:
                pass  
    print("Bones Annihilated")    
            
    bpy.ops.object.mode_set(mode='OBJECT')   


#Bone Detector____________
#Script to match bone names with Tekken 7 ones.
#Armature Assumptions:
#1- Armature is in the correct orientation (i.e face looking at the -ve global y-axis direction)
#2- The hands and the feet are the most extreme parts in the skeleton along the x-axis and z-axis, respectively.
#3- The armature has some max set z-scale and x-scale?? (cause of the minz and tolerance respectively)
#4- The armature data (bone head location) is quasi-semetric in edit mode
#5- The arms and the legs have 2 long spanning bones (i.e distance between their heads is relatively large)



#TODO: Detect Head and Neck Bones----> DONE
#TODO: Detect the first spine bone---> Done
#TODO: Find finger bones----> DONE
#TODO: Fix for overextending auxiliary bones (like wings, tentackles , etc)--->

# import bpy
# import numpy as np



def MaxBoundingBox(SK):
    Max = max(bpy.data.objects[SK.name].dimensions.x, bpy.data.objects[SK.name].dimensions.y, bpy.data.objects[SK.name].dimensions.z)
    return Max

def SK_Tolerance(SK):
    # obj = SK
    bpy.ops.object.mode_set(mode='EDIT')
    Max = max(bpy.data.objects[SK.name].dimensions.x, bpy.data.objects[SK.name].dimensions.y, bpy.data.objects[SK.name].dimensions.z)

    MaxX_distance = 0
    MinX_distance = 0
    Ogtolerance = 0.01
    
    for bone in SK.data.edit_bones:
#        BoneName = bone 
        BoneIndicator = "Unknown"
                     
        if bone.parent == None:
            # BoneIndicator = "Root"
            RootCount =+1  
            a = np.array([0, 0, 0])
            
        else:
            Parent = bone.parent
            a = np.array([Parent.head.x, Parent.head.y, Parent.head.z])  
            
        #Identify enxtreme bones

        if bone.head.x > MaxX_distance:
            MaxX_distance = bone.head.x
            ExtremeXBone = bone.name # Should be most left finger bone
            ParentXList =  bone.parent_recursive 
            
        if bone.head.x < MinX_distance:
            MinX_distance = bone.head.x
            ExtremeNXBone = bone.name # Should be most right finger bone
            ParentNXList =  bone.parent_recursive  
            
        # Adjtolerance = (MaxX_distance - MinX_distance)/1000
        Adjtolerance = (MaxX_distance - MinX_distance)/250  # Might need to be adjusted based on the Skeleton
    print("MAX X:", (MaxX_distance - MinX_distance))
        # if Adjtolerance < Ogtolerance:
        #     tolerance = Adjtolerance
        # else: 
        #     tolerance = Ogtolerance

    return Adjtolerance    
        

def ArmatureBoneIdentifier(SK, tolerance):
    # obj = SK
    bpy.ops.object.mode_set(mode='EDIT')

    Max = max(bpy.data.objects[SK.name].dimensions.x, bpy.data.objects[SK.name].dimensions.y, bpy.data.objects[SK.name].dimensions.z)

    RootCount = 0
    MaxX_distance = 0
    MinX_distance = 0
    HeadZ = 0
    MinZ = Max + 1000
    MinNZ = Max + 1000
    Ogtolerance = 0.01
    BoneInfo = []
    # Label = []

    Matches = []

    a = np.array([0, 0, 0])
    
    for bone in SK.data.edit_bones:
#        BoneName = bone 
        BoneIndicator = "Unknown"
                     
        if bone.parent == None:
            # BoneIndicator = "Root"
            RootCount =+1  
            a = np.array([0, 0, 0])
            
        else:
            Parent = bone.parent
            a = np.array([Parent.head.x, Parent.head.y, Parent.head.z])  
            
        #Identify enxtreme bones

        if bone.head.x > MaxX_distance:
            MaxX_distance = bone.head.x
            ExtremeXBone = bone.name # Should be most left finger bone
            ParentXList =  bone.parent_recursive 
            
        if bone.head.x < MinX_distance:
            MinX_distance = bone.head.x
            ExtremeNXBone = bone.name # Should be most right finger bone
            ParentNXList =  bone.parent_recursive  
                 
        
        if (-MinZ < bone.head.z < MinZ) and (bone.head.x>0+tolerance):
            MinZ = bone.head.z
            ExtremeZBone = bone.name # Should be left toe
            ParentZList =  bone.parent_recursive   

        if (-MinNZ < bone.head.z < MinNZ) and (bone.head.x<0-tolerance):
            MinNZ = bone.head.z
            ExtremeNZBone = bone.name # Should be right toe
            ParentNZList =  bone.parent_recursive   


        if (bone.head.z > HeadZ):
            HeadZ= bone.head.z
            ExtremePZBone = bone.name # Should be hair or somethin
            
            ParentPZList =  bone.parent_recursive  


        b = np.array([bone.head.x, bone.head.y,  bone.head.z])
        dist = np.linalg.norm(a-b)
        
        BoneInformation = bone#,  BoneIndicator, dist
        BoneInfo.append(bone.name)
        BoneInfoSize = len(BoneInfo)
        
#    print("ExtremeXBone", ExtremeXBone)
#    print("ExtremeNXBone", ExtremeNXBone)
#    print("ExtremeZBone", ExtremeZBone)
#    print("ExtremeNZBone", ExtremeNZBone)

    print("ExtremeBones:")
    print(ExtremeXBone, ExtremeNXBone, ExtremeZBone, ExtremeNZBone, ExtremePZBone)


    #Trace back to the bones at the center of the skeleton (he upper spine and the pelvis or what I call the Abr and the Noic respectively)

#Trace from the left hand
    for parent in ParentXList:
        DeltaX = parent.head.x
#        DeltaX = parent.tail.x - parent.head.x
        if DeltaX <= tolerance:
            Abr = parent
            AbrName = Abr.name
            print("Abr",Abr.name)
            index = ParentXList.index(Abr)
            print("Index is", index )
            break


#Trace from the right hand
    for parent in ParentNXList:
        DeltaX = parent.head.x
#        DeltaX = parent.tail.x - parent.head.x
        if DeltaX >= -tolerance:
            NAbr = parent
            NAbrName = NAbr.name
            print("NAbr",NAbr.name)
            Nindex = ParentNXList.index(NAbr)
            print("NIndex is", Nindex )
            break

#Trace from the left foot   
    for parent in ParentZList:
        DeltaXz = parent.head.x
#        DeltaX = parent.tail.x - parent.head.x
        if -tolerance <= DeltaXz <= tolerance:
            Noic = parent
            NoicName = Noic.name
            print("Noic",Noic.name)
            Zindex = ParentZList.index(Noic)
            print("ZIndex is", Zindex )
            break

#Trace from the right foot  
    for parent in ParentNZList:
        DeltaNXz = parent.head.x
#        DeltaX = parent.tail.x - parent.head.x
        if -tolerance <= DeltaNXz <= tolerance:
            NNoic = parent
            NNoicName = NNoic.name
            print("NNoic",NNoic.name)
            NZindex = ParentNZList.index(NNoic)
            print("NZIndex is", NZindex )
            break

#Find parent index for the head
    PZindex = ParentPZList.index(Abr)

# Trace and identify for Spine1
    Idric =None
    for spine in Abr.parent_recursive:
        if spine.parent == Noic or spine.parent == Noic.parent:
            Idric = spine
            IdricName = Idric.name
            break


#         DeltaX = parent.head.x
# #        DeltaX = parent.tail.x - parent.head.x
#         if DeltaX <= tolerance:
#             Abr = parent
#             AbrName = Abr.name
#             print("Abr",Abr.name)
#             index = ParentXList.index(Abr)
#             print("Index is", index )
#             break

             
        
    for i in range(BoneInfoSize):
        BoneIndicator = "Unknown"

        BoneName = BoneInfo[i]
        
#        if bone.parent == None:
#            Label.append("Left Shoulder")

        if BoneName == ParentPZList[PZindex-1].name:
            BoneIndicator = "Neck"

        elif BoneName == ParentPZList[PZindex-2].name:
            BoneIndicator = "Head"

        elif BoneName == AbrName and BoneName == NAbrName:
            BoneIndicator = "Spine2"

        elif Idric != None and BoneName == Idric.name:
            BoneIndicator = "Spine1"

        elif BoneName == ParentXList[index-1].name:
            BoneIndicator = "L_Shoulder"
            # Label.append("L_Shoulder")
            
        elif BoneName == ParentXList[index-2].name:
            BoneIndicator = "L_Arm"
            # Label.append("L_Arm")
            
        elif BoneName == ParentXList[index-3].name:
            BoneIndicator = "L_ForeArm"
            # Label.append("L_ForeArm")
            
        elif BoneName == ParentXList[index-4].name:
            BoneIndicator = "L_Hand"
            # Label.append("L_Hand")
            
        elif BoneName == ParentNXList[Nindex-1].name:
            BoneIndicator = "R_Shoulder"
            # Label.append("R_Shoulder")
            
        elif BoneName == ParentNXList[Nindex-2].name:
            BoneIndicator = "R_Arm"
            # Label.append("R_Arm")
            
        elif BoneName == ParentNXList[Nindex-3].name:
            BoneIndicator = "R_ForeArm"
            # Label.append("R_ForeArm")
            
        elif BoneName == ParentNXList[Nindex-4].name:
            BoneIndicator = "R_Hand"
            # Label.append("R_Hand")



        elif BoneName == NoicName and BoneName == NNoicName:
            BoneIndicator = "Hip"
            
        elif BoneName == ParentZList[Zindex-1].name:
            BoneIndicator = "L_UpLeg"
            # Label.append("L_UpLeg")
            
        elif BoneName == ParentZList[Zindex-2].name:
            BoneIndicator = "L_Leg"
            # Label.append("L_Leg")
            
        elif BoneName == ParentZList[Zindex-3].name:
            BoneIndicator = "L_Foot"
            # Label.append("L_Foot")
            
        elif BoneName == ExtremeZBone:
            BoneIndicator = "L_Toe"
            # Label.append("L_Toe")
            
        elif BoneName == ParentNZList[NZindex-1].name:
            BoneIndicator = "R_UpLeg"
            # Label.append("R_UpLeg")
            
        elif BoneName == ParentNZList[NZindex-2].name:
            BoneIndicator = "R_Leg"
            # Label.append("R_Leg")
            
        elif BoneName == ParentNZList[NZindex-3].name:
            BoneIndicator = "R_Foot"
            # Label.append("R_Foot")
            
        elif BoneName == ExtremeNZBone:
            BoneIndicator = "R_Toe"
            # Label.append("R_Toe")

        elif SK.data.edit_bones[BoneName].parent == None:
            BoneIndicator = "MODEL_00"
        # else:
        #     Label.append(BoneIndicator)
            
        if BoneIndicator != "Unknown":
            Matches.append([BoneName, BoneIndicator])

    #Add a mechanism to check ymmetry and confirm Abr here (especially for chars that have wings)
    
    #Children with max distance
    
#    TestIndex = BoneInformation[1].index(ParentXList[index-1])
#    print("Test index ", TestIndex)


    print( ParentXList[index-1].name, "---->", "L_Shoulder")
    print(ParentXList[index-2].name,"---->", "L_Arm")
    print(ParentXList[index-3].name, "---->","L_ForeArm")
    print( ParentXList[index-4].name, "---->", "L_Hand")
        
        
    print("Lowest: ",ExtremeZBone)
    print(ParentZList[Zindex-1].name, "---->", "L_UpLeg" )
    print(ParentZList[Zindex-2].name, "---->","L_Leg")
    print(ParentZList[Zindex-3].name,"---->", "L_Foot")
    print(ExtremeZBone,"---->", "L_Toe")
    
#        print(BoneInfo) 
#        print(bone.name, bone.head, bone.tail, BoneIndicator)  
  
    
    print(RootCount, ExtremeXBone)
#    print(Label[132], BoneInfo[132].name)

    bpy.ops.object.mode_set(mode='OBJECT')
    
    return Matches


def ArmatureHandIdentifier(SK, tolerance, InitialMatches):

    Max = max(bpy.data.objects[SK.name].dimensions.x, bpy.data.objects[SK.name].dimensions.y, bpy.data.objects[SK.name].dimensions.z)

    RootCount = 0
    MaxX_distance = 0
    MinX_distance = 0


    MinX = 2*Max
    MinNX = 2*Max
    # MaxChainIndex = 0
    MinLvl = len(SK.data.edit_bones)

    HeadZ = 0
    MinZ = Max + 1000
    MinNZ = Max + 1000
    Ogtolerance = 0.01
    BoneInfo = []
    # Label = []

    FingerTipNames = []
    FingerBaseNames = []

    a = np.array([0, 0, 0])
    # obj = SK
    bpy.ops.object.mode_set(mode='EDIT')
    for item in InitialMatches:
        if item[1]=="R_Hand" or item[1]=="L_Hand":
            if item[1]=="R_Hand":
                Right_Hand = item[0]
            else:
                Left_Hand = item[0]

            for bone in SK.data.edit_bones:
                if bone.name == item[0]:


                    for Child in bone.children_recursive:
                        Dist = bone.head - Child.head

                        Lvl = Child.parent_recursive.index(bone)

                        if len(Child.children) == 0 and  1 < Lvl < 10:
                            #Narrows to fingertips

                            FingerTipNames.append(Child.name)

                            if Lvl < MinLvl:
                                MinLvl = Lvl

                            print(Child.name, Lvl, Dist.length)
                            # print(MinX, MinNX)

                            if Dist.length < MinX and Child.head.x > 0: #left thumb tip
                                # print("Whatever1")
                                MinX = Dist.length
                                Left_Thumb_Tip = Child.name

                            if Dist.length < MinNX and Child.head.x < 0: #Right thumb tip
                                # print("Whatever1")
                                MinNX = Dist.length
                                Right_Thumb_Tip = Child.name

    print("LMAO", Left_Thumb_Tip, Right_Thumb_Tip)

    Left_Hand_bone = SK.data.edit_bones[Left_Hand]
    Right_Hand_bone = SK.data.edit_bones[Right_Hand]

    Left_Thumb_Tip_bone = SK.data.edit_bones[Left_Thumb_Tip]
    Right_Thumb_Tip_bone = SK.data.edit_bones[Right_Thumb_Tip]


    #Find the beginning of finger bone chains (Check whether Null is a thing or not)
    for FingerName in FingerTipNames:
        Finger = SK.data.edit_bones[FingerName]
        MaxSep = 0
        for Middlebone in Finger.parent_recursive:
            if Middlebone == Left_Hand_bone or Middlebone == Right_Hand_bone:
                break
            else:
                SpctVec =  Middlebone.parent.head - Middlebone.head
                Spc = SpctVec.length
                if Spc > MaxSep:
                    MaxSep = Spc
                    FingerChainStart = Middlebone.name
                    # if chainIndx > MaxChainIndex:
                    #    MaxChainIndex =  chainIndx 
        
        print(FingerChainStart)
        # print(FingerChainStart, chainIndx, MaxChainIndex)

        #Skip for thumb bones cause they're usually incorrect
        if Finger != Left_Thumb_Tip_bone and Finger != Right_Thumb_Tip_bone:
            FingerBaseNames.append(FingerChainStart) #Contains finger base bone names without thumbs


    # print(FingerBaseNames)       

    # Add correct thumb bone start
    RandomFingerBaseBone = SK.data.edit_bones[FingerBaseNames[0]]
    for Kid in RandomFingerBaseBone.children_recursive:
        if Kid.name in FingerTipNames:
            KidLvl = Kid.parent_recursive.index(RandomFingerBaseBone)
            break

    FullFingerBaseNames = FingerBaseNames.copy() #Full bone base names with thumbs

    Left_Thumb_Base_bone = Left_Thumb_Tip_bone.parent_recursive[KidLvl]
    Right_Thumb_Base_bone = Right_Thumb_Tip_bone.parent_recursive[KidLvl]
    FullFingerBaseNames.append(Left_Thumb_Base_bone.name)
    FullFingerBaseNames.append(Right_Thumb_Base_bone.name)

    print(FingerBaseNames)   




    FingerBaseContainer = FingerBaseNames.copy() # To remove items from

    #Classify index Bones
    PeakLeftThumbSpacing = Max 
    PeakRightThumbSpacing = Max  
    print(Max)

    
    for FingrBase in FingerBaseContainer:
        FingerBaseBone = SK.data.edit_bones[FingrBase]
        if FingerBaseBone == Left_Thumb_Base_bone or FingerBaseBone == Right_Thumb_Base_bone:
            pass
        else:
            if FingerBaseBone.head.x > 0: #For left hand FingerBaseBones
                LeftHandThumbAxis = Left_Thumb_Base_bone.head - Left_Hand_bone.head
                # FingrboneSpcVec =  Left_Thumb_Base_bone.head - FingerBaseBone.head
                LeftThumbProjection = LeftHandThumbAxis.dot(Left_Thumb_Base_bone.head - FingerBaseBone.head)

                if LeftThumbProjection < PeakLeftThumbSpacing:
                    PeakLeftThumbSpacing = LeftThumbProjection
                    LeftIndexBaseBoneName = FingrBase

                print("Left",FingrBase, LeftThumbProjection)
               
               
            elif FingerBaseBone.head.x < 0: #For right hand FingerBaseBones
                RightHandThumbAxis = Right_Thumb_Base_bone.head - Right_Hand_bone.head
                # FingrboneSpcVec =  Right_Thumb_Base_bone.head - FingerBaseBone.head
                RightThumbProjection = RightHandThumbAxis.dot(Right_Thumb_Base_bone.head - FingerBaseBone.head)
                
                if RightThumbProjection < PeakRightThumbSpacing:
                    PeakRightThumbSpacing = RightThumbProjection
                    RightIndexBaseBoneName = FingrBase

                print("Right",FingrBase, RightThumbProjection)
                
    
    FingerBaseContainer.remove(LeftIndexBaseBoneName)
    FingerBaseContainer.remove(RightIndexBaseBoneName)
    print(Max)
    print("Index",LeftIndexBaseBoneName,RightIndexBaseBoneName)


    #Classify middle Bones
    PeakLeftThumbSpacing = Max 
    PeakRightThumbSpacing = Max  
    print(Max)

    
    for FingrBase in FingerBaseContainer:
        FingerBaseBone = SK.data.edit_bones[FingrBase]
        if FingerBaseBone == Left_Thumb_Base_bone or FingerBaseBone == Right_Thumb_Base_bone:
            pass
        else:
            if FingerBaseBone.head.x > 0: #For left hand FingerBaseBones
                LeftHandThumbAxis = Left_Thumb_Base_bone.head - Left_Hand_bone.head
                # FingrboneSpcVec =  Left_Thumb_Base_bone.head - FingerBaseBone.head
                LeftThumbProjection = LeftHandThumbAxis.dot(Left_Thumb_Base_bone.head - FingerBaseBone.head)

                if LeftThumbProjection < PeakLeftThumbSpacing:
                    PeakLeftThumbSpacing = LeftThumbProjection
                    LeftMiddleBaseBoneName = FingrBase

                # print("Left",FingrBase, LeftThumbProjection)
               
               
            elif FingerBaseBone.head.x < 0: #For right hand FingerBaseBones
                RightHandThumbAxis = Right_Thumb_Base_bone.head - Right_Hand_bone.head
                # FingrboneSpcVec =  Right_Thumb_Base_bone.head - FingerBaseBone.head
                RightThumbProjection = RightHandThumbAxis.dot(Right_Thumb_Base_bone.head - FingerBaseBone.head)
                
                if RightThumbProjection < PeakRightThumbSpacing:
                    PeakRightThumbSpacing = RightThumbProjection
                    RightMiddleBaseBoneName = FingrBase

                # print("Right",FingrBase, RightThumbProjection)
                
    
    FingerBaseContainer.remove(LeftMiddleBaseBoneName)
    FingerBaseContainer.remove(RightMiddleBaseBoneName)
    print(Max)
    print("Middle",LeftMiddleBaseBoneName,RightMiddleBaseBoneName)


    #Classify ring Bones
    PeakLeftThumbSpacing = Max 
    PeakRightThumbSpacing = Max  
    print(Max)

    
    for FingrBase in FingerBaseContainer:
        FingerBaseBone = SK.data.edit_bones[FingrBase]
        if FingerBaseBone == Left_Thumb_Base_bone or FingerBaseBone == Right_Thumb_Base_bone:
            pass
        else:
            if FingerBaseBone.head.x > 0: #For left hand FingerBaseBones
                LeftHandThumbAxis = Left_Thumb_Base_bone.head - Left_Hand_bone.head
                # FingrboneSpcVec =  Left_Thumb_Base_bone.head - FingerBaseBone.head
                LeftThumbProjection = LeftHandThumbAxis.dot(Left_Thumb_Base_bone.head - FingerBaseBone.head)

                if LeftThumbProjection < PeakLeftThumbSpacing:
                    PeakLeftThumbSpacing = LeftThumbProjection
                    LeftRingBaseBoneName = FingrBase

                # print("Left",FingrBase, LeftThumbProjection)
               
               
            elif FingerBaseBone.head.x < 0: #For right hand FingerBaseBones
                RightHandThumbAxis = Right_Thumb_Base_bone.head - Right_Hand_bone.head
                # FingrboneSpcVec =  Right_Thumb_Base_bone.head - FingerBaseBone.head
                RightThumbProjection = RightHandThumbAxis.dot(Right_Thumb_Base_bone.head - FingerBaseBone.head)
                
                if RightThumbProjection < PeakRightThumbSpacing:
                    PeakRightThumbSpacing = RightThumbProjection
                    RightRingBaseBoneName = FingrBase

                # print("Right",FingrBase, RightThumbProjection)
                
    
    FingerBaseContainer.remove(LeftRingBaseBoneName)
    FingerBaseContainer.remove(RightRingBaseBoneName)
    print(Max)
    print("Ring",LeftRingBaseBoneName,RightRingBaseBoneName)




    #Classify Pinky Bones
    PeakLeftThumbSpacing = Max 
    PeakRightThumbSpacing = Max  
    print(Max)

    
    for FingrBase in FingerBaseContainer:
        FingerBaseBone = SK.data.edit_bones[FingrBase]
        if FingerBaseBone == Left_Thumb_Base_bone or FingerBaseBone == Right_Thumb_Base_bone:
            pass
        else:
            if FingerBaseBone.head.x > 0: #For left hand FingerBaseBones
                LeftHandThumbAxis = Left_Thumb_Base_bone.head - Left_Hand_bone.head
                # FingrboneSpcVec =  Left_Thumb_Base_bone.head - FingerBaseBone.head
                LeftThumbProjection = LeftHandThumbAxis.dot(Left_Thumb_Base_bone.head - FingerBaseBone.head)

                if LeftThumbProjection < PeakLeftThumbSpacing:
                    PeakLeftThumbSpacing = LeftThumbProjection
                    LeftPinkyBaseBoneName = FingrBase

                # print("Left",FingrBase, LeftThumbProjection)
               
               
            elif FingerBaseBone.head.x < 0: #For right hand FingerBaseBones
                RightHandThumbAxis = Right_Thumb_Base_bone.head - Right_Hand_bone.head
                # FingrboneSpcVec =  Right_Thumb_Base_bone.head - FingerBaseBone.head
                RightThumbProjection = RightHandThumbAxis.dot(Right_Thumb_Base_bone.head - FingerBaseBone.head)
                
                if RightThumbProjection < PeakRightThumbSpacing:
                    PeakRightThumbSpacing = RightThumbProjection
                    RightPinkyBaseBoneName = FingrBase

                # print("Right",FingrBase, RightThumbProjection)
                
    
    FingerBaseContainer.remove(LeftPinkyBaseBoneName)
    FingerBaseContainer.remove(RightPinkyBaseBoneName)
    print(Max)
    print("Pinky",LeftPinkyBaseBoneName,RightPinkyBaseBoneName)


    

    print(Lvl)
    lvlThreshold = 1
    #Start with the left hand
    #For the thumb
    InitialMatches.append([Left_Thumb_Base_bone.name, "L_Thumb1"])
    InitialMatches.append([Left_Thumb_Base_bone.children_recursive[0].name, "L_Thumb2"])
    InitialMatches.append([Left_Thumb_Base_bone.children_recursive[1].name, "L_Thumb3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([Left_Thumb_Base_bone.children_recursive[2].name, "L_Thumb4__null"])

    #For the index
    InitialMatches.append([LeftIndexBaseBoneName, "L_Index1"])
    InitialMatches.append([SK.data.edit_bones[LeftIndexBaseBoneName].children_recursive[0].name, "L_Index2"])
    InitialMatches.append([SK.data.edit_bones[LeftIndexBaseBoneName].children_recursive[1].name, "L_Index3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[LeftIndexBaseBoneName].children_recursive[2].name, "L_Index4__null"])


    #For the middle
    InitialMatches.append([LeftMiddleBaseBoneName, "L_Middle1"])
    InitialMatches.append([SK.data.edit_bones[LeftMiddleBaseBoneName].children_recursive[0].name, "L_Middle2"])
    InitialMatches.append([SK.data.edit_bones[LeftMiddleBaseBoneName].children_recursive[1].name, "L_Middle3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[LeftMiddleBaseBoneName].children_recursive[2].name, "L_Middle4__null"])


    #For the ring
    InitialMatches.append([LeftRingBaseBoneName, "L_Ring1"])
    InitialMatches.append([SK.data.edit_bones[LeftRingBaseBoneName].children_recursive[0].name, "L_Ring2"])
    InitialMatches.append([SK.data.edit_bones[LeftRingBaseBoneName].children_recursive[1].name, "L_Ring3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[LeftRingBaseBoneName].children_recursive[2].name, "L_Ring4__null"])


    #For the pinky
    InitialMatches.append([LeftPinkyBaseBoneName, "L_Pinky1"])
    InitialMatches.append([SK.data.edit_bones[LeftPinkyBaseBoneName].children_recursive[0].name, "L_Pinky2"])
    InitialMatches.append([SK.data.edit_bones[LeftPinkyBaseBoneName].children_recursive[1].name, "L_Pinky3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[LeftPinkyBaseBoneName].children_recursive[2].name, "L_Pinky4__null"])




    #Start with the right hand
    #For the thumb
    InitialMatches.append([Right_Thumb_Base_bone.name, "R_Thumb1"])
    InitialMatches.append([Right_Thumb_Base_bone.children_recursive[0].name, "R_Thumb2"])
    InitialMatches.append([Right_Thumb_Base_bone.children_recursive[1].name, "R_Thumb3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([Right_Thumb_Base_bone.children_recursive[2].name, "R_Thumb4__null"])

    #For the index
    InitialMatches.append([RightIndexBaseBoneName, "R_Index1"])
    InitialMatches.append([SK.data.edit_bones[RightIndexBaseBoneName].children_recursive[0].name, "R_Index2"])
    InitialMatches.append([SK.data.edit_bones[RightIndexBaseBoneName].children_recursive[1].name, "R_Index3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[RightIndexBaseBoneName].children_recursive[2].name, "R_Index4__null"])


    #For the middle
    InitialMatches.append([RightMiddleBaseBoneName, "R_Middle1"])
    InitialMatches.append([SK.data.edit_bones[RightMiddleBaseBoneName].children_recursive[0].name, "R_Middle2"])
    InitialMatches.append([SK.data.edit_bones[RightMiddleBaseBoneName].children_recursive[1].name, "R_Middle3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[RightMiddleBaseBoneName].children_recursive[2].name, "R_Middle4__null"])


    #For the ring
    InitialMatches.append([RightRingBaseBoneName, "R_Ring1"])
    InitialMatches.append([SK.data.edit_bones[RightRingBaseBoneName].children_recursive[0].name, "R_Ring2"])
    InitialMatches.append([SK.data.edit_bones[RightRingBaseBoneName].children_recursive[1].name, "R_Ring3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[RightRingBaseBoneName].children_recursive[2].name, "R_Ring4__null"])


    #For the pinky
    InitialMatches.append([RightPinkyBaseBoneName, "R_Pinky1"])
    InitialMatches.append([SK.data.edit_bones[RightPinkyBaseBoneName].children_recursive[0].name, "R_Pinky2"])
    InitialMatches.append([SK.data.edit_bones[RightPinkyBaseBoneName].children_recursive[1].name, "R_Pinky3"])
    if MinLvl > lvlThreshold:
        InitialMatches.append([SK.data.edit_bones[RightPinkyBaseBoneName].children_recursive[2].name, "R_Pinky4__null"])



    # print(Test)

    bpy.ops.object.mode_set(mode='OBJECT')

    return InitialMatches



#___________________________________________________________________
        

#___________________Simplifier_______________________

def VertexGroupMerger(SK, BoneSubstrgList):
# Takes the SK's children and starts merging the VG groups of the bones containing the substring in BoneSubstrgList (Has no external dependencies)
    
    bpy.ops.object.mode_set(mode='OBJECT')

    ArmatureA = SK #bpy.context.active_object #self.Skeleton
    

    for bone in reversed(ArmatureA.data.bones):

        Influence = True # Assume that the bone has direct influence on the mesh
        BoneName = bone.name

        for name in BoneSubstrgList:
            if name == "" or name.isspace():
                continue

            # if bone.name.lower().find(name)!=-1 and (bone.parent != None):
            elif bone.name.find(name)!=-1 and (bone.parent != None):
                print(bone.name , "------->", bone.parent.name)
        
                for mesh in ArmatureA.children:
                    

        #                mesh.select_set(True)
                    bpy.context.view_layer.objects.active = mesh

                    # print(bone.name)
        
                    verts = mesh.data.vertices
                    NumVerts = len(verts)
                    VertIndices = range (NumVerts)
                    

                    try:
                        GroupA = mesh.vertex_groups[bone.parent.name]
                    except:
                        try: #to bypass the root bone cause it has no parent
                            GA = mesh.vertex_groups.new(name=bone.parent.name) 
                            GA.add(VertIndices, 0, 'ADD')
                            #Generate the group A
                        except:
                            pass
                    try:
                        GroupB = mesh.vertex_groups[BoneName]
                    except:
                        GB = mesh.vertex_groups.new(name=bone.name) 
                        GB.add(VertIndices, 0, 'ADD')
                        Influence = False
                    #Generate the group B
                        
                    
        #             for name in BoneSubstrgList:
        #                 # if bone.name.lower().find(name)!=-1 and (bone.parent != None):
        #                 if bone.name.find(name)!=-1 and (bone.parent != None):
        # #                if fnmatch.fnmatchcase(bone.name, name):#"*offset") or fnmatch.fnmatchcase(bone.name, "*null") or fnmatch.fnmatchcase(bone.name, "*group") or fnmatch.fnmatchcase(bone.name, "*BASE"):
        # #                        VGmerge(bone.parent.name, bone.name)
                    # print(bone.name , "------->", bone.parent.name)
                        

                    #Check if VG has any influence on the mesh
                    # if Influence == True: #Thoroughly test for vertex influence on the mesh
                    #     Verts = [vert for vert in mesh.data.vertices if (mesh.vertex_groups[bone.name].index in [i.group for i in vert.groups if i.weight != 0])] # Contains all the verts belonging to a particular group
                    #     if len(Verts)!=0: 
                    #         Influence == True

                    if Influence == True:
                        bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')
                        
                        modname = bpy.context.object.modifiers.active.name
                        
                        bpy.context.object.modifiers[modname].vertex_group_a = bone.parent.name
                        bpy.context.object.modifiers[modname].vertex_group_b = bone.name
                        bpy.context.object.modifiers[modname].mix_mode = 'ADD'
                        bpy.context.object.modifiers[modname].mix_set = 'ALL'

                        bpy.ops.object.modifier_move_to_index(modifier=modname, index=0)

                        bpy.ops.object.modifier_apply(modifier=modname)
                    
                break
                        

            bpy.context.view_layer.objects.active = SK 


def ArmatureStructureFixer(SK, PrsvState):
#Realligns the bones so that they're visually connected (not actually connected) to their main children.

#TODO: look into bone annihilation in this code when S == 0 or child.head == parent.head
#TODO: Remove Tekken 7 dependency  for Neck bones

    obj = SK #context.object #self.Skeleton

    bpy.ops.object.mode_set(mode='EDIT')

#    print(obj)

    for bone in obj.data.edit_bones:
        
#        bone.use_connect = False#Remove bone connections cause tekken dont have those
        # if bone.use_connect == True:
        #     pass

        Connected = False

        for WildChild in bone.children:
            try:
                Cntstatus = WildChild.use_connect
                if Cntstatus == True:
                    Connected = True
                    # print(bone.name, "Connect to", WildChild.name)
                    break
            except:
                pass

        if Connected == False:# and bone.use_connect == False:
            BoneName = bone
            HT = bone.vector / bone.length
            NumOfChldrn = len(bone.children)
            
            try:
                Lvl = bone.parent_recursive.index(obj.data.edit_bones["Neck"])
                print(Lvl)
            except:
                
                if NumOfChldrn == 1:
    #                pass
        #            Location_child = bone.children[0].head
                    S = HT.dot(bone.head - bone.children[0].head)
                    print(bone.name, S)
    #                    if S > 0.01*bone.length: 
                    if PrsvState == True and not isclose(0, S, abs_tol=0.0):            
                        bone.tail = bone.head - S*HT
                    elif PrsvState == False and bone.head != bone.children[0].head:
                        bone.tail = bone.children[0].head  
                        
    #                bone.tail = bone.head - S*HT 
        #            bone.tail = bone.children[0].head


                elif NumOfChldrn > 1:
            #        print("More" , len(bone.children), bone)
                    Parent_1 = bone
                    Bone_Counter1 = 0
                    for child in bone.children:
                        if len(child.children) > 0:
                            Bone_Counter1 += 1
                            Offspring = child
                            
                    if Bone_Counter1 == 1:                        
                        
                        S = HT.dot(Parent_1.head - Offspring.head)
                        if PrsvState == True and not isclose(0, S, abs_tol=0.0):
    #                    if S > 0.01*bone.length:            
                            Parent_1.tail = Parent_1.head - S*HT
                        elif PrsvState == False and Parent_1.head != Offspring.head:
                            Parent_1.tail = Offspring.head
                               
        #                Parent_1.tail = Offspring.head

                    else:
                        pass
            #            print("terminal")
                        loop_count = 0
                        
                        Sum = mathutils.Vector((0, 0, 0))
         
                        for child in Parent_1.children:
                            Sum += child.head

                        
        #                Parent_1.tail = Sum / len(Parent_1.children)
                        CommonPoint = Sum / len(Parent_1.children)
                        
                        S = HT.dot(Parent_1.head - CommonPoint)
                        if PrsvState == True and not isclose(0, S, abs_tol=0.0):
    #                    if S > 0.01*bone.length:            
                            Parent_1.tail = Parent_1.head - S*HT
                        elif PrsvState == False and Parent_1.head != Sum / len(Parent_1.children):
                            Parent_1.tail = Sum / len(Parent_1.children)
                        

                else:

                    try:
                        # bone.length = bone.parent.length
                        bone.tail = bone.head + bone.parent.vector
                    except:
                        pass

    bpy.ops.object.mode_set(mode='OBJECT')





def VGmerge(GroupA, GroupB):#Not even used for the most part
    bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')
    
    modname = bpy.context.object.modifiers.active.name
    
    bpy.context.object.modifiers[modname].vertex_group_a = GroupA
    bpy.context.object.modifiers[modname].vertex_group_b = GroupB
    bpy.context.object.modifiers[modname].mix_mode = 'ADD'
    bpy.context.object.modifiers[modname].mix_set = 'ALL'
    bpy.ops.object.modifier_move_to_index(modifier=modname, index=0)

    bpy.ops.object.modifier_apply(modifier=modname)
    

def TekkenExtraBoneRemover(SK, BoneSubstrgList):
#Removes all extra bones that have names containing the substring in BoneSubstrgList from the SK (string list is case sensitive)

    
    obj = SK #context.object #self.Skeleton

    bpy.ops.object.mode_set(mode='EDIT')
    
    for bone in obj.data.edit_bones:
        
        BoneName = bone
        for name in BoneSubstrgList:
            # print(name , "is it space?", name.isspace())
            if not name.isspace() and name != "":
                try:
    #                print(bone)
                    # if bone.name.lower().find(name)!=-1:
                    if bone.name.find(name)!=-1:#"*offset") or fnmatch.fnmatchcase(bone.name, "*null") or fnmatch.fnmatchcase(bone.name, "*group") or fnmatch.fnmatchcase(bone.name, "*BASE"):
    #                if fnmatch.fnmatchcase(bone.name, name):#"*offset") or fnmatch.fnmatchcase(bone.name, "*null") or fnmatch.fnmatchcase(bone.name, "*group") or fnmatch.fnmatchcase(bone.name, "*BASE"):
                        print(BoneName.name,name)
                        obj.data.edit_bones.remove(BoneName)
                        break
                except:
                    pass  
    print("Bones removed")    
            
    bpy.ops.object.mode_set(mode='OBJECT')       


def MeshObjectJoiner(SK):
#Joins seperate mesh children into one piece--->Complete
# TODO: Check and megre UV layers ---->DONE

    bpy.ops.object.mode_set(mode='OBJECT')


    ArmatureA = SK #bpy.context.active_object #self.Skeleton
    
    UVname = "UV1"
    UV_flag = False

    for mesh in ArmatureA.children:
        

        mesh.select_set(True)
        bpy.context.view_layer.objects.active = mesh

        
        
        for UV in mesh.data.uv_layers:

            if UV.active_render:
                
                if UV_flag == False:
                    UVname = UV.name
                    UV_flag = True
               
                mesh.data.uv_layers[UV.name].name = UVname

    if len(ArmatureA.children) > 1:
        bpy.ops.object.join()
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = SK
    print("Mesh joied")


def MeshObjectSeparator(SK):
#Joins seperate mesh children into one piece--->Complete
# TODO: Check and megre UV layers ---->DONE

    bpy.ops.object.mode_set(mode='OBJECT')


    ArmatureA = SK #bpy.context.active_object #self.Skeleton
    
    UVname = "UV1"
    UV_flag = False

    for mesh in ArmatureA.children:
        

        mesh.select_set(True)
        bpy.context.view_layer.objects.active = mesh

        
        
        # for UV in mesh.data.uv_layers:

        #     if UV.active_render:
                
        #         if UV_flag == False:
        #             UVname = UV.name
        #             UV_flag = True
               
        #         mesh.data.uv_layers[UV.name].name = UVname

    if len(ArmatureA.children) > 0:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='MATERIAL')
        bpy.ops.object.mode_set(mode='OBJECT')

        # bpy.ops.object.join()

        
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = SK
    print("Mesh joied")

# def MatCheck(RefMat, CompMat):
#     # TODO: Fix for materials without nodes
#     if (RefMat.node_tree != None and CompMat.node_tree != None):
#         if len(RefMat.node_tree.nodes) == len(CompMat.node_tree.nodes):
#             TestResult = False   # Assumption     
#             for Nindx, n in enumerate(RefMat.node_tree.nodes):
                
                
#                 #NO NEED FOR WHILE LOOP
#     #            while TestResult == False:
#     #            print("Please work you sick fuck")
#                 if n.type == CompMat.node_tree.nodes[Nindx].type:
#                     if n.type=='TEX_IMAGE':
#                         if n.image == CompMat.node_tree.nodes[Nindx].image:
#                             TestResult = True
#                         else: 
#                             TestResult = False
#                             break
#     #                else:
#     #                    TestResult = False
#     #                    break
#                 else:
#                     TestResult = False
#                     break
                        
                
                
#         else:
#             TestResult = False

#     else:
#         TestResult = False

    
# #    print(TestResult)
#     return TestResult
    

def MatCheck(RefMat, CompMat):
# Compares to material objects and returns true if they have exactly the same nodes. Used for MatSlotCombine(SK)

    # TODO: Fix for materials without nodes--->Done
    if (RefMat.node_tree != None and CompMat.node_tree != None):
        if len(RefMat.node_tree.nodes) == len(CompMat.node_tree.nodes):
            # TestResult = False   # Assumption     
            for Nindx, n in enumerate(RefMat.node_tree.nodes):
                
                
                #NO NEED FOR WHILE LOOP
    #            while TestResult == False:
    #            print("Please work you sick fuck")


                if n.type == CompMat.node_tree.nodes[Nindx].type:
                    if n.type=='TEX_IMAGE':
                        if n.image == CompMat.node_tree.nodes[Nindx].image:
                            print(n.image, CompMat.node_tree.nodes[Nindx].image)
                            return True
                        else:
                            return False
    #                     else: 
    #                         TestResult = False
    #                         break
    # #                else:
    # #                    TestResult = False
    # #                    break
    #             else:
    #                 TestResult = False
    #                 break
                        
                
                
    #     else:
    #         TestResult = False

    # else:
    #     TestResult = False

    
#    print(TestResult)
    return False


def MatSlotCombine(SK):
#COmbines material slots for a given SK's children ---COMPLETE

#    print("___________________________________")
# DONE--TODO: Fix for objects with 1 or no materials--

# LOOP THRU ALL OBJECTS IN THE SCENE
    bpy.ops.object.mode_set(mode='OBJECT')
    
    ArmatureA = SK #bpy.context.active_object #self.Skeleton
     
    for ob in ArmatureA.children:

#    for ob in bpy.context.scene.objects:
#        print("Object",ob)
        
        # IF THIS OBJECT IS A MESH (THAT IS: NO LIGHT, NO CAMERA...)
        if ob.type=='MESH':
            
            bpy.context.view_layer.objects.active = ob
            
            # IF THIS OBJECT HAS UVMAP
            if ob.data.uv_layers:
#                print("UV",ob.data.uv_layers)
            
                # IF THIS OBJECT HAS ANY MATERIAL
                Mat_List = ob.material_slots 
                for idx, mat in enumerate(ob.material_slots):
                    
                    NumOfSlots = len(ob.material_slots)
    #                Mat_List.remove(mat)
    #                forr mat2 in ob.material_slots:
                    SearchIndx = idx + 1
                    while SearchIndx < NumOfSlots:
#                        print(idx ,SearchIndx)
#                        print("Num of slots",len(ob.material_slots))
    #                for idy, mat2 in enumerate(ob.material_slots):


                        ob.active_material_index = SearchIndx #span slots                       
                    
                        mat2 = ob.material_slots[SearchIndx]
                        
                        if idx == SearchIndx:
                            SearchIndx += 1
    #                        pass
                        else: #(mat.material!= None and ob.active_material!= None): <--- part in () is unnecessary
                            Match = MatCheck(mat.material, ob.active_material)
                            if Match == True:
                                print(mat.material, " and",ob.active_material, " match" )
                                TempIndx = SearchIndx
                                while TempIndx > idx +1:
                            
                                    bpy.ops.object.material_slot_move(direction='UP')
                                    TempIndx = ob.active_material_index
                                    
                                bpy.ops.object.material_slot_remove()
                                NumOfSlots = len(ob.material_slots)
    #                            SearchIndx -= 1

                            else:
    #                            pass
                                SearchIndx += 1
                                
                    
                  
                        # IF THIS OBJECT DOESN'T HAVE UVMAP
            else:
                        
                # SELECT THIS OBJECT
                ob.select_set(True)
            
        # IF THIS OBJECT IS NOT MESH
        else:
                        
            # DESELECT THIS OBJECT
            ob.select_set(False)

print("Materials combined")    



def MeshVGMerger(GroupAname, GroupBname, mesh):
# Takes in a mesh object and two VG names and tries to merge them together

    verts = mesh.data.vertices
    NumVerts = len(verts)
    VertIndices = range (NumVerts)
    
    try:
        GroupA = mesh.vertex_groups[GroupAname]
    except:
        GA = mesh.vertex_groups.new(name=GroupAname) 
        GA.add(VertIndices, 0, 'ADD')
        #Generate the group A

    try:
        GroupB = mesh.vertex_groups[GroupBname]
    except:
        GB = mesh.vertex_groups.new(name=GroupBname) 
        GB.add(VertIndices, 0, 'ADD')
        #Generate the group B
        
    
    # for name in BoneSubstrgList:
    #     if bone.name.find(name)!=-1 and (bone.parent != None):
#                if fnmatch.fnmatchcase(bone.name, name):#"*offset") or fnmatch.fnmatchcase(bone.name, "*null") or fnmatch.fnmatchcase(bone.name, "*group") or fnmatch.fnmatchcase(bone.name, "*BASE"):
#                        VGmerge(bone.parent.name, bone.name)
    print(GroupBname , "------->", GroupAname)


    bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')
    
    modname = bpy.context.object.modifiers.active.name
    
    bpy.context.object.modifiers[modname].vertex_group_a = GroupAname
    bpy.context.object.modifiers[modname].vertex_group_b = GroupBname
    bpy.context.object.modifiers[modname].mix_mode = 'ADD'
    bpy.context.object.modifiers[modname].mix_set = 'ALL'

    bpy.ops.object.modifier_move_to_index(modifier=modname, index=0)

    bpy.ops.object.modifier_apply(modifier=modname)




#_______Reborn blend method script______
def ChangeBlendMode(SK, blndmode = 'HASHED'):
    for child in SK.children:
    
        for slot in child.material_slots:
            
            slot.material.blend_method = blndmode

#____________________________________________________________


#_________________Other_________________



# def OLDglTFArmatureExpander(SK, BoneSubstrgList = ["offset", "null"]):
# #Realligns the bones so that they're visually connected (not actually connected) to their main children.

# #TODO: look into bone annihilation in this code when S == 0 or child.head == parent.head
# #TODO: Remove Tekken 7 dependency  for Neck bones

#     obj = SK #context.object #self.Skeleton

#     bpy.ops.object.mode_set(mode='EDIT')



#     for bone in obj.data.edit_bones:
        
#         BoneName = bone
#         for name in BoneSubstrgList:
#             Sum = mathutils.Vector((0, 0, 0))
#             CommonPoint = mathutils.Vector((0, 0, 0))
#             try:
#                 if bone.name.find(name)==-1:
#                     for child in bone.children:
#                         if bone.name.find(name)==-1:
#                             Sum += child.head

#             except:
#                 pass
            
#             if len(bone.children)!=0:
#                 CommonPoint = Sum / len(bone.children)

#             if CommonPoint == mathutils.Vector((0, 0, 0)):
#                 pass
#             else:
#                 bone.tail = CommonPoint

#     bpy.ops.object.mode_set(mode='OBJECT')

def glTFArmatureExpander(SK, BoneSubstrgList = ["offset", "null"]):
#Realligns the bones so that they're visually connected (not actually connected) to their main children.

#TODO: look into bone annihilation in this code when S == 0 or child.head == parent.head
#TODO: Remove Tekken 7 dependency  for Neck bones

    obj = SK #context.object #self.Skeleton

    bpy.ops.object.mode_set(mode='EDIT')



    for bone in obj.data.edit_bones:
        
        BoneName = bone
        for name in BoneSubstrgList:
            Check = 0
            Sum = mathutils.Vector((0, 0, 0))
            CommonPoint = mathutils.Vector((0, 0, 0))
            try:
                if bone.name.find(name)==-1:
                    Check += 1
                    
                    for child in bone.children:
                        # if child.name.find(name)==-1 and Check >= 1:
                        Sum += child.head
                        # print("Check this out:",bone.name, name)

            except:
                pass

            if len(bone.children)!=0:
                CommonPoint = Sum / len(bone.children)

            HT = bone.vector / bone.length
            S = HT.dot(CommonPoint - bone.head)
            # print(S)

            if CommonPoint == mathutils.Vector((0, 0, 0)):
                pass
            elif S>0:
                bone.length = S
                # bone.tail = CommonPoint

    bpy.ops.object.mode_set(mode='OBJECT')


def AplPose(SK):
# Applies pose as rest pose--->COMPLETE

    
    bpy.ops.object.mode_set(mode='OBJECT')

    ArmatureA = SK #bpy.context.active_object #self.Skeleton

    for mesh in ArmatureA.children:
        

#                mesh.select_set(True)
        bpy.context.view_layer.objects.active = mesh

        #Check for extra armature modifiers
        ModTest = False
        for mod in bpy.context.object.modifiers:
            
            if mod.type == 'ARMATURE':
                UnWntdMod = mod.name
                if mod.object == SK and ModTest == False:
                    modname = mod.name
                    ModTest = True
                else: #remove duplicates and other armature modifiers
                    
                    bpy.ops.object.modifier_remove(modifier=UnWntdMod)


        bpy.ops.object.modifier_copy(modifier=modname)
        bpy.ops.object.modifier_move_to_index(modifier=modname, index=0)
        bpy.ops.object.modifier_apply(modifier=modname)

            
    bpy.context.view_layer.objects.active = SK
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')

        # bpy.ops.object.modifier_set_active(modifier="Armature")

                    

                
        # bpy.ops.object.modifier_copy(modifier="Armature")

        # modname = bpy.context.object.modifiers.active.name
    
        # bpy.context.object.modifiers[modname].vertex_group_a = GroupA

        # bpy.ops.object.modifier_apply(modifier=modname)



def FacialBoneFixer(SK, L, B0, B1, N, H):
# Fixes the facial bones for glTF regardless of their initial bone condition

    obj = SK

    LengthFlag = 0

    bpy.ops.object.mode_set(mode='EDIT')

    for boneO in reversed(obj.data.edit_bones):
        
        if boneO.name == "Neck":# or boneM.name == "HEAD":

            for bone in reversed(boneO.children_recursive):
    #            BoneName = bone.name
                
                
                HT = bone.vector / bone.length
                
                
                if LengthFlag == 0:       
                   length = bone.length
                   LengthFlag = 1
           
                
                Condition = (bone.name.find("Bero")!=-1) or (bone.name.find("Head")!=-1) or (bone.name.find("HEAD")!=-1) or (bone.name.find("Neck")!=-1)
                
                if Condition == False:
                    bone.roll = 1.5708285570144653
                    
                    bone.tail = bone.head + length*L
    #                print(bone.name, "way")
                    
                elif (bone.name.find("Bero1")!=-1) and (bone.name.find("pos")==-1):
                    bone.roll = -1.5708285570144653
                    S = HT.dot(bone.head - bone.children[0].head)
                    bone.tail = bone.head - S*B0
    #                print(bone.name, "no")
                    
                elif (bone.name.find("Bero")!=-1):
                    bone.roll = -1.5708285570144653
                    print(bone.children)
                    if bone.children != []:
                        S = HT.dot(bone.head - bone.children[0].head)
                        bone.tail = bone.head - S*B1
                    else:
                        bone.tail = bone.head + length*B1
    #                print(bone.name, "waat")
                    
                elif (bone.name.find("Neck")!=-1):
                    bone.roll = 1.5708285570144653
                    if bone.children != []:     
                        S = HT.dot(bone.head - bone.children[0].head)
                        bone.tail = bone.head - S*N
                    else:
                        bone.tail = bone.head + length*N
    #                print(bone.name, "neck")
                    
                else:
                    bone.roll = 0
                    if (bone.name.find("ATH")==-1):
                        
                        Sum = mathutils.Vector((0, 0, 0))
         
                        for child in bone.children:
                            Sum += child.head
                        if bone.children != []: 
                            
                            CommonPoint = Sum / len(bone.children)
                            S = HT.dot(bone.head - CommonPoint)
                        
                            bone.tail = bone.head - S*H
                    else:                 
                        bone.tail = bone.head + length*L
    #                print(bone.name, "shit")

    bpy.ops.object.mode_set(mode='OBJECT')




            
 




def BoneActiveMerger(Bonelst, ActiveBone):
# Merges bones in edit mode to the active bone

    # objname = ActiveBone.id_data.name
    # obj = bpy.data.objects.get(objname)

    for obb in bpy.data.objects: # to find the object linked to the armature ex: bpy.data.armatures['Armature.002'] = ? (bpy.data.objects['SK_CH_mar_bdf_higeuncle'])
        if obb.data == ActiveBone.id_data:
            obj = obb
            break

    actvbonename = ActiveBone.name

    # Bonelst = []
    # for Sbone in bpy.context.selected_bones:
    #     Bonelst.append(Sbone.name)

    # bpy.ops.object.mode_set(mode='EDIT')


    bpy.ops.object.mode_set(mode='OBJECT')

    for bone in Bonelst:
        if bone == actvbonename:
            pass
        else: #bone.id_data == ActiveBone.id_data:
            print("active",actvbonename)
            ActvName = actvbonename
            print("bone",bone)
            Slctd = bone
            # bpy.ops.object.mode_set(mode='OBJECT')
            for mesh in obj.children:

                # bpy.ops.object.mode_set(mode='OBJECT')

                bpy.context.view_layer.objects.active = mesh

                MeshVGMerger(ActvName, Slctd, mesh)
                # bpy.context.view_layer.objects.active = obj

                # bpy.ops.object.mode_set(mode='EDIT')

    bpy.context.view_layer.objects.active = obj   

    bpy.ops.object.mode_set(mode='EDIT')




def BoneParentMerger(Bonelst, ActiveBone):
# Merges bones in edit mode to their parent bones

    Armature = ActiveBone.id_data
    # print("objname",objname)
    # # obj = bpy.data.objects.get(objname)
    # obj = bpy.data.armatures[objname]

    for obb in bpy.data.objects: # to find the object linked to the armature ex: bpy.data.armatures['Armature.002'] = ? (bpy.data.objects['SK_CH_mar_bdf_higeuncle'])
        if obb.data == ActiveBone.id_data:
            obj = obb
            break

    actvbonename = ActiveBone.name

    # Bonelst = []
    # for Sbone in bpy.context.selected_bones:
    #     Bonelst.append(Sbone.name)


    # bpy.ops.object.mode_set(mode='EDIT')


    bpy.ops.object.mode_set(mode='OBJECT')

    for bone in Bonelst:
        bonedata = Armature.bones[bone]

        ActvName = None

        for parent in bonedata.parent_recursive:
            # ActvName = bonedata.parent.name
            if parent.name in Bonelst:
                # print(bonedata.name,"--",parent.parent.name)
                ActvName = parent.parent.name
                # pass
            elif ActvName == None:
                ActvName = bonedata.parent.name
#TODO: figure out a way to identify ansestirs -----Done



        # print("active",ActvName)
        # ActvName = bonedata.parent.name
        # print("bone",bone)
        Slctd = bonedata.name
        # bpy.ops.object.mode_set(mode='OBJECT')
        # print(obj)
        for mesh in obj.children:

            # bpy.ops.object.mode_set(mode='OBJECT')

            bpy.context.view_layer.objects.active = mesh

            MeshVGMerger(ActvName, Slctd, mesh)
            # bpy.context.view_layer.objects.active = obj

            # bpy.ops.object.mode_set(mode='EDIT')

    bpy.context.view_layer.objects.active = obj   

    bpy.ops.object.mode_set(mode='EDIT')




# def BoneRenamer(SK, refSK):
# # tries to find nearby mathcing bones between two skeletons and then rename them
 
# # TODO: Test this code again cause I think mathcing works here--->Done (It doesn't)
# # TODO: Fix matching--->Done via pose.bones instead of data.bones
# # TODO: Skip renaming for facial bones--->Done 
# # TODO: Skip renaming for booba bones--->


#     # obj = SK #context.object #self.Skeleton

#     bpy.ops.object.mode_set(mode='POSE')

# #    print(obj)
#     List = []
#     try:
#         Head = refSK.pose.bones["Head"]
#     except:
#         Head = refSK.pose.bones["HEAD"]

#     for bone in SK.pose.bones:
        
# #        bone.use_connect = False#Remove bone connections cause tekken dont have those
#         # if bone.use_connect == True:
#         #     pass
#         Trgtbone = None
        
#         Min = bone.length * 1
#         for refbone in refSK.pose.bones:
            
#             DistVec = refbone.head - bone.head
#             Dist = abs(DistVec.length)
#             Threshold = bone.length * 1
#             if Dist < Min and refbone.name not in [row[1] for row in List]: #
#                 Min = Dist
#                 Displacement = DistVec
#                 if Head not in refbone.parent_recursive and not Min > Threshold: # Skip certain bones
#                     Trgtbone = refbone
#                     print(bone.name,"--------->",refbone.name, Dist)

        
#         # print(refbone.name, Dist)
#         try:
#             # bone.translate(Displacement)

#             # print(bone.name,"--------->",Trgtbone.name)
#             List.append([bone.name,Trgtbone.name])
            
#             # bpy.ops.object.posemode_toggle()
#             # print("lol")
#             # bpy.ops.object.posemode_toggle()


#             # bone.name = Trgtbone.name
            
#         except:
#             pass
#     print(List)

#     bpy.ops.object.mode_set(mode='OBJECT')


def BonePoseNamePositionMove(SK , refSK):
    #_________________Function taking SK and refSk_________________
    #TODO: fix face and left hand---->Done
    #TODO: Make it work for non-PSK and non-Tekken skeletons---->Done

    bpy.ops.object.mode_set(mode='EDIT')

    for bone in SK.data.edit_bones:
    
        bone.use_connect = False


    bpy.ops.object.mode_set(mode='POSE')

    for bone in SK.pose.bones:

        for refbone in refSK.pose.bones:
            
            if refbone.name == bone.name:
                
                Target = refbone.head
                
                Source =   bone.head
                

                Disp =  -Source + Target 
                    
                AdjDisp = bone.matrix.to_3x3().inverted() @ Disp # Uninverted matrix actually gives the exact 3D cursor coordinates too

                bone.location = AdjDisp#.to_tuple()
                bpy.ops.object.posemode_toggle()
                bpy.ops.object.posemode_toggle()

    bpy.ops.object.mode_set(mode='OBJECT')   
#___________________________________________________________________

#_________________________T Poser______________________

def Quat_Rotate(SK, bone_name, Projaxis):
    bone = SK.pose.bones[bone_name]

    bone.rotation_mode = 'QUATERNION' # Convert rotation mode to quaternion
    
    Projection = Projaxis.dot(bone.y_axis)

    #Cap projection between -1 and 1
    if Projection > 1:
        Projection = 1
    elif Projection < -1:
        Projection = -1

    HalfAngle = -math.acos(Projection)/2
    GQuatVec = Projaxis.cross(bone.y_axis)
    QuatVec = bone.matrix.to_3x3().inverted() @ GQuatVec

    if math.isclose(QuatVec.length, 0,abs_tol = 0.0001):
        NormQuat = mathutils.Vector((0,0,0))
    else:
        NormQuat = (QuatVec/QuatVec.length)*math.sin(HalfAngle)

    Quat = mathutils.Quaternion((math.cos(HalfAngle),NormQuat[0],NormQuat[1],NormQuat[2]))

    bone.rotation_quaternion = bone.rotation_quaternion @ Quat
    bpy.ops.object.posemode_toggle()
    bpy.ops.object.posemode_toggle()

    return Quat


def Quat_Rotate_Roll(SK, bone_name, Projection, sidesign):

    bone = SK.pose.bones[bone_name]

    bone.rotation_mode = 'QUATERNION' # Convert rotation mode to quaternion
    

    #Cap projection between -1 and 1
    if Projection > 1:
        Projection = 1
    elif Projection < -1:
        Projection = -1

    HalfAngle = sidesign * math.acos(Projection)/2
    GQuatVec = bone.y_axis
    QuatVec = bone.matrix.to_3x3().inverted() @ GQuatVec

    if math.isclose(QuatVec.length, 0,abs_tol = 0.0001):
        NormQuat = mathutils.Vector((0,0,0))
    else:
        NormQuat = (QuatVec/QuatVec.length)*math.sin(HalfAngle)

    Quat = mathutils.Quaternion((math.cos(HalfAngle),NormQuat[0],NormQuat[1],NormQuat[2]))
    
    bone.rotation_quaternion = bone.rotation_quaternion @ Quat
    bpy.ops.object.posemode_toggle()
    bpy.ops.object.posemode_toggle()

    return Quat




def Armature_T_Poser(SK, X_axis, Z_axis, Neck_Spines, Left_Arm_Bones_No_Thumb, Right_Arm_Bones_No_Thumb, Leg_Bones, Left_Thumb, Right_Thumb):

    #Main reference axis for Tposing

    bpy.ops.object.mode_set(mode='POSE')
    SKDict = {bone.name: bone for bone in SK.pose.bones}
    sidesign = -1

    for bonename in Neck_Spines:
        if (bonename in SKDict):
            Projaxis = Z_axis

            Quat = Quat_Rotate(SK, bonename, Projaxis)
            # bone.rotation_quaternion = bone.rotation_quaternion @ Quat
            # bpy.ops.object.posemode_toggle()
            # bpy.ops.object.posemode_toggle()


    for bonename in Leg_Bones:
        if (bonename in SKDict):
            Projaxis = -Z_axis

            Quat = Quat_Rotate(SK, bonename, Projaxis)
            # bone.rotation_quaternion = bone.rotation_quaternion @ Quat
            # bpy.ops.object.posemode_toggle()
            # bpy.ops.object.posemode_toggle()



    for bonename in Left_Arm_Bones_No_Thumb:
        if (bonename in SKDict):
            Projaxis = X_axis 

            Quat = Quat_Rotate(SK, bonename, Projaxis)
            # bone.rotation_quaternion = bone.rotation_quaternion @ Quat
            # bpy.ops.object.posemode_toggle()
            # bpy.ops.object.posemode_toggle()

    if "L_Shoulder" in SKDict and "L_Shoulder" in Left_Arm_Bones_No_Thumb:
        PointingVec = -SK.pose.bones["L_Pinky1"].head + SK.pose.bones["L_Index1"].head
        PointingVec.x = 0 # get rid of x-component to make it a pure y-z 3D vector
        print( PointingVec)
        Projection = math.cos(math.atan(PointingVec.z/PointingVec.y))
        if PointingVec.z <= 0:
            sidesign = -1
        else:
            sidesign = 1

        Quat = Quat_Rotate_Roll(SK, "L_Shoulder", Projection, sidesign)

            

    for bonename in Right_Arm_Bones_No_Thumb:
        if (bonename in SKDict):
            Projaxis = -X_axis 

            Quat = Quat_Rotate(SK, bonename, Projaxis)
            # bone.rotation_quaternion = bone.rotation_quaternion @ Quat
            # bpy.ops.object.posemode_toggle()
            # bpy.ops.object.posemode_toggle()

    if "R_Shoulder" in SKDict and "R_Shoulder" in Left_Arm_Bones_No_Thumb:
        PointingVec = -SK.pose.bones["R_Pinky1"].head + SK.pose.bones["R_Index1"].head
        PointingVec.x = 0 # get rid of x-component to make it a pure y-z 3D vector
        print( PointingVec)
        Projection = math.cos(math.atan(PointingVec.z/PointingVec.y))
        if PointingVec.z >= 0:
            sidesign = -1
        else:
            sidesign = 1

        Quat = Quat_Rotate_Roll(SK, "R_Shoulder", Projection, sidesign)


    for bonename in Left_Thumb:
        if (bonename in SKDict):
            Projaxis = mathutils.Vector((0.8055111765861511, -0.5115827322006226, -0.2990565001964569)) 

            Quat = Quat_Rotate(SK, bonename, Projaxis)

    for bonename in Right_Thumb:
        if (bonename in SKDict):
            Projaxis = mathutils.Vector((-0.8055111765861511, -0.5115827322006226, -0.2990565001964569))

            Quat = Quat_Rotate(SK, bonename, Projaxis)


    bpy.ops.object.mode_set(mode='OBJECT')



def ArmatureBoneTailFix(SK,  BoneNameList):
    # OrgObj = context.object
#    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    # print("Armature fix is happening...")
    # obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    # print(SK.data.edit_bones)
    
    # LoopCounter1 = 0
    for bone in SK.data.edit_bones:
 
        bone.use_connect = False # Disconnect bones to make sure children don't follow the tips (or tail) of their parents

        NumOfChldrn = len(bone.children)

        if (bone.name == "Spine2"):
            try:
                bone.tail = SK.data.edit_bones["Neck"].head
            except:
                pass

        elif (bone.name == "L_Hand"):
            try:
                CenterPoint = (SK.data.edit_bones["L_Index1"].head + SK.data.edit_bones["L_Pinky1"].head)/2
                bone.tail = CenterPoint
            except:
                pass
        elif (bone.name == "R_Hand"):
            try:
                CenterPoint = (SK.data.edit_bones["R_Index1"].head + SK.data.edit_bones["R_Pinky1"].head)/2
                bone.tail = CenterPoint
            except:
                pass

        elif (NumOfChldrn == 1):
            # Location_child = bone.children[0].head
            bone.tail = bone.children[0].head
        elif (NumOfChldrn > 1): 
            for Baby in bone.children:
                if Baby.name in BoneNameList and bone.name != "Spine2" and bone.name != "Hip":
                    bone.tail = Baby.head



            # [Mesh for Mesh in SK.children].data.vertices

    bpy.ops.object.mode_set(mode='OBJECT')



def ArmatureFingerTipTailFix(SK, FingerTips):
    # OrgObj = context.object
#    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    # print("Armature fix is happening...")
    # obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    # print(SK.data.edit_bones)
    
    # LoopCounter1 = 0
    for Tip in FingerTips:
        try:
            bone = SK.data.edit_bones[Tip]
        except:
            continue
            # raise Exception("A fingertip bone is missing")   
 
        bone.use_connect = False # Disconnect bones to make sure children don't follow the tips (or tail) of their parents

        NumOfChldrn = len(bone.children)

        FingerTipCenter = mathutils.Vector((0,0,0))
        AvrgCounter = 0

        if NumOfChldrn == 0:
            MaxDist = 0
            for Mesh in SK.children:
            # Meshes = [Mesh for Mesh in SK.children]
            #Write a code that snaps the bone to the center of VGs
            #TODO: Needs optimization    
                try:
                    Mesh.vertex_groups[bone.name] # Test if VG even exists

                    Verts = [vert for vert in Mesh.data.vertices if (Mesh.vertex_groups[bone.name].index in [i.group for i in vert.groups if i.weight != 0])] # Contains all the verts belonging to a particular group 
                    for Vert in Verts:
                        VertGlobalCo = Mesh.matrix_basis.to_3x3() @ Vert.co
                        FingerTipCenter += Mesh.matrix_basis.to_3x3() @ Vert.co 
                        AvrgCounter += 1
                        if (bone.head - VertGlobalCo).length >= MaxDist:
                            FingerTip = VertGlobalCo

            # [vert for vert in bpy.context.object.data.vertices if bpy.context.object.vertex_groups['bone.name'].index in [i.group for i in vert.groups]]
                except:
                    pass

            # Fix fingertip based on vg center
            if AvrgCounter != 0:
                # print(FingerTipCenter / (AvrgCounter))
                bone.tail = (FingerTipCenter / (AvrgCounter)) #- bone.head
            else:
                bone.tail = bone.head + bone.parent.vector

            # Fix fingertip based on farthest vertex
            # bone.tail = FingerTip # This is messed up when tested on Hugo strange




            # [Mesh for Mesh in SK.children].data.vertices

    bpy.ops.object.mode_set(mode='OBJECT')


def ArmatureBoneHeadFix(SK, LimbJoints):
    # OrgObj = context.object
#    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    
    # obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    # print(SK.data.edit_bones)
    
    # LoopCounter1 = 0
    for bone in SK.data.edit_bones :
 
        bone.use_connect = False # Disconnect bones to make sure children don't follow the tips (or tail) of their parents

        if bone.name in LimbJoints:
            for Mesh in SK.children:
                sdfsdf = Mesh.ray_cast(bone.head, mathutils.Vector((0,0,1)))
                print(sdfsdf)
                pass
                #Incomplete code

    bpy.ops.object.mode_set(mode='OBJECT')


#__________________________Pose Snapper_________________

def bonedisconnet(SK):
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in SK.data.edit_bones:
        
        bone.use_connect = False

    bpy.ops.object.mode_set(mode='OBJECT')

def boneScaleInheritanceDisabler(SK):
    for bone in SK.data.bones:
        
        bone.inherit_scale = 'NONE'


def BonePoseSnapper(SK, RefSK, bonename):
    bone = SK.pose.bones[bonename]
    refbone = RefSK.pose.bones[bonename]

    Disp =  -bone.head + refbone.head 
        
    AdjDisp = bone.matrix.to_3x3().inverted() @ Disp # Uninverted matrix actually gives the exact 3D cursor coordinates too

#            print(bone.name ,  bone.head, Disp, AdjDisp)
    
    bone.location = bone.location + AdjDisp#.to_tuple()
    bpy.ops.object.posemode_toggle()
    bpy.ops.object.posemode_toggle()

def BonePoseSnapperWithCheck(SK, RefSK, bonename):
    bone = SK.pose.bones[bonename]
    refbone = RefSK.pose.bones[bonename]

    Rule = (bone.parent.head - bone.head).length
    Measure = (bone.parent.head - refbone.head).length

    # SK.data.bones[bonename].inherit_scale = 'NONE'

    if Measure >= Rule:
        Disp =  -bone.head + refbone.head 
            
        AdjDisp = bone.matrix.to_3x3().inverted() @ Disp # Uninverted matrix actually gives the exact 3D cursor coordinates too
  
        bone.location = bone.location + AdjDisp#.to_tuple()
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.posemode_toggle()
        # if bonename == "L_Hand":
        #     print("Hand dOOOne")


        # CurrentScaleSetting = SK.data.bones[bonename].inherit_scale
        # SK.data.bones[bonename].inherit_scale = 'NONE' # disable scale inheritance temporarily

        # Scale = Measure / Rule
        # bone.parent.scale[1] = bone.parent.scale[1] * Scale
        # SK.data.bones[bonename].inherit_scale = CurrentScaleSetting

    else:
        CurrentScaleSetting = SK.data.bones[bonename].inherit_scale
        SK.data.bones[bonename].inherit_scale = 'NONE' # disable scale inheritance temporarily

        Scale = Measure / Rule
        #It's better to adjust entire scale not just y
        bone.parent.scale = bone.parent.scale * Scale #* (1/bone.parent.parent.scale[1])
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.posemode_toggle()
        # SK.data.bones[bonename].inherit_scale = CurrentScaleSetting
        # if bonename == "L_Hand":
        #     print("Hand daaaaaaaaaaaa")




def ArmaturePosePoints(SK, refSK, Triade, SnapBones, SmartSnapBonesBrief, Fingers_Bases, Fingers_No_Bases):

    bpy.ops.object.mode_set(mode='POSE')

    # Numerator = 0
    # Denominator = 0




    RefSKDict = {Refbone.name: Refbone for Refbone in refSK.pose.bones}
    SKDict = {bone.name: bone for bone in SK.pose.bones}

     #Add something for the spine here
    if ("Spine2" in SKDict and "Spine2" in RefSKDict):
        BonePoseSnapperWithCheck(SK, refSK, "Spine2")
        # AplPose(SK)
        

    #TODO: Give people the option to Enable/Disable this
    NumOfElements = 0
    Diff_Sum = mathutils.Vector((0,0,0)) 
    for bonename in Triade:
        if (bonename in SKDict and bonename in RefSKDict):
            Ref_Local = refSK.pose.bones[bonename].head #- SK.pose.bones["Spine2"].head
            Point_Local =  SK.pose.bones[bonename].head #- SK.pose.bones["Spine2"].head

            Diff = Ref_Local - Point_Local
            # Local_Diff = SK.pose.bones[bonename].matrix.to_3x3().inverted() @ Diff
            Diff_Sum += Diff
            NumOfElements += 1
    
    Rise = Diff_Sum / NumOfElements
    Adj = SK.pose.bones["Spine2"].matrix.to_3x3().inverted() @ Rise
    print("Rise: ", Rise)

    Spine2Test = mathutils.geometry.distance_point_to_plane(Rise + SK.pose.bones["Spine1"].tail, SK.pose.bones["Spine1"].tail, SK.pose.bones["Spine1"].vector)

    if Spine2Test>=0:
        SK.pose.bones["Spine2"].location =  Adj
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.posemode_toggle()
        # AplPose(SK)

    else:
        pass




    # if Rise >= 0 and ("Spine2" in SKDict and "Spine2" in RefSKDict):
    #     SK.pose.bones["Spine2"].location[1] = SK.pose.bones["Spine2"].head.z  + Rise
    #     bpy.ops.object.posemode_toggle()
    #     bpy.ops.object.posemode_toggle()
    #     AplPose(SK)


#Commented for a bit

    for bonename in SnapBones:
        if (bonename in SKDict and bonename in RefSKDict):
            BonePoseSnapper(SK, refSK, bonename)
            # AplPose(SK)

   

    for bonename in SmartSnapBonesBrief:
        if (bonename in SKDict and bonename in RefSKDict):
            # print(bonename)
            BonePoseSnapperWithCheck(SK, refSK, bonename)
            # AplPose(SK)



    # for bonename in Left_Hand_Bones:
    #     if (bonename in SKDict and bonename in RefSKDict):
    #         # print(bonename)
    #         BonePoseSnapperWithCheck(SK, refSK, bonename)


    # for bonename in Right_Hand_Bones:
    #     if (bonename in SKDict and bonename in RefSKDict):
    #         # print(bonename)
    #         BonePoseSnapperWithCheck(SK, refSK, bonename)




    for bonename in Fingers_Bases:
        if (bonename in SKDict and bonename in RefSKDict):
            BonePoseSnapper(SK, refSK, bonename)
        

    for bonename in  Fingers_No_Bases:
        if (bonename in SKDict and bonename in RefSKDict):
            # print(bonename)
            BonePoseSnapperWithCheck(SK, refSK, bonename)             




    # if Denominator != 0:
    #     S = Numerator/Denominator
    # else:
    #     S = S0

    # print(S)

    # bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='OBJECT')



def ArmatureScaleAdjust(SK, refSK):

    bpy.ops.object.mode_set(mode='POSE')

    Numerator = 0
    Denominator = 0

    for bone in SK.pose.bones:

        for refbone in refSK.pose.bones:
            
            if refbone.name == bone.name:
                
                #Not a good idea to scale based on all bones. Moviing few bones might give perfect alignment
                Numerator += refbone.head.dot(bone.head)
                Denominator += (bone.head.dot(bone.head))

                if bone.name =="Spine1":
                    S0 = refbone.head.dot(bone.head) / (bone.head.dot(bone.head))

                    print("Scale",S0, bone.head, refbone.head)
                # bone.matrix = refbone.matrix
                # bpy.ops.object.posemode_toggle()
                # bpy.ops.object.posemode_toggle()

    if Denominator != 0:
        S = Numerator/Denominator
    else:
        S = S0

    # print(S)

    # bpy.ops.object.mode_set(mode='OBJECT')
    SK.scale = mathutils.Vector((S0,S0,S0))

    bpy.ops.object.mode_set(mode='OBJECT')


def Simple_Pose_Snapper(SK, refSK):

    bpy.ops.object.mode_set(mode='POSE')

    for bone in SK.pose.bones:

        for refbone in refSK.pose.bones:
            
            if refbone.name == bone.name:

                BonePoseSnapper(SK, refSK, bone.name)

    bpy.ops.object.mode_set(mode='OBJECT')
                



    #___________________Armature match fixer_____________
#TODO: Make it more robust. This feels really weak---Done
#TODO: Make sure that it knows how to deal BASE vs Base or HEAD vs Head ---> Done

# def Armature_QuickHeirarchyFix(SK, refSK):



#     bpy.ops.object.mode_set(mode='EDIT')

#     # RefSKDict = {Refbone.name: Refbone for Refbone in  refSK.data.edit_bones}
#     SKDict = {bone.name: bone for bone in  SK.data.edit_bones}
    

#     SK.data.edit_bones.new("BODY_SCALE__group")
#     SK.data.edit_bones["BODY_SCALE__group"].length = refSK.data.edit_bones["BODY_SCALE__group"].length
#     SK.data.edit_bones["BODY_SCALE__group"].matrix = refSK.data.edit_bones["BODY_SCALE__group"].matrix
#     SK.data.edit_bones["BODY_SCALE__group"].parent = SK.data.edit_bones["MODEL_00"]

#     if "Base" not in SKDict and "BASE" not in SKDict:
#         try:
#             refSK.data.edit_bones["BASE"]
            
#             Basename = "BASE"
#         except:
#             refSK.data.edit_bones["Base"]

#             Basename = "Base"
    
#         SK.data.edit_bones.new(Basename)



#         SK.data.edit_bones[Basename].length = refSK.data.edit_bones[Basename].length
#         SK.data.edit_bones[Basename].matrix = refSK.data.edit_bones[Basename].matrix
#         SK.data.edit_bones[Basename].parent =  SK.data.edit_bones["BODY_SCALE__group"]
        
#     SK.data.edit_bones["Hip"].parent = SK.data.edit_bones["BASE"]
#     SK.data.edit_bones["Spine1"].parent = SK.data.edit_bones["BASE"]


#     bpy.ops.object.mode_set(mode='OBJECT')


# def Armature_Edit_Matrix(SK,refSK):
#     bpy.ops.object.mode_set(mode='EDIT')

#     RefSKDict = {Refbone.name: Refbone for Refbone in  refSK.data.edit_bones}

#     for bone in SK.data.edit_bones:
#         if bone.name in RefSKDict:
#             bone.matrix = RefSKDict[bone.name].matrix
#             # print(bone.matrix)
# #            bpy.ops.object.editmode_toggle()
# #            bpy.ops.object.editmode_toggle()



#     bpy.ops.object.mode_set(mode='OBJECT')

def Armature_OverHall(SK,refSK):
# Not recommended cause when the SK sees main bones with no influence it will be put into Tpose?<---need to confirm this TODO

    bpy.ops.object.mode_set(mode='EDIT')

    SKDict = {bone.name: bone for bone in  SK.data.edit_bones}
    SKDictLower = {bone.name.lower(): bone for bone in  SK.data.edit_bones}
    # for bolne in SK.data.edit_bones:
    for refbone in refSK.data.edit_bones:
        if refbone.name in SKDict:
        # if bone.name.lower() == refbone.name.lower():
            
            pass
        # if bone.name in SKDict:
        #     pass
        # elif (case mismatch condition):
            
        elif refbone.name.lower() in SKDictLower:
            SK.data.edit_bones[SKDictLower[refbone.name.lower()].name].name = refbone.name #Rename the bone to match watch on the refSK
        else:
            SK.data.edit_bones.new(refbone.name)
        print(refbone.name)
#        bpy.ops.object.editmode_toggle()
#        bpy.ops.object.editmode_toggle()

        SK.data.edit_bones[refbone.name].length = refbone.length
        SK.data.edit_bones[refbone.name].matrix = refbone.matrix
        if refbone.name != "MODEL_00":
            SK.data.edit_bones[refbone.name].parent = SK.data.edit_bones[refbone.parent.name]

            # print(bone.matrix)
#            bpy.ops.object.editmode_toggle()
#            bpy.ops.object.editmode_toggle()

 #Complete   #TODO: Make sure the heirarchy has no multiple root bones---DONE
    for Mainbone in SK.data.edit_bones:
        if Mainbone.parent == None and Mainbone.name != 'MODEL_00':
            Mainbone.parent = SK.data.edit_bones['MODEL_00']


    bpy.ops.object.mode_set(mode='OBJECT')
