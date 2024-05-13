# Contains the panel classes 

import bpy
from bpy.types import Panel

# from.TK_UI import *
from.TK_PROP_FX import *
from . import addon_updater_ops
# from .__init__ import bl_info

#asd
#______________________________Panel Classes_____________________________________

class Tekke7Panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TK7_SK_CH"
    # bl_options = {"DEFAULT_CLOSED"}
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    
class Character_Modding(Tekke7Panel,Panel):
    bl_idname = "TEKKEN7_PT_CHARACTER"
    bl_label = ""
    # bl_options = {"DEFAULT_CLOSED"}

    # bl_space_type = "VIEW_3D"
    # bl_region_type = "UI"
    # bl_category = "TK7_SK_CH"
    # bl_options = {"DEFAULT_CLOSED"}
    def draw_header(self, context):
        
        layout = self.layout

        # self.layout.label(text="Skeleton Generator")
        layout.prop(context.scene, "tk_main_menu", text="Lol",expand = True)

    def draw(self, context):

        # layout = self.layout
        # layout.label(bl_info["version"])
        addon_updater_ops.update_settings_ui(self, context)

        

class EXP_SCENE_PT_PANEL(Tekke7Panel, Panel):
    # bl_idname = "TEKKEN7_PT_SK_TOOLS"
    bl_label = ""

    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '0' or context.scene.tk_main_menu  == '1':


            return True
    

        return False


    def draw_header(self, context):
        
        layout = self.layout

        self.layout.label(text="Scene and export settings")

        # self.layout.label(text=" ")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#quick-tools'


    def draw(self, context):
        layout = self.layout

#        layout.label(text="This is the main panel.")
        col = layout.column()

#        col.label(text='Import:')
        # c = col.column()
        r = col.row() # Start a row
        
        r1c1 = r.column(align=True) #start a column
        r1c1.operator("object.tk7_scene_setup", text='Scene setup', icon='PREFERENCES')
   
        r.separator()

        r2 = col.row() # Start a row
        r2.label(text='Export settings:') 

        layout.separator()

        r3 = col.row() # Start a row
        # r2.label(text='Export by:')     
        r3.prop(context.scene, "fbx_exp_enum", text="Name by ", expand = True)

        r4 = col.row() # Start a row
        # r2.label(text='Export by:') 
        # if len(context.scene.tk_main_menu ) == '1':    
        r4.prop(context.scene, "tk_import_type", text="Import type ", expand = True)


        r5 = col.row() # Start a row
        r5.prop(context.scene.fbx_exp_path, "user_file_path", text="Output Folder ")
        # r2c2.use_property_split = True

        r6 = col.row() # Start a row
        r6.operator('object.tk7_export', text='FBX Export', icon='EXPORT')

       



class PT_SK_TOOLS(Tekke7Panel, Panel):
    # bl_idname = "TEKKEN7_PT_SK_TOOLS"
    bl_label = ""

    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '2': #or context.scene.tk_main_menu  == '1':


            return True
    

        return False


    def draw_header(self, context):
        
        layout = self.layout

        self.layout.label(text="Skeleton Tools")

        # self.layout.label(text=" ")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#quick-tools'


    def draw(self, context):
        layout = self.layout
        

        row = layout.row(align=True)
        row.operator('object.sk_bonemerger', text='Merge bones to ', icon = 'GROUP_BONE')

        row.prop(context.scene, "bone_mrg_enum", text="")

        # layout.separator()

        row = layout.row(align=True)
        row.operator('object.sk_applypose', text='Apply Pose', icon = 'ARMATURE_DATA')
        row.separator()
        row.operator('object.sk_bonefix', text='Fix bones', icon = 'MODIFIER_OFF')


        if context.scene.bone_isolation_switch == False:
            Dsblr_State = 'Off'
        else:
            Dsblr_State = 'On'

        Dsblr_condition = False
        if context.active_object != None:
            if context.active_object.type == 'ARMATURE':
                if (not context.scene.bone_isolation_switch and context.scene.sk_to_isolate == None) or (context.scene.bone_isolation_switch and context.active_object == context.scene.sk_to_isolate):
                    Dsblr_condition = True

        row = layout.row(align=True)
        row.enabled = Dsblr_condition
        row.prop(context.scene, "bone_isolation_switch" ,text = 'Disable hierarchy: '+Dsblr_State, toggle=True)
        sub = row.row(align=True)
        sub.enabled = False
        sub.prop(context.scene, "sk_to_isolate" , icon='ARMATURE_DATA')




class SK_GEN_PT_PANEL(Tekke7Panel, Panel):
    # bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = ""
    # bl_options = {"HEADER_LAYOUT_EXPAND"}


    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '0':


            return True
    

        return False

    def draw_header(self, context):
        
        layout = self.layout

        self.layout.label(text="Skeleton Generator")

        # self.layout.label(text=" ")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#skeleton-generator'

        

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
    # bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = ""

    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '0':


            return True
    

        return False

    
    def draw_header(self, context):
        
        layout = self.layout

        self.layout.label(text="Tposer")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#t_poser'

    def draw(self, context):
        layout = self.layout

        # row = layout.row(align=True)
        # row.label(text='T-Poser:')
        # row = layout.row(align=True)
        # row.prop(context.scene, 'tp_fix_armature', text='Fix armature')
        # #TODO: Add the active thing here

        row = layout.row(align=True)
        row.prop(context.scene, 'tp_connect_bones', text='connect main bones')
 
        
        # sub = row.row(align=True)
        # # sub.active = context.scene.tp_fix_armature
        # sub.enabled = context.scene.tp_fix_armature
        # sub.prop(arm, "axes_position", text="Position")

        # row.active == context.scene.tp_fix_armature
        row = layout.row(align=True)
        row.prop(context.scene, 'tp_fix_fingertips', text='Fix finger tips')
        row = layout.row(align=True)
        row.prop(context.scene, "tp_tpose_spine", text="Apply to spine bones")
        row = layout.row(align=True)
        row.operator('object.sk_tposer', text='T Pose', icon = 'ARMATURE_DATA')


class SK_POSE_SNAP_PT_PANEL(Tekke7Panel, Panel):
    # bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = ""
    
    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '0':


            return True
    

        return False


    def draw_header(self, context):
        
        layout = self.layout

        self.layout.label(text="Pose Snapper")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#pose-snapper'

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
    # bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = ""
    # bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '2':


            return True
    

        return False


    def draw_header(self, context):
        
        layout = self.layout
        
        self.layout.label(text="Bone Renamer")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#bone_renamer'

        # layout.direction = 'VERTICAL'
       

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
            row.separator()

            row.operator("bone_renamer_preset.remove", text="", icon="TRASH")
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
        Arm_Objs = [ob.type for ob in context.selected_objects if ob.type=='ARMATURE']

        for Selected_obj in bpy.context.selected_objects:
            if Selected_obj  != obj  and Selected_obj.type == 'ARMATURE':
                refSK = Selected_obj

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

        col.separator()
        #Insert autopopulate here
        col.operator('bone_rename_list.duplicate', text='', icon="DUPLICATE")

        if scene.bone_rename_list_index >= 0 and scene.bone_rename_list:
            item = scene.bone_rename_list[scene.bone_rename_list_index]

            row = layout.row()
            if obj is not None and obj.type == 'ARMATURE' and obj in bpy.context.selected_objects:
                row.prop_search(item, "Current_Name", bpy.context.active_object.data, "bones")

            else:
                row.prop(item, "Current_Name")
            
            #row.operator('object.br_current_selector', text='', icon = 'RESTRICT_SELECT_OFF')

            if obj is not None and obj.type == 'ARMATURE' and obj in bpy.context.selected_objects and len(Arm_Objs)==2:
                row.prop_search(item, "New_Name", refSK.data, "bones")
            else:
                row.prop(item, "New_Name")
            #row.operator('object.br_new_selector', text='', icon = 'RESTRICT_SELECT_OFF')

            row = layout.row()
            

        if len(scene.bone_rename_list)>0:
            row = layout.row(align=True)
            row.prop(context.scene, 'bone_r_mrg', text='Merge bones with same / similar new names')
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
    # bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = ""

    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '2':


            return True
    

        return False

    def draw_header(self, context):
        
        layout = self.layout

        self.layout.label(text="Skeleton Simplifier")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#skeleton-simplifier'

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene

        row = layout.row(align=True)
        row.label(text='Keywords: (ex: "offset", "null",...)')

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
        row.prop(context.scene, 'bone_simp_connect', text='connect main bones')
        row = layout.row()
        row.prop(context.scene, 'bone_remv', text='remove bones')
        row = layout.row()
        row.prop(context.scene, 'mesh_join', text='join meshes')
        row = layout.row()
        row.prop(context.scene, 'clr_trnspc', text='XPS')

        col = layout.column()
        r = col.row(align=True)
        r2 = r.column(align=True)
        r2.operator('object.sk_simplify', text='Simplify', icon = 'MOD_ARMATURE')
        

class VGMERGER_PT_PANEL(Tekke7Panel, Panel):
    # bl_parent_id = "TEKKEN7_PT_CHARACTER"
    bl_label = ""

    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '2':


            return True
    

        return False

    # @classmethod
    # def poll(cls, context):
    #     obj = context.active_object

    #     if obj is not None:
    #         if obj.type == 'MESH':
    #             if obj.mode == 'OBJECT':
    #                 return True

    def draw_header(self, context):
        
        layout = self.layout

        self.layout.label(text="Vertex Group Merger")

        op = layout.operator(
            'wm.url_open',
            text='',
            icon='QUESTION'
            )
        op.url = 'https://github.com/Ludenous1/TK7_SK_CH#vertex-group-merger'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        Target = scene.vg_list_target
#        layout.label(text="First Sub Panel of Panel 1.")


            
        col = layout.column()     
        c = col.column(align=True)
        row = c.row(align=True)
    

        row = layout.row()
        row.template_list("MY_UL_VG_List", "The_other_List", scene,
                          "vg_list", scene, "vg_list_index")
        
        col = row.column(align=True)
        col.operator('vg_list.new_item', text='', icon="ADD")
        col.operator('vg_list.delete_item', text='', icon="REMOVE")
        
        # if obj is not None and obj.type == 'MESH' and obj in bpy.context.selected_objects:
        #     row.prop_search(Target, "Target", bpy.context.active_object, "vertex_groups", text="Target VG")
        # else:
        row.prop(Target,"Target",text="New Name")
        
        row = layout.row()

        if scene.vg_list_index >= 0 and scene.vg_list:
            item = scene.vg_list[scene.vg_list_index]
            # 

            row = layout.row()
            if obj is not None and obj.type == 'MESH' and obj in bpy.context.selected_objects:
                row.prop_search(item, "VG", bpy.context.active_object, "vertex_groups")
            else:
                row.prop(item, "VG")

            row = layout.row()
            row.prop(context.scene, 'vg_remove', text='Remove merged vertex groups')
            
            
            # if obj is not None and obj.type == 'MESH' and obj in bpy.context.selected_objects:
            #     row.prop_search(target, "Target", bpy.context.active_object, "vertex_groups")
            # else:
            #     row.prop(target, "Target")

            # row = layout.row()
        
        col = layout.column()     
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('object.vg_merge', text='Merge Vertex Groups')
         

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