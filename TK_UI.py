#Contains UI related items that aren't panels such as lists, windows, etc...

import bpy
from bpy.types import Panel, Operator, PropertyGroup , UIList, AddonPreferences
from bpy.props import EnumProperty, PointerProperty, StringProperty, IntProperty, BoolProperty

from.TK_FX import *

from . import addon_updater_ops

#____________________Bone Renamer_________________________

class MY_UL_BoneRenameList(UIList):
    """List for the Bone Renamer."""

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
    """List for the Skeleton Generator."""

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


#____________________Addon updater_________________________
# UI aspects for the addon updater were added to the init file instead

#____________________Vertex Group Merger_________________________

class MY_UL_VG_List(UIList):
    """List for the vertex group merger."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        vg_icon = 'GROUP_VERTEX'

        # custom_icon = 'RIGHTARROW_THIN'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.VG, icon = vg_icon)
            # layout.label(text=item.New_Name, icon = custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = vg_icon)



