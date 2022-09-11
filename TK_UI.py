#Contains UI related items that aren't panels such as lists, windows, etc...

import bpy
from bpy.types import Panel, Operator, PropertyGroup , UIList
from bpy.props import EnumProperty, PointerProperty, StringProperty

from.TK_FX import *

#____________________Bone Renamer_________________________

class MY_UL_BoneRenameList(UIList):
    """Demo UIList."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        bone_icon = 'BONE_DATA'

        custom_icon = 'RIGHTARROW_THIN'

        layout = layout.split(factor=0.5, align=True)

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.Current_Name, icon = bone_icon)
            layout.label(text=item.New_Name, icon = custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

    # def filter_items(self, context, data , property):
    #     pass

#____________________Simplifier_________________________

class MY_UL_BoneSubstringList(UIList):
    """Demo UIList."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        bone_icon = 'BONE_DATA'

        # custom_icon = 'RIGHTARROW_THIN'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.Substrng, icon = bone_icon)
            # layout.label(text=item.New_Name, icon = custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = bone_icon)

# def test_items2(self, context):
    
#     Enum_items = ['fen', 'aki', 'ann', 'arb', 'asa', 'ask', 'bob', 'bry', 'bs7', 'crz', 'dek', 'dnc', 'dra', 'dvj', 'edd', 'elz', 'frv', 'gan', 'hei', 'hwo', 'ita', 'ja4', 'jac', 'jac', 'jin', 'jul', 'kaz', 'kin', 'knm', 'kum', 'kzm', 'lar', 'law', 'lee', 'lei', 'leo', 'lil', 'ltn', 'mar', 'mig', 'mrx', 'mut', 'nin', 'nsa', 'nsb', 'nsc', 'nsd', 'pan', 'pau', 'ste', 'xia', 'yhe', 'ykz', 'yos', 'zaf']
    
#     for test_number in enumerate(context.scene.test_collection):
        
#         data = str(test_number.number)
#         item = (data, data, data)
        
#         Enum_items.append(item)
        
#     return Enum_items




# # class MyProperties(bpy.types.PropertyGroup):
    
# #     my_enum : EnumProperty(
# #         name= "Enumerator / Dropdown",
# #         description= "sample text",
# #         items= [('OP1', "Add Cube", ""),
# #                 ('OP2', "Add Sphere", ""),
# #                 ('OP3', "Add Suzanne", "")
# #         ]
# #     )


# class WM_OT_simplifier(bpy.types.Operator):
#     """Simplifies the skeleton"""
#     bl_label = "Simplifier"
#     bl_idname = "wm.simplifier"
    
#     # text = bpy.props.StringProperty(name= "Enter Name", default= "")
#     # scale = bpy.props.FloatVectorProperty(name= "Scale:", default= (1,1,1))
    
#     # prop1: bpy.props.EnumProperty()#name = "Merge bones with names containing: ", deafault = [])
#     # prop2: bpy.props.BoolProperty()
#     prop3: bpy.props.BoolProperty(default = True)
#     prop4: bpy.props.BoolProperty(default = True)
#     prop5: bpy.props.BoolProperty(default = True)



#     my_enum : bpy.props.EnumProperty(
#         name= "Enumerator / Dropdown",
#         description= "sample text",
#         items= [('OP1', "Add Cube", ""),
#                 ('OP2', "Add Sphere", ""),
#                 ('OP3', "Add Suzanne", "")
#         ]
#     )

    
#     def execute(self, context):
        
#         # t = self.text
#         # s = self.scale
#         # print(self.prop3, self.prop4, self.prop5)
#         Simplifier(PrsvBones = self.prop5, BoneSubstrgList = ["adj", "unused", "ctr", "roll", "offset", "twist", "fix", "joint", "null"], Removebones = self.prop3, MergeMeshes = self.prop4)

#         # bpy.ops.mesh.primitive_cube_add()
#         # obj = bpy.context.object
#         # obj.name = t
        
#         # obj.scale[0] = s[0] 
#         # obj.scale[1] = s[1] 
#         # obj.scale[2] = s[2] 
        
        
#         return {'FINISHED'}
    
#     def invoke(self, context, event):
        
#         return context.window_manager.invoke_props_dialog(self)

#     def draw(self, context):

#         layout = self.layout

#         ob = context.object
#         group = ob.vertex_groups.active
#         layout.label(text = "Are you crazy?")
#         rows = 3
#         if group:
#             rows = 5

#         row = layout.row()
#         # row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows)
#         row.template_list("MATERIAL_UL_matslots_example", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows)

#         col = row.column(align=True)

#         col.operator("object.vertex_group_add", icon='ADD', text="")
#         props = col.operator("object.vertex_group_remove", icon='REMOVE', text="")
#         # props.all_unlocked = props.all = False

#         col.separator()

#         col.operator("object.vertex_group_remove", icon='FILE_REFRESH', text="")

#         # if group:
#         #     col.separator()
#         #     col.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
#         #     col.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

#         # if (
#         #         ob.vertex_groups and
#         #         (ob.mode == 'EDIT' or
#         #          (ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex))
#         # ):
#         #     row = layout.row()

#         #     sub = row.row(align=True)
#         #     sub.operator("object.vertex_group_assign", text="Assign")
#         #     sub.operator("object.vertex_group_remove_from", text="Remove")

#         #     sub = row.row(align=True)
#         #     sub.operator("object.vertex_group_select", text="Select")
#         #     sub.operator("object.vertex_group_deselect", text="Deselect")

#         #     layout.prop(context.tool_settings, "vertex_group_weight", text="Weight")



        



#         row = self.layout
#         # row.label(text="Do you really want to do that?")
#         # row.prop(self, "prop1", text="Bones to merge?")
#         # row.prop(self, "prop2", text="Preserve bone orientation")
#         row.prop(self, "prop3", text="Remove bones")
#         row.prop(self, "prop4", text="Merge meshes")
#         row.prop(self, "prop5", text="Preserve bone orientation")
        




# #         layout = self.layout
# # #        layout.label(text="This is the main panel.")
# #         col = layout.column()

# # #        col.label(text='Import:')
# #         # c = col.column()
# #         r = col.row(align=True) # Start a row
# #         r1c1 = r.column(align=True) #start a column
# #         r1c1.operator("object.tk_scene_setup", text='Scene setup', icon='NONE')
# #         r1c2 = r.column(align=True)
# #         r1c2.operator('object.tk7_export', text='FBX Export')
        
# #         r = col.row(align=True)
# #         r2 = r.column(align=True)
# #         r2.operator('object.tk7_test', text='Test')



# class MATERIAL_UL_matslots_example(bpy.types.UIList):
#     # The draw_item function is called for each item of the collection that is visible in the list.
#     #   data is the RNA object containing the collection,
#     #   item is the current drawn item of the collection,
#     #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
#     #   have custom icons ID, which are not available as enum items).
#     #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
#     #   active item of the collection).
#     #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
#     #   index is index of the current item in the collection.
#     #   flt_flag is the result of the filtering process for this item.
#     #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
#     #         need them.


#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
#         ob = data
#         slot = item
#         ma = slot.material
#         # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             # You should always start your row layout by a label (icon + text), or a non-embossed text field,
#             # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
#             # We use icon_value of label, as our given icon is an integer value, not an enum ID.
#             # Note "data" names should never be translated!
#             if ma:
#                 layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
#             else:
#                 layout.label(text="", translate=False, icon_value=icon)
#         # 'GRID' layout type should be as compact as possible (typically a single icon!).
#         elif self.layout_type in {'GRID'}:
#             layout.alignment = 'CENTER'
#             layout.label(text="", icon_value=icon)



#     # def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
#     #     # Just in case, we do not use it here!
#     #     self.use_filter_invert = False

#     #     # assert(isinstance(item, bpy.types.VertexGroup)
#     #     vgroup = item
#     #     if self.layout_type in {'DEFAULT', 'COMPACT'}:
#     #         # Here we use one feature of new filtering feature: it can pass data to draw_item, through flt_flag
#     #         # parameter, which contains exactly what filter_items set in its filter list for this item!
#     #         # In this case, we show empty groups grayed out.
#     #         if flt_flag & self.VGROUP_EMPTY:
#     #             col = layout.column()
#     #             col.enabled = False
#     #             col.alignment = 'LEFT'
#     #             col.prop(vgroup, "name", text="", emboss=False, icon_value=icon)
#     #         else:
#     #             layout.prop(vgroup, "name", text="", emboss=False, icon_value=icon)
#     #         icon = 'LOCKED' if vgroup.lock_weight else 'UNLOCKED'
#     #         layout.prop(vgroup, "lock_weight", text="", icon=icon, emboss=False)
#     #     elif self.layout_type in {'GRID'}:
#     #         layout.alignment = 'CENTER'
#     #         if flt_flag & self.VGROUP_EMPTY:
#     #             layout.enabled = False
#     #         layout.label(text="", icon_value=icon)






# # import bpy


# # class MyProperties(bpy.types.PropertyGroup):
    
# #     my_enum : EnumProperty(
# #         name= "Enumerator / Dropdown",
# #         description= "sample text",
# #         items= [('OP1', "Add Cube", ""),
# #                 ('OP2', "Add Sphere", ""),
# #                 ('OP3', "Add Suzanne", "")
# #         ]
# #     )

# # class ADDONNAME_PT_main_panel(Panel):
# #     bl_label = "Main Panel"
# #     bl_idname = "ADDONNAME_PT_main_panel"
# #     bl_space_type = 'VIEW_3D'
# #     bl_region_type = 'UI'
# #     bl_category = "New Tab"

# #     def draw(self, context):
# #         layout = self.layout
# #         scene = context.scene
# #         mytool = scene.my_tool
        
        
# #         layout.prop(mytool, "my_enum")
# #         layout.operator("addonname.myop_operator")


# # class ADDONNAME_OT_my_op(Operator):
# #     bl_label = "Add Object"
# #     bl_idname = "addonname.myop_operator"
    
# #     def execute(self, context):
# #         scene = context.scene
# #         mytool = scene.my_tool
        
# #         return {'FINISHED'}
    

# # classes = [MyProperties, ADDONNAME_PT_main_panel, ADDONNAME_OT_my_op]
  
# # def register():
# #     for cls in classes:
# #         bpy.utils.register_class(cls)
        
# #     bpy.types.Scene.my_tool = PointerProperty(type= MyProperties)
 
# # def unregister():
# #     for cls in classes:
# #         bpy.utils.unregister_class(cls)
# #     del bpy.types.Scene.my_tool
 
 
 
# # if __name__ == "__main__":
# #     register()











#___________________________Simple popup______________________________

# import bpy

# class SimplePopUpOperator(bpy.types.Operator):
#     """Really?"""
#     bl_idname = "my_category.custom_popup_dialog"
#     bl_label = "Do you really want to do that?"
#     bl_options = {'REGISTER', 'INTERNAL'}

#     prop1: bpy.props.BoolProperty()
#     prop2: bpy.props.BoolProperty()

#     @classmethod
#     def poll(cls, context):
#         return True

#     def execute(self, context):
#         self.report({'INFO'}, "YES!")
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         return context.window_manager.invoke_popup(self)

#     def draw(self, context):
#         row = self.layout
#         row.label(text="Do you really want to do that?")
#         row.prop(self, "prop1", text="Property A")
#         row.prop(self, "prop2", text="Property B")


# class OBJECT_PT_CustomPanel(bpy.types.Panel):
#     bl_label = "My Panel"
#     bl_idname = "OBJECT_PT_custom_panel"
#     bl_space_type = "VIEW_3D"   
#     bl_region_type = "UI"
#     bl_category = "Tools"
#     bl_context = "objectmode"

#     def draw(self, context):
#         layout = self.layout
#         layout.operator(SimplePopUpOperator.bl_idname)

# def register():
#     bpy.utils.register_class(OBJECT_PT_CustomPanel)
#     bpy.utils.register_class(SimplePopUpOperator)

# def unregister():
#     bpy.utils.unregister_class(SimplePropConfirmOperator)
#     bpy.utils.unregister_class(SimplePopUpOperator)

# if __name__ == "__main__":
#     register()






#_____________________________Simple Message box_______________________________

# def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

#     def draw(self, context):
#         self.layout.label(text=message)

#     bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


# #Shows a message box with a specific message 
# ShowMessageBox("This is a message") 

# #Shows a message box with a message and custom title
# ShowMessageBox("This is a message", "This is a custom title")

# #Shows a message box with a message, custom title, and a specific icon
# ShowMessageBox("This is a message", "This is a custom title", 'ERROR')







