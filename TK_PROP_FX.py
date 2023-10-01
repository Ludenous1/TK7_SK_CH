#This file contains functions associated with the custom blender properties (like update, etc) defined in TK_PROP.py. 
#It relies on the functions from TK_FX.py.


#Devnote_1: assiging a value of a property using self[<property_name>] won't invoke the class's __setattr__ method unlike self.<property_name>
#Devnote_2: bl_idname should all be in lowercase for blender 2.8 and above with no spaces.


import bpy
import re
import os
import addon_utils

import time

# from bpy.types import PropertyGroup
# from bpy.props import EnumProperty, PointerProperty, StringProperty, IntProperty

from.TK_FX import *



#____________________File related functions______________
def GetAddonsFolderName_propfx():
    addon_folder = None
    
    for mod in addon_utils.modules():
        if mod.bl_info.get('name') == "TK7_SK_CH":
            addon_folder = os.path.dirname(mod.__file__)
            break
    
    if addon_folder is None:
        raise Exception("The TK7_SK_CH addon is not installed.")
    
    if len(addon_folder.split(os.sep)) > 1:
        addon_folder = os.path.basename(os.path.normpath(addon_folder))
    
    return addon_folder

def GetAddonsFolderPath_propfx():
    addon_folder_path = None
    
    for mod in addon_utils.modules():
        if mod.bl_info.get('name') == "TK7_SK_CH":
            addon_folder_path = os.path.dirname(mod.__file__)
            break
    
    if addon_folder_path is None:
        raise Exception("The TK7_SK_CH addon is not installed.")
    
    return addon_folder_path



def FileExistenceTester(Folder,name):

    AddonFolder_Path = GetAddonsFolderPath_propfx()

    #Tests if a txt file with the name 'name' exists in the folder called "Folder"

    File_Path = os.path.join(AddonFolder_Path, Folder, name +'.txt')

    return os.path.exists(File_Path)

def Find_File_Names(FolderName, FileType):

    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder_Path = GetAddonsFolderPath_propfx()

    FolderPath = os.path.join(AddonFolder_Path, FolderName)


    File_Names = []
    for root, dirs, files in os.walk(FolderPath):
        for file in files:
            if file.endswith(FileType):

                PresetName = os.path.splitext(file)[0]


                File_Names.append(PresetName)
    return File_Names

def FileCreater(Folder,name):

    AddonFolder_Path = GetAddonsFolderPath_propfx()



    File_Path = os.path.join(AddonFolder_Path ,Folder, name +'.txt')

    with open(File_Path,'w') as f:
        pass
    return 

def FileRenamer(Folder ,OldName, NewName):

    AddonFolder_Path = GetAddonsFolderPath_propfx()

    File_Path_old = os.path.join(AddonFolder_Path,Folder, OldName +'.txt')

    File_Path_new = os.path.join(AddonFolder_Path,Folder, NewName +'.txt')
    # Renaming the file
    os.rename(File_Path_old, File_Path_new)

def FileRemover(Folder ,FileName):

    AddonFolder_Path = GetAddonsFolderPath_propfx()

    File_Path = os.path.join(AddonFolder_Path,Folder, FileName +'.txt')

    os.remove(File_Path)

def Find_Missing_File_Name(FolderName,Preset_Name_Collection):

    print("Missing file function invoked")

    AddonFolder_Path = GetAddonsFolderPath_propfx()

    Folder_Path = os.path.join(AddonFolder_Path,FolderName)

    File_Names = []
    for root, dirs, files in os.walk(Folder_Path):
        for file in files:
            if file.endswith(".txt"):
                PresetName = os.path.splitext(file)[0]
                File_Names.append(PresetName)


    for FileName in File_Names:
        if FileName in Preset_Name_Collection:
            pass
        else:
            print(FileName, ".txt file needs to be renamed")
            return FileName
#_______________________________________________________


#______________For Main tools____________________________
def Generate_Enum_for_FBX_Exporter(self, context):
    
    
    Enum_items = ['Mesh', 'Armature']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enums.append(item)
        
    return Enums


def Generate_Enum_for_BoneMerger(self, context):
    
    
    Enum_items = ['parents', 'active']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enums.append(item)
        
    return Enums


def SK_hierarchy_disabler_poll(self, object):
    return object.type == 'ARMATURE'


def check_ob_in_scene(scene):
    ob = scene.sk_to_isolate

    if ob is not None:
        if ob.name not in scene.objects:
            scene.sk_to_isolate = None
            scene.bone_isolation_switch = False
            scene.bone_parent_list.clear()

def Store_SK_hierarchy_data(SK):

    bpy.ops.object.mode_set(mode='OBJECT')

    for indx,bone in enumerate(SK.data.bones):
        bpy.context.scene.bone_parent_list.add()
        bpy.context.scene.bone_parent_list[indx].Bone_Name = bone.name
        if bone.parent != None:
            bpy.context.scene.bone_parent_list[indx].Bone_Parent = bone.parent.name
        else:
            bpy.context.scene.bone_parent_list[indx].Bone_Parent = ''

    bpy.ops.object.mode_set(mode='OBJECT')

def Disable_SK_hierarchy_data(SK):

    bpy.ops.object.mode_set(mode='EDIT')

    for bone in SK.data.edit_bones:
        bone.parent = None

    bpy.ops.object.mode_set(mode='OBJECT')

def Update_SK_hierarchy_data(SK):
    
    SKDict = {bone.name: bone for bone in  SK.data.edit_bones}

    for indx1,item1 in enumerate(bpy.context.scene.bone_parent_list):
        if item1.Bone_Name not in SKDict:
            for indx2,item2 in enumerate(bpy.context.scene.bone_parent_list):
                if item2.Bone_Parent == item1.Bone_Name:
                    item2.Bone_Parent = item1.Bone_Parent

            item1.Bone_Name = ''

def Restore_SK_hierarchy_data(SK):

    bpy.ops.object.mode_set(mode='EDIT')

    Update_SK_hierarchy_data(SK)

    for item in bpy.context.scene.bone_parent_list:
        if item.Bone_Name != '':
            if item.Bone_Parent == '':
                Parent = None
            else:
                Parent = SK.data.edit_bones[item.Bone_Parent]

            SK.data.edit_bones[item.Bone_Name].parent = Parent


    bpy.ops.object.mode_set(mode='OBJECT')


def SK_hierarchy_disabler_Switch_update(self, context):
    
    OgMode = context.mode
    
    if context.scene.bone_isolation_switch == True:
        self.sk_to_isolate = bpy.context.active_object
        Store_SK_hierarchy_data(self.sk_to_isolate)
        Disable_SK_hierarchy_data(self.sk_to_isolate)
        # SK_copy = bpy.context.active_object.data.copy()

    elif context.scene.bone_isolation_switch == False:
        #Return the Sk to normal before changing it to None and clearing its copied data
        if self.sk_to_isolate != None:
            Restore_SK_hierarchy_data(self.sk_to_isolate)
            bpy.context.scene.bone_parent_list.clear()
            # print(SK_copy)
            self.sk_to_isolate = None

    print(context.scene.bone_isolation_switch,self.sk_to_isolate)
    # pass

    if bpy.context.active_object == None:
        pass
    
    else:
        if 'EDIT' in OgMode:
            bpy.ops.object.mode_set(mode='EDIT')
        elif 'OBJECT' in OgMode:
            bpy.ops.object.mode_set(mode='OBJECT')
        elif 'POSE' in OgMode:
            bpy.ops.object.mode_set(mode='POSE')




#________________________________________________________


#_______________For SK gen_______________________________

def Generate_Enum_for_SK_Gen_Opt2(self, context):
    
    
    Enum_items = ['All bones', 'Main bones only']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enums.append(item)
        
    return Enums

def Generate_Enum_for_SK_Gen_Opt1(self, context):
    
    
    Enum_items = ['glTF', 'Psk']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enums.append(item)
        
    return Enums

def Generate_Enum_for_Chars(self, context):
    
    
    Enum_items = ['aki', 'ann', 'arb', 'asa', 'ask', 'bob', 'bry', 'bs7', 'crz', 'dek', 'dnc', 'dra', 'dvj', 'edd', 'elz', 'fen', 'frv', 'gan', 'hei', 'hwo', 'ita', 'ja4', 'jac', 'jin', 'jul', 'kaz', 'kin', 'knm', 'kum', 'kzm', 'lar', 'law', 'lee', 'lei', 'leo', 'lil', 'ltn', 'mar', 'mig', 'mrx', 'mry', 'mrz', 'mut', 'nin', 'nsa', 'nsb', 'nsc', 'nsd', 'pan', 'pau', 'ste', 'xia', 'yhe', 'ykz', 'yos', 'zaf']
    Enums = []

    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enums.append(item)
        
    return Enums

#___________________For Pose Snapper____________________________

def Generate_Enum_for_ps_mode(self, context):
    
    
    Enum_items = ['Simple', 'Advanced (Experimental)']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enums.append(item)
        
    return Enums

#_______________________________________________

#___________________For Renamer____________________________
def collection_from_element(self):
    # this gets the collection that the element is in
    path = self.path_from_id()
    match = re.match('(.*)\[\d*\]', path)
    parent = self.id_data
    start = '['
    end = ']'
    index = int((path.split(start))[1].split(end)[0])
    try:
        coll_path = match.group(1)
    except AttributeError:
        raise TypeError("Propery not element in a collection.") 
    else:
        return parent.path_resolve(coll_path) , index
 


def Generate_Enum_from_Rename_Preset_Collection(self, context):
    
    Enum_items = []
 
    for indx,test_number in enumerate(context.scene.preset_collection):
        
        data = str(test_number.RenameListPreset)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enum_items.append(item)
        
    return Enum_items


def InitializeBoneRenamerEnumerator():

    PresetNames = Find_File_Names('Rename_Presets', ".txt")
    bpy.context.scene.preset_collection.clear()



    for file in PresetNames:
        
        Preset = bpy.context.scene.preset_collection.add()
        Preset.RenameListPreset = file

    if len(PresetNames)!=0:
        bpy.context.scene.preset_enum = '0'


                    
#_____________________________________________________________


def SaveBoneRenameList(Path, collection):

    Lines = []
    for item in collection:
            CurrentName = item.Current_Name
            NewName = item.New_Name
            Line = BoneRenameText(CurrentName, NewName)
            Lines.append(Line)
    
    with open(Path,'w') as f:
    # with open(GlobalPath,'w') as f:
        for line in Lines:
            f.write(line) 
            f.write('\n')  

def BoneRenameText(Current, New):
    #TODO: Search where the line is located first, and if it's not already there, the lines are the indices. If it's there, change only that particular line 
    Line = "'"+Current+"': '"+New+"'"
    return Line
        

def CheckPresetNameMatch():
    Files = Find_File_Names('Rename_Presets', ".txt")
    PresetNames = []
    for preset in bpy.context.scene.preset_collection:
        PresetNames.append(preset.RenameListPreset)

    if set(Files) == set(PresetNames):
        return True


def BoneNameUpdateFunction(self, context):
    collection, indx = collection_from_element(self)

    AddonFolder_Path = GetAddonsFolderPath_propfx()


    File_Path = os.path.join(AddonFolder_Path,'Rename_Presets', context.scene.preset_collection[int(context.scene.preset_enum)].RenameListPreset +'.txt')

    
    SaveBoneRenameList(File_Path, collection)


def RenamePresetMainFunction(self, context):
    collection, indx = collection_from_element(self)


    CollectionNames = []
    MatchFlag = False
    counter = 0
    for n,element in enumerate(collection):
        CollectionNames.append(element.RenameListPreset)
        if self.RenameListPreset == element.RenameListPreset and n != indx:
            MatchFlag = True

    while MatchFlag == True:
        if self.RenameListPreset in CollectionNames:
            MatchFlag = True
            # print("this is is where all the chiz happens")
            self["RenameListPreset"] = self.RenameListPreset + str(counter)
        else:
            MatchFlag = False                  
        counter += 1    
    


def RenamePresetUpdatedFunction(self, context):
    #Should rename preset files too
    print("In update function")

    collection, indx = collection_from_element(self)
    FilePresent = FileExistenceTester('Rename_Presets',self.RenameListPreset)

    CollectionNames = []
    MatchFlag = False
    counter = 0
    for n,element in enumerate(collection):
        CollectionNames.append(element.RenameListPreset)
        if self.RenameListPreset == element.RenameListPreset and n != indx:
            MatchFlag = True

    while MatchFlag == True:
        if self.RenameListPreset in CollectionNames:
            MatchFlag = True
            # print("this is is where all the chiz happens")
            self["RenameListPreset"] = self.RenameListPreset + str(counter)
        else:
            MatchFlag = False                  
        counter += 1    
    
    #TODO: Rename preset txt file if it exists
    NewPresetName = self.RenameListPreset
    
    # FileRenamer(Folder ,OldName, NewName)
    # if MatchFlag == True:
    OldName = Find_Missing_File_Name('Rename_Presets', CollectionNames)
    if OldName!=None: #and OldName!=NewPresetName:
        print("Rename ",OldName, "to ", NewPresetName )
        FileRenamer('Rename_Presets' ,OldName, NewPresetName)
        # print(FileExistenceTester('Rename_Presets',self.RenameListPreset))
    return


def LineInfoConverterForRenamerPresets(line):
#Function that cleans up the bone string data into a more blender friendly format 
    Elements = line.split('\'')
    Elements2 = line.split('\"') 
    if "\'" in line and len(Elements)==5:
        
        CurrentName = Elements[1]
        NewName = Elements[3]

        ConvertedLine = [CurrentName, NewName]

    
    elif "\"" in line and len(Elements2)==5:
        
        CurrentName = Elements2[1]
        NewName = Elements2[3]

        ConvertedLine = [CurrentName, NewName]
    else:
        ConvertedLine = []

    return ConvertedLine

def ClearBoneRenameList():
    my_list = bpy.context.scene.bone_rename_list
    # for indx ,item in enumerate(bpy.context.scene.bone_rename_list):
    #         my_list = bpy.context.scene.bone_rename_list
    #         # bpy.context.scene.bone_rename_list_index = indx
    #         index = 0
    #         # print("Clear:" ,index, my_list, item.Current_Name)
    #         my_list.remove(index)

    my_list.clear()


def InitializeRenameList(Defaul_List):


    ClearBoneRenameList()

    # bpy.context.scene.bone_rename_list.append(len(Defaul_List))

    for indx,bonename in enumerate(Defaul_List):
        bpy.context.scene.bone_rename_list.add()
        bpy.context.scene.bone_rename_list[indx].Current_Name = ''
        bpy.context.scene.bone_rename_list[indx].New_Name = bonename



def RenamerListPopulate():

    Default_List = ['MODEL_00', 'BASE', 'Hip', 'Spine1', 'Spine2', 'Neck', 'Head', 'L_Shoulder', 'L_Arm', 'L_ForeArm', 'L_Hand', 'L_Thumb1', 'L_Thumb2', 'L_Thumb3', 'L_Index1', 'L_Index2', 'L_Index3', 'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'R_Shoulder', 'R_Arm', 'R_ForeArm', 'R_Hand', 'R_Thumb1', 'R_Thumb2', 'R_Thumb3', 'R_Index1', 'R_Index2', 'R_Index3', 'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Ring1', 'R_Ring2', 'R_Ring3', 'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'L_UpLeg', 'L_Leg', 'L_Foot', 'L_Toe', 'R_UpLeg', 'R_Leg', 'R_Foot', 'R_Toe', 'SWG_OPT1_bustL__swing', 'SWG_OPT3_bustR__swing']
    Gen_list = []
    ClearBoneRenameList()

    RenameList = RenamerListPopulateFx()

    for indx,bonename in enumerate(RenameList):

        bpy.context.scene.bone_rename_list.add()
        bpy.context.scene.bone_rename_list[indx].Current_Name = bonename[0]
        bpy.context.scene.bone_rename_list[indx].New_Name = bonename[1]
        Gen_list.append(bonename[1])


    Unused_List = list(set(Default_List) - set(Gen_list))

    #Add any missing bones as empty lines
    for indx2, item in enumerate(Unused_List):
        bpy.context.scene.bone_rename_list.add()

        bpy.context.scene.bone_rename_list[-1].Current_Name = ''
        bpy.context.scene.bone_rename_list[-1].New_Name = item
        



def FillNewPreset():
    obj = bpy.context.active_object
    Defaul_List = ['MODEL_00', 'BASE', 'Hip', 'Spine1', 'Spine2', 'Neck', 'Head', 'L_Shoulder', 'L_Arm', 'L_ForeArm', 'L_Hand', 'L_FingerBase', 'L_Thumb1', 'L_Thumb2', 'L_Thumb3',  'L_Index1', 'L_Index2', 'L_Index3', 'L_Middle', 'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Ring', 'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Pinky', 'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'R_Shoulder', 'R_Arm', 'R_ForeArm', 'R_Hand', 'R_FingerBase', 'R_Thumb1', 'R_Thumb2', 'R_Thumb3', 'R_Index1', 'R_Index2', 'R_Index3', 'R_Middle', 'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Ring', 'R_Ring1', 'R_Ring2', 'R_Ring3','R_Pinky', 'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'L_UpLeg', 'L_Leg', 'L_Foot', 'L_Toe', 'R_UpLeg', 'R_Leg', 'R_Foot', 'R_Toe', 'SWG_OPT1_bustL__swing', 'SWG_OPT3_bustR__swing' ]
    
    InitializeRenameList(Defaul_List)


                

def BoneRenamerPresetSelection(self, context):
    startTime = time.time() 
    
    print("Start", time.time() - startTime)

    

    AddonFolder_Path = GetAddonsFolderPath_propfx()
    File_Path = os.path.join(AddonFolder_Path,'Rename_Presets', context.scene.preset_collection[int(context.scene.preset_enum)].RenameListPreset +'.txt')
   

    ClearBoneRenameList()

    print("After clearing the list", time.time() - startTime )

    with open(File_Path,"r") as f:
        Counter = 0
        lines = f.readlines()
        for line in lines:
            ConvLine = LineInfoConverterForRenamerPresets(line)
            if len(ConvLine) == 2:
                context.scene.bone_rename_list.add()

                print("Adding more lines to rename list...", time.time() - startTime )
                bpy.context.scene.bone_rename_list[Counter].Current_Name = ConvLine[0]
                bpy.context.scene.bone_rename_list[Counter].New_Name = ConvLine[1]
                Counter +=1 

    print("Done", time.time() - startTime )

        
    return



#______________________For simplifier______________________
#TODO: for simplifier
def GetBoneSubstringList():
    #Generate substring list based on _______?
    BoneSubstrgList = []
    for Item in bpy.context.scene.bone_substrng_list:
        if Item.name not in BoneSubstrgList:
            BoneSubstrgList.append(Item.Substrng)

    print(BoneSubstrgList, "Just to check")
    return BoneSubstrgList



#______________________For Vertex Group Merger______________________
#TODO: for simplifier
def GetVertexGroupList():
    
    VertexGroupList = []
    for Item in bpy.context.scene.vg_list:
        if Item.name not in VertexGroupList:
            VertexGroupList.append(Item.VG)

    print(VertexGroupList, "Just to check")
    return VertexGroupList