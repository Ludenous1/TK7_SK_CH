# Contains the panel classes 

import bpy
from bpy.types import Panel

# from.TK_UI import *
from.TK_PROP_FX import *
#asd
#______________________________Panel Classes_____________________________________

class Tekke7Panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TK7_SK_CH"
    bl_options = {"DEFAULT_CLOSED"}

class Character_Modding(Tekke7Panel, Panel):
    bl_idname = "TEKKEN7_PT_CHARACTER"
    bl_label = "Character modding"

    def draw(self, context):
        layout = self.layout
#        layout.label(text="This is the main panel.")
        col = layout.column()

#        col.label(text='Import:')
        # c = col.column()
        r = col.row() # Start a row
        r1c1 = r.column(align=True) #start a column
        r1c1.operator("object.tk7_scene_setup", text='Scene setup', icon='PREFERENCES')
        r1c2 = r.column(align=True)
        r1c2.operator('object.tk7_export', text='FBX Export', icon='EXPORT')
        

        # row.label(text="", icon='ERROR')
        layout.separator()
        row = layout.row(align=True)
        row.label(text='Quick Tools:')

        row = layout.row(align=True)
        row.operator('object.sk_bonemerger', text='Merge bones to ', icon = 'GROUP_BONE')

        row.prop(context.scene, "Bone_Mrg_enum", text="")

        # layout.separator()

        row = layout.row(align=True)
        row.operator('object.sk_applypose', text='Apply Pose', icon = 'ARMATURE_DATA')
        row.separator()
        row.operator('object.sk_bonefix', text='Fix bones', icon = 'MODIFIER_OFF')


        


        # r = col.row(align=True)
        # r2 = r.column(align=True)
        
        # r2.operator('object.sk_bnremove', text='Remove bones')

        # r = col.row(align=True)
        # r2 = r.column(align=True)
        # r2.operator('object.sk_bonerename', text='Rename')


        # r = col.row(align=True)
        # r2 = r.column(align=True)
        # r2.operator('object.sk_bonemergeparent', text='MergeParent')

        # r = col.row(align=True)
        # r2 = r.column(align=True)
        # r2.operator('object.sk_posmove', text='PosMove')



#Not really used / deprecated
class SK_TOOLS_PT_PANEL(Tekke7Panel, Panel):
    bl_idname = "TEKKEN7_PT_SK_TOOLS"
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Skeleton Tools"
    

    def draw(self, context):
        layout = self.layout


        row = layout.row(align=True)
        row.label(text='Quick Tools:')
        row.label(text="", icon='ERROR')

        row = layout.row(align=True)
        row.operator('object.tk7_sk_generator', text='Merge bones to ', icon = 'OUTLINER_OB_ARMATURE')

        row.prop(context.scene, "sk_gen_char_enum", text="")

        row = layout.row(align=True)
        row.operator('object.sk_bonefix', text='Fix bones to match ', icon = 'OUTLINER_OB_ARMATURE')

        row.prop(context.scene, "sk_gen_char_enum", text="")

        row = layout.row(align=True)
        row.operator('object.sk_applypose', text='Apply Pose', icon = 'ARMATURE_DATA')


#         row = layout.row(align=True)
#         row.label(text='Skeleton Generator:')

#         row = layout.row(align=True)
#         row.prop(context.scene, "sk_gen_char_enum", text="Mode")
#         row.prop(context.scene, "sk_gen_opt1_enum", text="")
#         row.prop(context.scene, "sk_gen_opt2_enum", text="")

#         row = layout.row(align=True)
#         row.operator('object.tk7_sk_generator', text='Generate Skeleton', icon = 'OUTLINER_OB_ARMATURE')

#         layout.separator()
#         layout.separator()

#         row = layout.row(align=True)
#         row.label(text='T-Poser:')
#         row = layout.row(align=True)
#         row.prop(context.scene, 'bone_R_Mrg', text='Fix armature')
#         #TODO: Add the active thing here
#         row = layout.row(align=True)
#         row.prop(context.scene, 'bone_R_Mrg', text='Fix finger tips')
#         row = layout.row(align=True)
#         row.operator('object.tk7_sk_generator', text='T Pose', icon = 'OUTLINER_OB_ARMATURE')

#         layout.separator()
#         layout.separator()

#         row = layout.row(align=True)
#         row.label(text='Pose snapper:')
#         row = layout.row(align=True)
#         row.prop(context.scene, 'bone_R_Mrg', text='Autoscale')

#         row = layout.row(align=True)
#         row.prop(context.scene, "sk_gen_char_enum", text="Mode")

#         row = layout.row(align=True)
#         row.operator('object.tk7_sk_generator', text='Snap bones', icon = 'OUTLINER_OB_ARMATURE')

#         layout.separator()
#         layout.separator()


# #        layout.label(text="Second Sub Panel of Panel 1.")
#         # col = layout.column()
#         # col.separator()
#         # row.separator()


#         # row.label(text='Select the armatures:')
 
#         row = layout.row(align=True)
#         row.label(text='Other Tools:')

#         row = layout.row(align=True)
#         row.operator('object.tk7_sk_generator', text='Merge bones to ', icon = 'OUTLINER_OB_ARMATURE')

#         row.prop(context.scene, "sk_gen_char_enum", text="")

#         row = layout.row(align=True)
#         row.operator('object.sk_applypose', text='Apply Pose', icon = 'ARMATURE_DATA')


#         # c = col.column(align=True)
#         # r = c.row(align=True)
#         # r.operator('object.sk_applypose', text='Apply Pose', icon = 'ARMATURE_DATA')

#         # col.separator()

#         # c = col.column(align=True)
#         # r = c.row(align=True)
#         # r.operator('object.sk_bonemergeparent', text='Merge Selected bones to ', icon = 'ARMATURE_DATA')



class SK_GEN_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Skeleton Generator"
    

    def draw(self, context):
        layout = self.layout
        # row = layout.row(align=True)
        # row.label(text='Skeleton Generator:')

        row = layout.row(align=True)
        row.prop(context.scene, "sk_gen_char_enum", text="Mode")
        row.prop(context.scene, "sk_gen_opt1_enum", text="")
        row.prop(context.scene, "sk_gen_opt2_enum", text="")

        row = layout.row(align=True)
        row.operator('object.tk7_sk_generator', text='Generate Skeleton', icon = 'OUTLINER_OB_ARMATURE')


class SK_TPOSER_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "T-Poser"
    

    def draw(self, context):
        layout = self.layout

        # row = layout.row(align=True)
        # row.label(text='T-Poser:')
        row = layout.row(align=True)
        row.prop(context.scene, 'tp_fix_armature', text='Fix armature')
        #TODO: Add the active thing here

        
        sub = row.row(align=True)
        sub.active = context.scene.tp_fix_armature
        # sub.prop(arm, "axes_position", text="Position")

        # row.active == context.scene.tp_fix_armature
        sub.prop(context.scene, 'tp_fix_fingertips', text='Fix finger tips')
        row = layout.row(align=True)
        row.prop(context.scene, "tp_tpose_spine", text="Apply to spine bones")
        row = layout.row(align=True)
        row.operator('object.sk_tposer', text='T Pose', icon = 'ARMATURE_DATA')


class SK_POSE_SNAP_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Pose Snapper"
    

    def draw(self, context):
        layout = self.layout

        # row = layout.row(align=True)
        # row.label(text='Pose snapper:')
        row = layout.row(align=True)
        row.prop(context.scene, 'ps_autoscale', text='Autoscale')

        row = layout.row(align=True)
        row.prop(context.scene, "ps_mode_enum", text="Mode")

        row = layout.row(align=True)
        row.operator('object.sk_pose_snapper', text='Snap bones', icon = 'OUTLINER_OB_ARMATURE')

        # layout.separator()
        # layout.separator()


#        layout.label(text="Second Sub Panel of Panel 1.")
        # col = layout.column()
        # col.separator()
        # row.separator()


        # row.label(text='Select the armatures:')
 


        # c = col.column(align=True)
        # r = c.row(align=True)
        # r.operator('object.sk_applypose', text='Apply Pose', icon = 'ARMATURE_DATA')

        # col.separator()

        # c = col.column(align=True)
        # r = c.row(align=True)
        # r.operator('object.sk_bonemergeparent', text='Merge Selected bones to ', icon = 'ARMATURE_DATA')



class RENAMER_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Bone Renamer"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)

        # PresetNames = Find_File_Names('Rename_Presets', ".txt")
        # if len(PresetNames) == len(context.scene.preset_collection)

        PresetNames = Find_File_Names('Rename_Presets', ".txt")
        if len(context.scene.preset_collection)>0:
            row.prop(context.scene, "preset_enum", text="Preset")

        if CheckPresetNameMatch():
            row.operator("bone_renamer_preset.add", text="", icon="ADD")
            row.operator("bone_renamer_preset.remove", text="", icon="REMOVE")
        else:
            row.operator("bone_renamer_preset.load", text="Load", icon="FILE_TICK")
        
        # elif len(PresetNames)>len(context.scene.preset_collection):
        #     row.operator("bone_renamer_preset.load", text="Load")
        
        # row.operator("bone_renamer_preset.add", text="", icon="ADD")
        # row.operator("bone_renamer_preset.remove", text="", icon="REMOVE")
        row = layout.row()

        if context.scene.preset_enum != '' and CheckPresetNameMatch():
            item = context.scene.preset_collection[int(context.scene.preset_enum)]
            row.prop(item, "RenameListPreset", text="")




        ####____________Default template list__________
        scene = context.scene
        obj = context.active_object



        row = layout.row()
        row.template_list("MY_UL_BoneRenameList", "The_List", scene,
                          "bone_rename_list", scene, "bone_rename_list_index")

        # row = layout.row()
        col = row.column(align=True)
        if CheckPresetNameMatch():
            col.operator('bone_rename_list.new_item', text='', icon="ADD")
            col.operator('bone_rename_list.delete_item', text='', icon="REMOVE")
        # row.operator('my_list.move_item', text='UP').direction = 'UP'
        # row.operator('my_list.move_item', text='DOWN').direction = 'DOWN'

        col.separator()
        #Insert autopopulate here
        col.operator('bone_rename_list.populate', text='', icon="SYSTEM")

        if scene.bone_rename_list_index >= 0 and scene.bone_rename_list:
            item = scene.bone_rename_list[scene.bone_rename_list_index]

            row = layout.row()
            if obj is not None and obj.type == 'ARMATURE' and obj in bpy.context.selected_objects:
                row.prop_search(item, "Current_Name", bpy.context.active_object.data, "bones")
            else:
                row.prop(item, "Current_Name")

            row.prop(item, "New_Name")
            row = layout.row()
            

        if len(scene.bone_rename_list)>0:
            row = layout.row(align=True)
            row.prop(context.scene, 'bone_R_Mrg', text='Merge bones with same/similar new names')
            row = layout.row(align=True)
            row.operator('object.sk_bonerename', text='Rename', icon = 'COLOR_RED')
        ####____________________________________________



        # ob = context.object
        # bone = context.bone
        # arm = context.armature
        # pchan = None

        # if ob and bone:
        #     pchan = ob.pose.bones[bone.name]
        # elif bone is None:
        #     bone = context.edit_bone

        # col = layout.column()
        # col.use_property_split = False
        # col.prop(bone, "layers", text="")
        # col.use_property_split = True
        # col = layout.column()

        # col.separator()

        # if context.bone:
        #     col.prop(bone, "parent")
        # else:
        #     col.prop_search(bone, "parent", arm, "edit_bones")





        
#No longer used
class SKTOOLS_PT_PANEL(Tekke7Panel, Panel):
    bl_idname = "SK_PT_SKELETON"
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Skeleton"

    # @classmethod
    # def poll(cls, context):
    #     obj = context.active_object

    #     if obj is not None and obj in bpy.context.selected_objects:
    #         if obj.type == 'ARMATURE':
    #             # if obj.mode == 'OBJECT':
    #             return True


    def draw(self, context):
        layout = self.layout
#        layout.label(text="Second Sub Panel of Panel 1.")



        col = layout.column()

 
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('object.sk_applypose', text='Apply Pose', icon = 'ARMATURE_DATA')

        col.separator()

        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('object.sk_bonemergeparent', text='Merge Selected bones to ', icon = 'ARMATURE_DATA')


        # c = col.column(align=True)
        # r = c.row(align=True)
        # r.operator('object.sk_tposer', text='T Poser')

        # c = col.column(align=True)
        # r = c.row(align=True)
        # r.operator('object.sk_bonefix', text='Align Bones')
       
       
#        col = layout.column()
#        c = col.column(align=True)
#        r = c.row(align=True)

class SIMPLIFIER_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Skeleton Simplifier"

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene

        row = layout.row(align=True)
        row.label(text='Merge bones containing the following to their parents:')

        row = layout.row()
        row.template_list("MY_UL_BoneSubstringList", "The_other_List", scene,
                          "bone_substrng_list", scene, "bone_substrng_list_index")

        row = layout.row()
        row.operator('bone_substrng_list.new_item', text='NEW')
        row.operator('bone_substrng_list.delete_item', text='REMOVE')
        # row.operator('my_list.move_item', text='UP').direction = 'UP'
        # row.operator('my_list.move_item', text='DOWN').direction = 'DOWN'

        if scene.bone_substrng_list_index >= 0 and scene.bone_substrng_list:
            item = scene.bone_substrng_list[scene.bone_substrng_list_index]

            row = layout.row()
            row.prop(item, "Substrng")
            # row.prop(item, "New_Name")

        row = layout.row()
        row.prop(context.scene, 'bone_prsv', text='keep bone orientation')
        row = layout.row()
        row.prop(context.scene, 'bone_remv', text='remove bones')
        row = layout.row()
        row.prop(context.scene, 'mesh_join', text='join meshes')
        row = layout.row()
        row.prop(context.scene, 'clr_trnspc', text='Change alpha blend to HASHED')



        col = layout.column()
        r = col.row(align=True)
        r2 = r.column(align=True)
        r2.operator('object.sk_simplify', text='Simplify', icon = 'MOD_ARMATURE')
        

class MESHTOOLS_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Mesh"


    @classmethod
    def poll(cls, context):
        obj = context.active_object

        if obj is not None:
            if obj.type == 'MESH':
                if obj.mode == 'OBJECT':
                    return True

    def draw(self, context):
        layout = self.layout
#        layout.label(text="First Sub Panel of Panel 1.")
        
        
        col = layout.column()     
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('object.sk_test', text='Mixamo port')
         

class VIEWPORT_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Viewport"

    def draw(self, context):
        layout = self.layout
#        layout.label(text="First Sub Panel of Panel 1.")
        col = layout.column()
        
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('xps_tools.bones_dictionary_generate', text='Facial bone fix')


class PORTER_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Porters"

    def draw(self, context):
        layout = self.layout
#        layout.label(text="First Sub Panel of Panel 1.")


#        col = layout.column()
#        
#        c = col.column(align=True)
#        r = c.row(align=True)
#        r.operator('xps_tools.bones_dictionary_generate', text='Facial bone fix')
#  


class CUSTOM_PT_PANEL(Tekke7Panel, Panel):
    bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = "Custom"

    def draw(self, context):
        layout = self.layout
#        layout.label(text="First Sub Panel of Panel 1.")


#        col = layout.column()
#        
#        c = col.column(align=True)
#        r = c.row(align=True)
#        r.operator('xps_tools.bones_dictionary_generate', text='Facial bone fix')
#  






#____________________Operators_____________________________________



# class TekkenCharacterSceneSetup(bpy.types.Operator):
#     """Clears out all objects and adjusts the scene settings for character meshes"""
#     bl_idname = "object.tk_scene_setup"
#     bl_label = "Scene setup"


#     def execute(self, context):
#         TekkenSceneSetup(context)
#         return {'FINISHED'}
   
    
# class TekkenCharacterExport(bpy.types.Operator):
#     """Applies the correct export settings for character meshes"""
#     bl_idname = "object.tk7_export"
#     bl_label = "Character Export"


#     def execute(self, context):
#         TekkenFBXexporter(context)
#         return {'FINISHED'}



# class ArmatureViewportAdjust(bpy.types.Operator):
#     """Moves auxiliary bones to other layers and enlarges primary bones without affecting how the mesh loads inside Tekken"""
#     bl_idname = "object.tk7_armature_viewport_fix"
#     bl_label = "Viewport adjust"


#     def execute(self, context):
#         ArmatureViewportFix(context)
#         return {'FINISHED'}



#____________________Class registration_____________________________


# classes = (
#     Character_Modding,
#     SKTOOLS_PT_PANEL,
#     MESHTOOLS_PT_PANEL, 
#     VIEWPORT_PT_PANEL,
#     PORTER_PT_PANEL,
#     CUSTOM_PT_PANEL,
#     TekkenCharacterSceneSetup,
#     TekkenCharacterExport,
#     ArmatureViewportAdjust
# )

# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)

# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
#     register()