# Contains properties used for the _____ (TK_PT.py) and relies on the functions from _______ TK_FX.py.
# It also contains some functions used only with the properties (like update, etc)
#bl_idname should all be in lowercase for blender 2.8->3.1

#Devnote: assiging a value of a property using self[<property_name>] won't invoke the class's __setattr__ method unlike self.<property_name>

import bpy
import re
import os
import addon_utils
# from bpy.types import PropertyGroup
# from bpy.props import EnumProperty, PointerProperty, StringProperty, IntProperty

from.TK_FX import *





# def lol():
#     print("Update!!!!")

#____________________File related functions______________
def GetAddonsFolderName_propfx():
    Instances = []
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == "TK7_SK_CH":
            filepath = mod.__file__
            # print (filepath)
            Instances.append(filepath)
            # os.path.basename(filepath)
        else:
            pass

    if len(Instances) > 1:
        raise Exception("You have multiple instances of TK7_SK_CH installed. Please keep only one and try again")   
        
    start = '\\'
    end = '\\'  
    AddonFolder = filepath.split(start)[-2].split(end)[0]
    # print(AddonFolder)

    return AddonFolder



def FileExistenceTester(Folder,name):
#Works fine
    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder = GetAddonsFolderName_propfx()

    #Tests if a txt file with the name 'name' exists in the folder called "Folder"
    #Path = 'Rename_Presets/'+ name +'.txt'
    Path = Folder+'/'+ name +'.txt'
    GlobalPath = directory+'/'+AddonFolder+'/'+Path
    return os.path.exists(GlobalPath)

def Find_File_Names(FolderName, FileType):
    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder = GetAddonsFolderName_propfx()

    GlobalPath = directory+'/'+AddonFolder+'/'+FolderName
    # GlobalPath = AddonFolder+'/'+FolderName
    # print("Global path1:",GlobalPath)

    File_Names = []
    for root, dirs, files in os.walk(GlobalPath):
        for file in files:
            if file.endswith(FileType):
                # print(os.path.join(root, file))

                
                Path = os.path.join(root, file)
                start = '\\'
                end = '.'
                PresetName = Path.split(start)[-1].split(end)[0]

                File_Names.append(PresetName)
    return File_Names

def FileCreater(Folder,name):

    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder = GetAddonsFolderName_propfx()

    #Tests if a txt file with the name 'name' exists in the folder called "Folder"
    # Path = 'Rename_Presets/'+ name +'.txt'
    Path = Folder+'/'+ name +'.txt'
    GlobalPath = directory+'/'+AddonFolder+'/'+Path

    with open(GlobalPath,'w') as f:
        pass
    return 

def FileRenamer(Folder ,OldName, NewName):
#Works fine

    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path="addons")
    AddonFolder = GetAddonsFolderName_propfx()

    old_name = Folder+'/'+ OldName +'.txt'
    Global_old = directory+'/'+AddonFolder+'/'+old_name
    new_name = Folder+'/'+ NewName +'.txt'
    Global_new = directory+'/'+AddonFolder+'/'+new_name
    # Renaming the file
    os.rename(Global_old, Global_new)

def FileRemover(Folder ,FileName):
#Works fine
    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder = GetAddonsFolderName_propfx()

    Path = Folder+'/'+ FileName +'.txt'

    Global_old = directory+'/'+AddonFolder+'/'+Path
    # new_name = Folder+'/'+ NewName +'.txt'
    # Renaming the file
    os.remove(Global_old)

def Find_Missing_File_Name(FolderName,Preset_Name_Collection):

    print("Missing file function invoked")

    script_file = os.path.realpath(__file__)
    directory_ = os.path.dirname(script_file)

    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder = GetAddonsFolderName_propfx()

    GlobalPath = directory+'/'+AddonFolder+'/'+FolderName
    # GlobalPath = AddonFolder+'/'+FolderName

    # print("Global path 2:",GlobalPath)

    File_Names = []
    for root, dirs, files in os.walk(GlobalPath):
        for file in files:
            if file.endswith(".txt"):
                # print(os.path.join(root, file))

                
                Path = os.path.join(root, file)
                start = '\\'
                end = '.'
                PresetName = Path.split(start)[-1].split(end)[0]

                File_Names.append(PresetName)

                # bpy.context.scene.preset_collection.add()
                # bpy.context.scene.preset_collection[int(bpy.context.scene.preset_enum)].RenameListPreset = PresetName

    for FileName in File_Names:
        if FileName in Preset_Name_Collection:
            pass
        else:
            print(FileName, ".txt file needs to be renamed")
            return FileName
#_______________________________________________________


#______________For Main tools____________________________
def Generate_Enum_for_BoneMerger(self, context):
    
    
    Enum_items = ['parents', 'active']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        # Enum_items.append(item)
        Enums.append(item)
        
    return Enums
#________________________________________________________


#_______________For SK gen_______________________________

def Generate_Enum_for_SK_Gen_Opt2(self, context):
    
    
    Enum_items = ['All bones', 'Main bones only']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        # Enum_items.append(item)
        Enums.append(item)
        
    return Enums

def Generate_Enum_for_SK_Gen_Opt1(self, context):
    
    
    Enum_items = ['glTF', 'Psk']
    Enums = []
    
    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        # Enum_items.append(item)
        Enums.append(item)
        
    return Enums

def Generate_Enum_for_Chars(self, context):
    
    
    Enum_items = ['aki', 'ann', 'arb', 'asa', 'ask', 'bob', 'bry', 'bs7', 'crz', 'dek', 'dnc', 'dra', 'dvj', 'edd', 'elz', 'fen', 'frv', 'gan', 'hei', 'hwo', 'ita', 'ja4', 'jac', 'jin', 'jul', 'kaz', 'kin', 'knm', 'kum', 'kzm', 'lar', 'law', 'lee', 'lei', 'leo', 'lil', 'ltn', 'mar', 'mig', 'mrx', 'mut', 'nin', 'nsa', 'nsb', 'nsc', 'nsd', 'pan', 'pau', 'ste', 'xia', 'yhe', 'ykz', 'yos', 'zaf']
    Enums = []

    for indx, item in enumerate(Enum_items):
        
        data = str(item)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        # Enum_items.append(item)
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
        
        # Enum_items.append(item)
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

# def AddBoneRenameText(Path, Text):
#     #TODO: Search where the line is located first, and if it's not already there, the lines are the indices. If it's there, change only that particular line 
#     # Line = "'"+Current+"': '"+New+"'"
       
#     with open(Path,'w') as f:
#         more_lines = ['', 'Append text files', 'The End']

#         f.writelines('\n'.join(more_lines))
#     return 


def Generate_Enum_from_Rename_Preset_Collection(self, context):
    
    Enum_items = []
 
    for indx,test_number in enumerate(context.scene.preset_collection):
        
        data = str(test_number.RenameListPreset)
        Strindx = str(indx)
        item = (Strindx, data, '')
        
        Enum_items.append(item)
        
    return Enum_items


def InitializeBoneRenamerEnumerator():
    # print("lmao")
    # for root, dirs, files in os.walk("Skeletons"):
    PresetNames = Find_File_Names('Rename_Presets', ".txt")
    bpy.context.scene.preset_collection.clear()
    for file in PresetNames:
        
        Preset = bpy.context.scene.preset_collection.add()
        Preset.RenameListPreset = file


    # for root, dirs, files in os.walk("Rename_Presets"):
    #     for file in files:
    #         if file.endswith(".txt"):
    #             # print(os.path.join(root, file))

                
    #             Path = os.path.join(root, file)
    #             start = '\\'
    #             end = '.'
    #             PresetName = Path.split(start)[1].split(end)[0]

    #             bpy.context.scene.preset_collection.add()
    #             bpy.context.scene.preset_collection[int(bpy.context.scene.preset_enum)].RenameListPreset = PresetName

    #             print(PresetName)


                
                # with open(Path) as f:
                #     lines = f.readlines()
                #     for line in lines:
                #         ConvLine = LineInfoConverterForRenamerPresets(line)
                #         if len(ConvLine) == 2:
                #             print(ConvLine, len(ConvLine))
                    
#_____________________________________________________________


def SaveBoneRenameList(Path, collection):
    Lines = []
    for item in collection:
            CurrentName = item.Current_Name
            NewName = item.New_Name
            # print (CurrentName, NewName)
            Line = BoneRenameText(CurrentName, NewName)
            Lines.append(Line)
    
    with open(Path,'w') as f:
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
    # intersection = set(Files).intersection(PresetNames) 
    # if len(intersection)==len(Files) and len(intersection)==len(Files):
    if set(Files) == set(PresetNames):
        return True
    # else:
    #     return False

def BoneNameUpdateFunction(self, context):
    collection, indx = collection_from_element(self)
    # print("Preset name assigned to:",self.RenameListPreset)
    CurrentName = self.Current_Name
    NewName = self.New_Name
    # print (CurrentName, NewName)
    Line = BoneRenameText(CurrentName, NewName)
    Path = 'Rename_Presets/'+ context.scene.preset_collection[int(context.scene.preset_enum)].RenameListPreset +'.txt'
    
    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder = GetAddonsFolderName_propfx()
    # print("How are you")
    GlobalPath = directory+'/'+AddonFolder+'/'+Path
    
    # Path = 'Rename_Presets'+'/'+ context.RenameListPreset +'.txt'
    # print(Path)
    # print(Line)

    # WriteBoneRenameItemToTextFile(Path, bpy.context.scene.bone_rename_list_index, Line)
    # replace_line(Path, bpy.context.scene.bone_rename_list_index, Line)
    SaveBoneRenameList(GlobalPath, collection)
    # CollectionNames = []
    # MatchFlag = False
    # counter = 0
    # for n,element in enumerate(collection):
    #     CollectionNames.append(element.RenameListPreset)
    #     if self.RenameListPreset == element.RenameListPreset and n != indx:
    #         MatchFlag = True

    # while MatchFlag == True:
    #     if self.RenameListPreset in CollectionNames:
    #         MatchFlag = True
    #         # print("this is is where all the chiz happens")
    #         self["RenameListPreset"] = self.RenameListPreset + str(counter)
    #     else:
    #         MatchFlag = False                  
    #     counter += 1    

def RenamePresetMainFunction(self, context):
    collection, indx = collection_from_element(self)
    # print("Preset name assigned to:",self.RenameListPreset)
    CurrentPresetName = self.RenameListPreset
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
    
    
    # FileRenamer(Folder ,OldName, NewName)
    # if MatchFlag == True:
    #     print("Rename ",CurrentPresetName, "to ", NewPresetName )
    # print(FileExistenceTester('Rename_Presets',self.RenameListPreset))
    # return


def RenamePresetUpdatedFunction(self, context):
    #Should rename preset files too
    print("In update function")

    collection, indx = collection_from_element(self)
    FilePresent = FileExistenceTester('Rename_Presets',self.RenameListPreset)
    # print("Preset name assigned to:",self.RenameListPreset)
    CurrentPresetName = self.RenameListPreset
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
    for indx ,item in enumerate(bpy.context.scene.bone_rename_list):
            my_list = bpy.context.scene.bone_rename_list
            # bpy.context.scene.bone_rename_list_index = indx
            index = 0
            # print("Clear:" ,index, my_list, item.Current_Name)
            my_list.remove(index)


def InitializeRenameList(Defaul_List):

    ClearBoneRenameList()

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
        




    


# def FillNewPreset():
#     obj = bpy.context.active_object
#     Defaul_List = ['MODEL_00', 'BASE', 'Hip', 'Spine1', 'Spine2', 'Neck', 'Head', 'L_Shoulder', 'L_Arm', 'L_ForeArm', 'L_Hand', 'L_Thumb1', 'L_Thumb2', 'L_Thumb3', 'L_Index1', 'L_Index2', 'L_Index3', 'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'R_Shoulder', 'R_Arm', 'R_ForeArm', 'R_Hand', 'R_Thumb1', 'R_Thumb2', 'R_Thumb3', 'R_Index1', 'R_Index2', 'R_Index3', 'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Ring1', 'R_Ring2', 'R_Ring3', 'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'L_UpLeg', 'L_Leg', 'L_Foot', 'L_Toe', 'R_UpLeg', 'R_Leg', 'R_Foot', 'R_Toe' ]

#     if obj is not None:
#         if obj.type == 'ARMATURE':
#             try:
#                 BoneRenameList = AutoDetectBones()
#                 ClearBoneRenameList()
#                 for indx,bonename in enumerate(Defaul_List):
#                     bpy.context.scene.bone_rename_list.add()
#                     bpy.context.scene.bone_rename_list[indx].New_Name = bonename
#                     for element in BoneRenameList:
#                         if element[1]==bonename:
#                             bpy.context.scene.bone_rename_list[indx].Current_Name = element[0]
#                             # print(bonename,"--->",element[1])
#                             break
#                         else: 
#                             bpy.context.scene.bone_rename_list[indx].Current_Name = ''
                    

#             except:
#                 InitializeRenameList(Defaul_List)

#         else:
#             InitializeRenameList(Defaul_List)
#     else:
#         InitializeRenameList(Defaul_List)


def FillNewPreset():
    obj = bpy.context.active_object
    Defaul_List = ['MODEL_00', 'BASE', 'Hip', 'Spine1', 'Spine2', 'Neck', 'Head', 'L_Shoulder', 'L_Arm', 'L_ForeArm', 'L_Hand', 'L_Thumb1', 'L_Thumb2', 'L_Thumb3', 'L_Index1', 'L_Index2', 'L_Index3', 'L_Middle1', 'L_Middle2', 'L_Middle3', 'L_Ring1', 'L_Ring2', 'L_Ring3', 'L_Pinky1', 'L_Pinky2', 'L_Pinky3', 'R_Shoulder', 'R_Arm', 'R_ForeArm', 'R_Hand', 'R_Thumb1', 'R_Thumb2', 'R_Thumb3', 'R_Index1', 'R_Index2', 'R_Index3', 'R_Middle1', 'R_Middle2', 'R_Middle3', 'R_Ring1', 'R_Ring2', 'R_Ring3', 'R_Pinky1', 'R_Pinky2', 'R_Pinky3', 'L_UpLeg', 'L_Leg', 'L_Foot', 'L_Toe', 'R_UpLeg', 'R_Leg', 'R_Foot', 'R_Toe', 'SWG_OPT1_bustL__swing', 'SWG_OPT3_bustR__swing' ]
    
    InitializeRenameList(Defaul_List)


                

def BoneRenamerPresetSelection(self, context):
    # collection, indx = collection_from_element(self)
    print("Preset Selected:",context.scene.preset_enum , context.scene.preset_collection[int(context.scene.preset_enum)].RenameListPreset)
    Path = 'Rename_Presets/'+ context.scene.preset_collection[int(context.scene.preset_enum)].RenameListPreset +'.txt'
    print("Hi")
    directory = bpy.utils.user_resource('SCRIPTS',path= "addons")
    AddonFolder = GetAddonsFolderName_propfx()
    print("How are you")
    GlobalPath = directory+'/'+AddonFolder+'/'+Path
    
    # bpy.context.scene.bone_rename_list.clear()
    ClearBoneRenameList()
    print(GlobalPath)
    with open(GlobalPath,"r") as f:
        Counter = 0
        lines = f.readlines()
        for line in lines:
            ConvLine = LineInfoConverterForRenamerPresets(line)
            if len(ConvLine) == 2:
                context.scene.bone_rename_list.add()
                bpy.context.scene.bone_rename_list[Counter].Current_Name = ConvLine[0]
                bpy.context.scene.bone_rename_list[Counter].New_Name = ConvLine[1]
                Counter +=1 

                # print(ConvLine, len(ConvLine))
    # Call function to load preset by changing bone_rename_list
    
        
    return




# def GenerateBoneRenamerEnumerator():
#     # for root, dirs, files in os.walk("Skeletons"):
#     for root, dirs, files in os.walk("Rename_Presets"):
#         for file in files:
#             if file.endswith(".txt"):
#                 # print(os.path.join(root, file))

                
#                 Path = os.path.join(root, file)
#                 start = '\\'
#                 end = '.'
#                 PresetName = Path.split(start)[1].split(end)[0]
#                 print(PresetName)
#                 with open(Path) as f:
#                     lines = f.readlines()
#                     for line in lines:
#                         ConvLine = LineInfoConverterForRenamerPresets(line)
#                         if len(ConvLine) == 2:
#                             print(ConvLine, len(ConvLine))
                    



# GenerateBoneRenamerEnumerator()


#______________________For simplifier______________________
#TODO: for simplifier
def GetBoneSubstringList():
    #Generate substring list based on _______?
    BoneSubstrgList = []
    for Item in bpy.context.scene.bone_substrng_list:
        if Item.name not in BoneSubstrgList:
            BoneSubstrgList.append(Item.Substrng)
    return BoneSubstrgList

# #TODO: for simplifier
# def TemplateBoneSubstrngListGenerate(preset):
#     #clear current substring list
#     for indx,item in enumerate(bpy.context.scene.my_list):
#         bpy.context.scene.my_list.remove(indx)

#     #Generate new list based on the preset choice
#     if preset == "Default":
#         list = ["adj", "unused", "ctr", "roll" , "ROLL", "offset", "twist", "fix", "joint", "null"]
#         for ind,name in enumerate(list):
#             bpy.context.scene.my_list.add()
#             bpy.context.scene.my_list[ind].name = list[ind]

# #TODO: for SK gen
# def Generate_Enum_for_SK_Gen(self, context):
    
#     Enum_items = []
    
#     # for indx,test_number in enumerate(context.scene.preset_collection):
        
#     #     data = str(test_number.RenameListPreset)
#     #     Strindx = str(indx)
#     #     item = (Strindx, data, '')
        
#     #     Enum_items.append(item)
        
#     return Enum_items



#_________________________________________________________
