# Contains properties used for the _____ (TK_PT.py) and relies on the functions from _______ TK_PROP_FX.py.

#bl_idname should all be in lowercase for blender 2.8->3.1

import bpy
import re
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, PointerProperty, StringProperty, IntProperty

from.TK_PROP_FX import *
# from.TK_FX import *

# def lol():
#     print("Update!!!!")

# class ListItem(PropertyGroup):
#___________________Bone Renamer______________________

class BoneRenameListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    Current_Name: StringProperty(
           name="Current Name",
           description="The current name of the bone/vertex group",
           default="",#,
           update=BoneNameUpdateFunction)

    New_Name: StringProperty(
           name="New Name",
           description="The name you wish to rename your bone/vertex group to",
           default="",#)#,
           update=BoneNameUpdateFunction)

    # def __setattr__(self, name, value):
    #     print("Help me!!!")
    #     return


class Rename_Preset(PropertyGroup):
    # number: IntProperty()
    # print("Assign")
    RenameListPreset: StringProperty(
        name="Preset",
        description="",
        default="New",
        update=RenamePresetUpdatedFunction)#,#,
        # set = InitializeBoneRenamerEnumerator)
        # get=print("g"),
        # set=print("s"))
        # update = lol )
    



#attemp to make non conflicting preset names
    def __setattr__(self, name, value): 

#_____Name and file____ 
# Exists, Exists (Rename and Rename in updater)
# Exists, Doesn't (Rename first and generate new here)
# Doesn't, Exists (ERROR: SHOULD NOT EVER BE THE CASE. RESOLVE:?)
# Doesn't, Doesn't (SIMPLE: Keep, generate here)

        #invoked when I try to modify the collection
        print("New preset created")

        print("Only invoked when i create new enum element AND renamed an existing collection element")

        # if value == getattr(self, name):
        #     # check for assignement of current value
        #     return


        coll, indxx = collection_from_element(self)
        TrueColl = []
        self[name] = value #Necessary notation to avoid reinvoking __setattr__ 
        for whatever in coll:
            TrueColl.append(whatever.RenameListPreset)
        # print(coll[0].number)
        for ind, SampleName  in enumerate(TrueColl):
            if ind != indxx and SampleName == value:
                print(value, " already exists")
                RenamePresetMainFunction(self, bpy.context)
        # if value in TrueColl:
        #     # if value is not in the collection, just assign
        #     # self[name] = value

        
        #TODO: Check if preset txt file exists and if not generate it
        if FileExistenceTester('Rename_Presets',self.RenameListPreset) == False:
            FileCreater('Rename_Presets',self.RenameListPreset)
        # print(FileExistenceTester('Rename_Presets',self.RenameListPreset))
        return
        

#___________________Simplifier______________________

class BoneSubstrngListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    Substrng: StringProperty(
           name="Substring",
           description="The name, or part of the name, of the bone(s) to be merged to their parents",
           default="")#,
           #update=BoneNameUpdateFunction)


#________________Pose Isolator__________________________

# class SK_Hierarchy_Disabler(PropertyGroup):
#     """Group of properties representing an item in the list."""

#     ArmatureName: PointerProperty(
#            name="SK",
#            description='Select the skeleton that you want to isolate the bones of',
#            poll="",
#            update=BoneNameUpdateFunction)


class BoneParent(PropertyGroup):
    """Group of properties representing an item in the list."""

    Bone_Name: StringProperty(
           name="Bone name",
           description="The current name of the bone/vertex group",
           default="")

    Bone_Parent: StringProperty(
           name="Bone parent name",
           description="The name you wish to rename your bone/vertex group to",
           default="")#,#)#,
        #    update=BoneNameUpdateFunction)



# class Test_Number(PropertyGroup):
    
#     number: StringProperty(
#         name="Name",
#         description="A name for this item",
#         default="offset")


# class MyProperties(bpy.types.PropertyGroup):
    
#     my_enum : EnumProperty(
#         name= "Enumerator / Dropdown",
#         description= "sample text",
#         items= [('OP1', "Add Cube", ""),
#                 ('OP2', "Add Sphere", ""),
#                 ('OP3', "Add Suzanne", "")]
#     )
