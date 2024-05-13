# VisualUV
# Copyright (C) 2023 Samuel Bílek

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.



import bpy

import os
import uuid
import gpu

from bpy.props import BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, PointerProperty, IntProperty

from bpy.types import Operator
from mathutils import Vector
from mathutils.geometry import area_tri, normal
from bpy_extras import mesh_utils
from gpu_extras.batch import batch_for_shader


#_________________Panels__________________________
# import bpy

class VisualUVPanel():
    def draw_ui(self, layout, context, is_uv):
        if not context.selected_objects:
            layout.label(text='No object selected')
            return
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                layout.label(text='Some selected objects are not MESH objects')
                return
            if not obj.data.uv_layers.active:
                layout.label(text='Some selected objects do not have an active UV layer')
                return
        obj = context.selected_objects[0]
        visualuv = obj.visualuv
        operation_box = None

        #Hide texture button

        # toggle_text = 'Hide Texture' if visualuv.checker_texture else 'Show Texture'
        # toggle_icon = 'TEXTURE' if visualuv.checker_texture else 'MESH_PLANE'

        # texture_box = layout.box()
        # texture_container = texture_box.row()
        # texture_container.operator('visualuv.toggle_texture', text=toggle_text, icon=toggle_icon)
        # texture_container.scale_y = 1.5

        # layout.separator(factor=0.1)

        # toggle_text = 'Enable Stretching' if visualuv.operation != 'UV_STRETCHING' else 'Disable Stretching'
        # toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_STRETCHING' else 'HIDE_ON'

        # enable_box = layout.box()
        # enable_container = enable_box.row()
        # enable_container.operator('visualuv.toggle_stretching', text=toggle_text, icon=toggle_icon)
        # enable_container.scale_y = 1.5
        # if visualuv.operation == 'UV_STRETCHING':
        #     operation_box = enable_box

        # layout.separator(factor=0.1)

        # UV normals button

        # toggle_text = 'Enable UV Normals' if visualuv.operation != 'UV_NORMALS' else 'Disable UV Normals'
        # toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_NORMALS' else 'HIDE_ON'

        # enable_box = layout.box()
        # enable_container = enable_box.row()
        # enable_container.operator('visualuv.toggle_normals', text=toggle_text, icon=toggle_icon)
        # enable_container.scale_y = 1.5
        # if visualuv.operation == 'UV_NORMALS':
        #     operation_box = enable_box

        # layout.separator(factor=0.1)

        # UV overlapping button

        # if obj.mode == 'EDIT' and not bpy.context.tool_settings.use_uv_select_sync:
        #     toggle_text = 'Enable UV Overlapping' if visualuv.operation != 'UV_OVERLAP' else 'Disable UV Overlapping'
        #     toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_OVERLAP' else 'HIDE_ON'

        #     enable_box = layout.box()
        #     enable_container = enable_box.row()
        #     enable_container.operator('visualuv.toggle_overlap', text=toggle_text, icon=toggle_icon)
        #     enable_container.scale_y = 1.5
        #     if visualuv.operation == 'UV_OVERLAP':
        #         operation_box = enable_box

        #     layout.separator(factor=0.1)

        # UV island coloring button
        toggle_text = 'Enable Island Coloring' if visualuv.operation != 'UV_ISLANDS' else 'Disable Island Coloring'
        toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_ISLANDS' else 'HIDE_ON'

        enable_box = layout.box()
        enable_container = enable_box.row()
        enable_container.operator('visualuv.toggle_islands', text=toggle_text, icon=toggle_icon)
        enable_container.scale_y = 1.5
        if visualuv.operation == 'UV_ISLANDS':
            operation_box = enable_box

        layout.separator(factor=0.1)

        if visualuv.operation == 'NONE' and not visualuv.checker_texture:
            return

        # texture controls
        # if visualuv.checker_texture:
        #     subbox = texture_box.box()
        #     subbox.template_ID(visualuv, 'image', open='image.open', new='image.new')
        #     subbox.prop(visualuv, 'texture_scale', text='Texture Scale', slider=True)
        #     if is_uv:
        #         subbox.prop(visualuv, 'texture_alpha', text='Texture Alpha', slider=True)
        #         subbox.prop(visualuv, 'fill_texture', text='Texture Fill')
        
        # current operation controls
        
        # if operation_box:
        #     if visualuv.operation == 'UV_STRETCHING':
        #         subbox = operation_box.box()
        #         subbox.prop(visualuv, 'max_division', text='Stretch Factor', slider=True)     
        #         subbox.prop(visualuv, 'stretch_type', expand=True)
        #     elif visualuv.operation == 'UV_ISLANDS':
        #         subbox = operation_box.box()
        #         subbox.prop(visualuv, 'hue_multiply', text='Color Variation')

        # refresh options
        refresh_box = layout.box()
        refresh_box.operator('visualuv.update', text='Refresh', icon='FILE_REFRESH')
        refresh_box.prop(visualuv, 'auto_update', text="Auto-Update")
        refresh_box.scale_y = 1.5
        layout.separator(factor=0.1)
        
        # controls for enabling additional features
        main_box = layout.box()
        main_box.prop(visualuv, 'alpha', text='Overlay Opacity', slider=True)
        if is_uv:
            main_box.prop(visualuv, 'overlay_layer', text='Layer', icon='NODE_COMPOSITING')
        main_box.prop(visualuv, 'show_3D', text='Render 3D Viewport', icon='VIEW3D')
        main_box.prop(visualuv, 'show_2D', text='Render UV Editor', icon='UV')
        if not is_uv:
            main_box.prop(visualuv, 'show_wire', text='Wireframe', icon='SHADING_WIRE')
            main_box.prop(visualuv, 'backface_culling', text='Backface Culling', icon='AXIS_SIDE')
        layout.separator(factor=0.1)

        # change color box
        if visualuv.operation != 'NONE':
            color_box = layout.box()
            color_box.prop(visualuv, 'enable_color_change', text='Color Change', icon='BRUSH_DATA')
            if visualuv.enable_color_change:
                color_box.prop(visualuv, 'hue_shift', text='Hue Shift', slider=True)
                color_box.prop(visualuv, 'saturation', text='Saturation', slider=True)
                color_box.prop(visualuv, 'value', text='Value', slider=True)
                color_box.separator(factor=0.1)
        layout.separator(factor=0.1)

        if is_uv:
            return

        # change location box
        location_box = layout.box()
        location_box.prop(visualuv, 'enable_position_change', text='Position Change', icon='OBJECT_ORIGIN')
        if visualuv.enable_position_change:
            location_box.prop(visualuv, 'location_offset', text='Location Offset')
            location_box.separator(factor=0.1)
        layout.separator(factor=0.1)

        # explosion view box
        explosion_box = layout.box()
        explosion_box.prop(visualuv, 'enable_explosion_view', text='Explosion View', icon='MOD_EXPLODE', toggle=True)
        if visualuv.enable_explosion_view:
            explosion_box.prop(visualuv, 'explosion_offset', text='Explosion Offset', slider=False)
            explosion_box.separator(factor=0.1)
        layout.separator(factor=0.1)

class VISUALUV_PT_3d_view(bpy.types.Panel, VisualUVPanel):
    bl_label = "VisualUV Overlays"
    bl_idname = "VISUALUV_PT_uv_tool_menu3d"
    # bl_space_type = 'VIEW_3D'
    # bl_region_type = 'UI'
    # bl_category = 'VisualUV'

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TK7_SK_CH"
    # bl_options = {"DEFAULT_CLOSED"}
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    @classmethod
    def poll(self, context):
      
        if context.scene.tk_main_menu  == '2':


            return True
    

        return False


    def draw(self, context):
        layout = self.layout
        self.draw_ui(layout, context, False)

class VISUALUV_PT_2d_view(bpy.types.Panel,VisualUVPanel):
    bl_label = "UV Overlay"
    bl_idname = "VISUALUV_PT_uv_tool_menu2d"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "TK7_SK_CH"

    def draw(self, context):
        layout = self.layout
        self.draw_ui(layout, context, True)


#_____________________Shaders_________________________

# import gpu

shared_functions = \
'''
    vec3 hsv2rgb(vec3 c);
    vec3 hsv2rgb(vec3 c)
    {
        // this function is from: https://gist.github.com/983/e170a24ae8eba2cd174f
        vec4 K = vec4(1.0f, 2.0f / 3.0f, 1.0f / 3.0f, 3.0f);
        vec3 p = abs(fract(c.xxx + K.xyz) * 6.0f - K.www);
        return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0f, 1.0f), c.y);
    }

    float get_division(float a, float b);
    float get_division(float a, float b)
    {
        if (a == 0.0f || b == 0.0f)
        {
            return 0.0f;
        }
        if (a > b) 
        {
            return a / b;
        }
        return b / a;
    }

    float normalized_value(float value, float max_value);
    float normalized_value(float value, float max_value) 
    {
        if (value > max_value)
            {
                value = max_value;
            }
            float COLOR_BLUE = 2.0f / 3.0f;
            float MIN_DIVISION = 1.0f;
            return COLOR_BLUE - (value - MIN_DIVISION) / (max_value - MIN_DIVISION) * COLOR_BLUE;
    }
'''

# shader info for the 3D Viewport shader
vert_out = gpu.types.GPUStageInterfaceInfo("shader_interface")
vert_out.smooth('VEC2', "uvInterp")
vert_out.smooth('VEC4', "tempColor")
vert_out.smooth('FLOAT', "fragmentHue")
shader_info = gpu.types.GPUShaderCreateInfo()
shader_info.push_constant('MAT4', "viewProjectionMatrix")
shader_info.push_constant('MAT4', "worldMatrix")

shader_info.typedef_source("struct UBO_3D {float hue_shift; \
                                            float hue_multiply; \
                                            float saturation; \
                                            float value; \
                                            float alpha; \
                                            float scale_factor; \
                                            int tex_enabled; \
                                            int tex_only; \
                                            float vert_offset; \
                                            float x_offset; \
                                            float y_offset; \
                                            float z_offset; \
                                            float explosion_offset; \
                                            float max_division;};")
shader_info.uniform_buf(0, 'UBO_3D', "ubo_3d")

shader_info.sampler(0, 'FLOAT_2D', "image")
shader_info.vertex_in(0, 'VEC3', "position")
shader_info.vertex_in(1, 'VEC3', "normal")
shader_info.vertex_in(2, 'VEC3', "uv")
shader_info.vertex_in(3, 'VEC2', "input")
shader_info.vertex_in(4, 'VEC3', "direction")
shader_info.vertex_out(vert_out)
shader_info.fragment_out(0, 'VEC4', "FragColor")

shader_info.vertex_source(shared_functions +
'''
    void main()
    {
        float color = 0.0f;
        if (ubo_3d.max_division > 0.0f) 
        {
            color = get_division(input.x, input.y);
            color = normalized_value(color, ubo_3d.max_division);
        }
        else
        {
            color = input.x;
        }
        uvInterp = uv.xy;
        vec3 hsv = vec3(mod((color + 0.001f) * ubo_3d.hue_multiply + ubo_3d.hue_shift, 1.0), ubo_3d.saturation, ubo_3d.value);
        fragmentHue = color;
        tempColor = vec4(hsv2rgb(hsv), ubo_3d.alpha);
        vec3 location_offset = vec3(ubo_3d.x_offset, ubo_3d.y_offset, ubo_3d.z_offset);
        gl_Position = viewProjectionMatrix * worldMatrix * vec4(position + normal * ubo_3d.vert_offset + direction * ubo_3d.explosion_offset + location_offset, 1.0f);
    }

'''
)

shader_info.fragment_source(
'''
    void main()
    {
        if (tempColor.a == 0) discard;
        vec4 tex = texture(image, uvInterp / abs(ubo_3d.scale_factor));
        if (ubo_3d.tex_enabled <= 0  && fragmentHue < 0.0f)
        {
            discard;
        }
        else if (ubo_3d.tex_enabled > 0 && ubo_3d.tex_only > 0)
        {
            FragColor = vec4(tex.r, tex.g, tex.b, tempColor.a);
        }
        else if (ubo_3d.tex_enabled > 0  && fragmentHue < 0.0f)
        {
            FragColor = vec4(tex.r, tex.g, tex.b, tempColor.a);
        }
        else if (ubo_3d.tex_enabled > 0) 
        {
            FragColor = vec4(tex.r * tempColor.r, tex.g * tempColor.g, tex.b * tempColor.b, tempColor.a);
        }
        else
        {
            FragColor = tempColor;
        }
    }
'''
)

SHADER_3D = gpu.shader.create_from_info(shader_info)


# shader info for the wireframe shader
vert_out_wireframe = gpu.types.GPUStageInterfaceInfo("uv_shader_interface_wireframe")
vert_out_wireframe.smooth('VEC4', "tempColor")
shader_info_wireframe = gpu.types.GPUShaderCreateInfo()
shader_info_wireframe.push_constant('MAT4', "viewProjectionMatrix")
shader_info_wireframe.push_constant('MAT4', "worldMatrix")
shader_info_wireframe.typedef_source("struct UBO_WIRE {float x_offset; \
                                                        float y_offset; \
                                                        float z_offset; \
                                                        float explosion_offset; \
                                                        float offset;};")
shader_info_wireframe.uniform_buf(0, 'UBO_WIRE', "ubo_wire")
shader_info_wireframe.vertex_in(0, 'VEC3', "position")
shader_info_wireframe.vertex_in(1, 'VEC3', "normal")
shader_info_wireframe.vertex_in(2, 'VEC3', "direction")
shader_info_wireframe.vertex_in(3, 'VEC4', "color")
shader_info_wireframe.vertex_out(vert_out_wireframe)
shader_info_wireframe.fragment_out(0, 'VEC4', "FragColor")

shader_info_wireframe.vertex_source(
'''
    void main()
    {
        tempColor = color;
        vec3 location_offset = vec3(ubo_wire.x_offset, ubo_wire.y_offset, ubo_wire.z_offset);
        gl_Position = viewProjectionMatrix * worldMatrix * vec4(position + normal * ubo_wire.offset + direction * ubo_wire.explosion_offset + location_offset, 1.0f);
    }
'''
)

shader_info_wireframe.fragment_source(
'''
    void main()
    {
        if (tempColor.a == 0) discard;
        FragColor = tempColor;
    }
'''
)

SHADER_WIREFRAME = gpu.shader.create_from_info(shader_info_wireframe)

# shader info for the UV Editor shader
vert_out_2D = gpu.types.GPUStageInterfaceInfo("uv_shader_interface_2D")
vert_out_2D.smooth('VEC4', "tempColor")
shader_info_2D = gpu.types.GPUShaderCreateInfo()
shader_info_2D.push_constant('MAT4', "ModelViewProjectionMatrix")
shader_info_2D.typedef_source("struct UBO_COLOR {float hue_shift; \
                                                float hue_multiply; \
                                                float saturation; \
                                                float value; \
                                                float alpha; \
                                                float layer; \
                                                float max_division;};")
shader_info_2D.uniform_buf(0, 'UBO_COLOR', "ubo_color")

shader_info_2D.vertex_in(0, 'VEC3', "position")
shader_info_2D.vertex_in(1, 'VEC2', "input")
shader_info_2D.vertex_out(vert_out_2D)
shader_info_2D.fragment_out(0, 'VEC4', "FragColor")

shader_info_2D.vertex_source(shared_functions +
'''
    void main()
    {
        float color = 0.0f;
        if (ubo_color.max_division > 0.0f) 
        {
            color = get_division(input.x, input.y);
            color = normalized_value(color, ubo_color.max_division);
        }
        else
        {
            color = input.x;
        }
        gl_Position = ModelViewProjectionMatrix * vec4(position.xy, 0.0f, 1.0f);
        gl_Position.z = 0.5f * (2f - ubo_color.layer);
        vec3 hsv = vec3(mod((color + 0.001f) * ubo_color.hue_multiply + ubo_color.hue_shift, 1.0), ubo_color.saturation, ubo_color.value);
        if (color < 0) 
        {
            tempColor = vec4(0.0f);
        }
        else 
        {
            tempColor = vec4(hsv2rgb(hsv), ubo_color.alpha);
        }
    }
'''
)

shader_info_2D.fragment_source(
'''
    void main()
    {
        if (tempColor.a == 0) discard;
        FragColor = vec4(tempColor.r, tempColor.g, tempColor.b, tempColor.a);
    }
'''
)

SHADER_2D = gpu.shader.create_from_info(shader_info_2D)


# shader info for the wireframe UV Editor shader
vert_out_2D_wireframe = gpu.types.GPUStageInterfaceInfo("uv_shader_interface_2D_wireframe")
vert_out_2D_wireframe.smooth('VEC4', "tempColor")
shader_info_2D_wireframe = gpu.types.GPUShaderCreateInfo()
shader_info_2D_wireframe.push_constant('MAT4', "ModelViewProjectionMatrix")
shader_info_2D_wireframe.typedef_source("struct UBO_WIRE {float hue_shift; \
                                                float hue_multiply; \
                                                float saturation; \
                                                float value; \
                                                float alpha; \
                                                float layer; \
                                                float max_division;};")
shader_info_2D_wireframe.uniform_buf(0, 'UBO_WIRE', "ubo_wire")

shader_info_2D_wireframe.vertex_in(0, 'VEC3', "position")
shader_info_2D_wireframe.vertex_in(1, 'VEC2', "input")
shader_info_2D_wireframe.vertex_out(vert_out_2D_wireframe)
shader_info_2D_wireframe.fragment_out(0, 'VEC4', "FragColor")

shader_info_2D_wireframe.vertex_source(shared_functions +
'''
    void main()
    {
        float color = 0.0f;
        if (ubo_wire.max_division > 0.0f) 
        {
            color = get_division(input.x, input.y);
            color = normalized_value(color, ubo_wire.max_division);
        }
        else
        {
            color = input.x;
        }
        gl_Position = ModelViewProjectionMatrix * vec4(position.xy, 0.0f, 1.0f);
        gl_Position.z = 0.5f * (2f - ubo_wire.layer);
        vec3 hsv = vec3(mod((color + 0.001f) * ubo_wire.hue_multiply + ubo_wire.hue_shift, 1.0), ubo_wire.saturation, ubo_wire.value);
        if (color < 0) 
        {
            tempColor = vec4(0.0f);
        }
        else 
        {
            tempColor = vec4(hsv2rgb(hsv), ubo_wire.alpha);
        }
    }
'''
)

shader_info_2D_wireframe.fragment_source(
'''
    void main()
    {
        if (tempColor.a == 0) discard;
        FragColor = tempColor;
    }
'''
)

shader_info_2D_wireframe = gpu.shader.create_from_info(shader_info_2D_wireframe)



# shader info for the UV Editor texture shader

# vert_out_texture = gpu.types.GPUStageInterfaceInfo("uv_texture_shader_interface_2D")
# vert_out_texture.smooth('VEC2', "uvInterp")
# shader_info_texture = gpu.types.GPUShaderCreateInfo()
# shader_info_texture.push_constant('MAT4', "ModelViewProjectionMatrix")
# shader_info_texture.typedef_source("struct UBO_TEX2D {float scale_factor; \
#                                                         float alpha; \
#                                                         float layer;};")
# shader_info_texture.uniform_buf(0, 'UBO_TEX2D', "ubo_tex2d")
# shader_info_texture.sampler(0, 'FLOAT_2D', "image")
# shader_info_texture.vertex_in(0, 'VEC3', "position")
# shader_info_texture.vertex_out(vert_out_texture)
# shader_info_texture.fragment_out(0, 'VEC4', "FragColor")

# shader_info_texture.vertex_source(
# '''
#     void main()
#     {
#         uvInterp = position.xy;
#         gl_Position = ModelViewProjectionMatrix * vec4(position.xy, 0.0f, 1.0f);
#         gl_Position.z = 0.5 * (2f - ubo_tex2d.layer);
#     }
# '''
# )

# shader_info_texture.fragment_source(
# '''
#     void main()
#     {
#         if (ubo_tex2d.alpha == 0) discard;
#         vec4 tex = texture(image, uvInterp / abs(ubo_tex2d.scale_factor));
#         FragColor = vec4(tex.r, tex.g, tex.b, tex.a * ubo_tex2d.alpha);
#     }
# '''
# )

# SHADER_TEXTURE_2D = gpu.shader.create_from_info(shader_info_texture)


#__________________Props______________________
# import bpy
# from bpy.props import BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, PointerProperty, IntProperty


class VISUALUV_ObjectProperties(bpy.types.PropertyGroup):
    enabled : BoolProperty()
    auto_update : BoolProperty(
        default=True,
        update=lambda self, context: self.update_func(),
        description="Toggle the Auto-Update feature"
    )
    backface_culling : BoolProperty(
        description="Turn on to cull backfaces"
    )
    show_wire : BoolProperty(
        default=True,
        description="Display wireframe in Edit-Mode, with seams, selected vertices, edges, and faces",
        update=lambda self, context: self.update_func()
    )
    alpha : FloatProperty(
        default=0.75,
        max=1.0,
        min=0.0,
        description="Tweak the overlay's opacity"
    )
    recalculate : BoolProperty()
    overlap_recalculate : BoolProperty()
    show_3D : BoolProperty(
        default=True,
        description="Display the overlay in the 3D Viewport"
    )
    show_2D : BoolProperty(
        default=True,
        description="Display the overlay in the UV Editor"
    )
    overlay_layer : IntProperty(
        default=1,
        description="Move the overlay between background and foreground of the UV Editor",
        min=0,
        max=2
    )
    enable_position_change : BoolProperty(
        description="Enable for the overlay's position manipulation"
    )
    enable_color_change : BoolProperty(
        description="Enable for the overlay's color manipulation"
    )
    enable_explosion_view : BoolProperty(
        description="Enable for separating and offsetting the overlay by individual UV islands",
        update=lambda self, context: self.update_func()
    )
    checker_texture : BoolProperty(
        default=False,
        update=lambda self, context: self.update_func()
    )
    fill_texture : BoolProperty(
        default=True,
        description="Fill the whole UV square with the selected texture of an active object"
    )
    image : PointerProperty(name='Image', type=bpy.types.Image)

    texture_scale : FloatProperty(
        default=1.0,
        soft_max=2.0,
        min=0.01,
        description="Tweak the texture's scale"
    )
    texture_alpha : FloatProperty(
        default=1.0,
        max=1.0, 
        min=0.0,
        description="Tweak the texture's opacity in the UV Editor"
    )
    max_division : FloatProperty(
        default=2.0,
        min=1.01,
        soft_max=5.0,
        description="Tweak the stretching sensitivity. Lower factor means higher sensitivity"
    )
    hue_shift : FloatProperty(
        default=0.0,
        max=1.0, 
        min=0.0,
        description="Tweak the overlay's color hue"
    )
    hue_multiply : FloatProperty(
        default=1.0,
        min=1.0,
        description="Change the color variation of UV islands"
    )
    saturation : FloatProperty(
        default=1.0,
        max=1.0,
        min=0.0,
        description="Tweak the overlay's color saturation"
    )
    value : FloatProperty(
        default=0.8,
        max=1.0, 
        min=0.0,
        description="Tweak the overlay's color value"
    )
    explosion_offset : FloatProperty(
        default=0.0,
        min=0.0,
        description="Tweak the offset of the explosion"
    )
    location_offset : FloatVectorProperty(
        subtype='XYZ',
        description="Tweak the overlay's position"
    )
    operation : EnumProperty(
        items=[
            ('NONE', "None", "", 1),
            ('UV_STRETCHING', "Stretching", "", 2),
            ('UV_ISLANDS', "Islands", "", 3),
            ('UV_NORMALS', "Normals", "", 4),
            ('UV_OVERLAP', "Overlap", "", 5)
        ],
        default='NONE',
        update=lambda self, context: self.update_func()
    )
    stretch_type : EnumProperty(
        items=[
            ('ANGLES', "Angles", "Stretching between angles of the UV map and the original model", 1), 
            ('AREA', "Area", "Stretching between the relative areas of the UV map and the original model", 2), 
            ('EDGE_LENGTH', "Edge length", "Stretching between the relative edge lengths of the UV map and the original model", 3)
        ], 
        default='ANGLES',
        update=lambda self, context: self.update_func()
    )

    def update_func(self):
        value = getattr(self, 'operation') != 'NONE' or getattr(self, 'checker_texture')
        setattr(self, 'recalculate', value)
        setattr(self, 'enabled', value)


class VISUALUV_WindowManagerProperties(bpy.types.PropertyGroup):
    select_overlap : BoolProperty(default=False)



# _____________________Operators___________________________________

# import os
# import uuid
# import bpy
# import gpu

# from bpy.types import Operator
# from mathutils import Vector
# from mathutils.geometry import area_tri, normal
# from bpy_extras import mesh_utils
# from gpu_extras.batch import batch_for_shader

# from .visualuv_shaders import SHADER_3D, SHADER_2D, SHADER_TEXTURE_2D, SHADER_WIREFRAME

COLOR_BLUE = 2.0 / 3.0
COLOR_RED = 1.0
COLOR_NEGATIVE = -1.0
HSV_HUE_MULTIPLY_DEFAULT = 1.0
HSV_HUE_SHIFT_DEFAULT = 0.0
HSV_SATURATION_DEFAULT = 1.0
HSV_VALUE_DEFAULT = 0.8
HSV_MIN_HUE = 0.0
HSV_MAX_HUE = 1.0

VERTEX_OFFSET = 0.0035
WIREFRAME_OFFSET_FACE = 0.005
WIREFRAME_OFFSET = 0.007
POSITION_OFFSET_DEFAULT = 0.0
EXPLOSION_OFFSET_DEFAULT = 0.0
ZERO_VECTOR_3D = Vector()
ZERO_VECTOR_4D = Vector((0.0, 0.0, 0.0, 0.0))

PLANE_VERTICES = (
            (0,1),(1,1),(0,0),
            (0,0),(1,1),(1,0)
)

ENABLED = 1
DISABLED = 0

EMPTY = 0.0

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
IMG_NAME = "__visualuv_checkers.png"

OVERLAY_HANDLERS = dict()
MODAL_HANDLERS = dict()


def get_checker_image():
    if bpy.data.images.find(IMG_NAME) == -1:                           
        return bpy.data.images.load(filepath= os.path.join(FILE_DIRECTORY, IMG_NAME))
    return bpy.data.images[IMG_NAME]


def check_image_remove():
    idx = bpy.data.images.find(IMG_NAME)
    if idx != -1 and not MODAL_HANDLERS:
        img = bpy.data.images[idx]
        bpy.data.images.remove(img)


def create_overlay_3d(draw_function):
    key_handler_3d = uuid.uuid4()
    OVERLAY_HANDLERS[key_handler_3d] = bpy.types.SpaceView3D.draw_handler_add(draw_function, (key_handler_3d,), 'WINDOW', 'POST_VIEW')


def create_overlay_2d(draw_function):
    key_handler_2d = uuid.uuid4()
    OVERLAY_HANDLERS[key_handler_2d] = bpy.types.SpaceImageEditor.draw_handler_add(draw_function, (key_handler_2d,), 'WINDOW', 'POST_VIEW')


def remove_overlay_3d(handler_key):
    handler = OVERLAY_HANDLERS.pop(handler_key, None)
    if handler:
        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')


def remove_overlay_2d(handler_key):
    handler = OVERLAY_HANDLERS.pop(handler_key, None)
    if handler:
        bpy.types.SpaceImageEditor.draw_handler_remove(handler, 'WINDOW')


class VisualUVOperator():

    @classmethod
    def poll(cls, context):
        if not context.selected_objects:
            return False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                return False
            if not obj.data.uv_layers.active:
                return False
        return True

class VISUALUV_OT_update(Operator, VisualUVOperator):
    bl_idname = "visualuv.update"
    bl_label = "Recalculate"
    bl_description = "Refresh the VisualUV overlay"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        for obj in context.selected_objects:
            visualuv = obj.visualuv
            if visualuv.enabled:
                visualuv.recalculate = True
                if visualuv.operation == 'UV_OVERLAP':
                    context.window_manager.visualuv.select_overlap = True
                if not MODAL_HANDLERS.get(obj):
                    obj.data.update()
                    bpy.ops.visualuv.overlay('INVOKE_DEFAULT')
        return {'FINISHED'}

class VISUALUV_OT_toggle_texture(Operator, VisualUVOperator):
    bl_idname = "visualuv.toggle_texture"
    bl_label = "Toggle Texture overlay"
    bl_description = "Enable/Disable Texture overlay"

    def execute(self, context):
        obj = context.object
        visualuv = obj.visualuv
        if not visualuv.enabled:
            visualuv.checker_texture = True
            obj.data.update()
            bpy.ops.visualuv.overlay('INVOKE_DEFAULT')
        elif visualuv.operation != 'NONE':
            visualuv.checker_texture = not visualuv.checker_texture
        else:
            visualuv.checker_texture = False
        return {'FINISHED'}

class TogglableOperationOperator(VisualUVOperator):

    def toggle_operation(self, context, operation):
        active_obj = context.object
        for obj in context.selected_objects:
            visualuv = obj.visualuv
            if not obj.data.uv_layers.active:
                continue
            context.view_layer.objects.active = obj
            if not visualuv.enabled:
                visualuv.operation = operation
                obj.data.update()
                bpy.ops.visualuv.overlay('INVOKE_DEFAULT')
            elif visualuv.operation != operation:
                visualuv.operation = operation
            else:
                visualuv.operation = 'NONE'
        context.view_layer.objects.active = active_obj

class VISUALUV_OT_toggle_stretching(Operator, TogglableOperationOperator):
    bl_idname = "visualuv.toggle_stretching"
    bl_label = "Toggle UV Stretching overlay"
    bl_description = "Enable/Disable UV Stretching overlay"
    
    def execute(self, context):
        self.toggle_operation(context, 'UV_STRETCHING')
        return {'FINISHED'}

class VISUALUV_OT_toggle_islands(Operator, TogglableOperationOperator):
    bl_idname = "visualuv.toggle_islands"
    bl_label = "Toggle Colored UV Islands overlay"
    bl_description = "Enable/Disable Colored UV Islands overlay"

    def execute(self, context):
        self.toggle_operation(context, 'UV_ISLANDS')
        return {'FINISHED'}

class VISUALUV_OT_toggle_normals(Operator, TogglableOperationOperator):
    bl_idname = "visualuv.toggle_normals"
    bl_label = "Toggle Flipped UV Normals overlay"
    bl_description = "Enable/Disable UV Normals overlay. Useful for visualizing flipped UVs"

    def execute(self, context):
        self.toggle_operation(context, 'UV_NORMALS')
        return {'FINISHED'}

class VISUALUV_OT_toggle_overlap(Operator, TogglableOperationOperator):
    bl_idname = "visualuv.toggle_overlap"
    bl_label = "Toggle Overlapping UVs overlay"
    bl_description = "Enable/Disable Overlapping UVs overlay. This operator requires manual refreshing"

    def execute(self, context):
        for obj in context.selected_objects:
            visualuv = obj.visualuv
            if visualuv.operation != 'UV_OVERLAP' and obj.mode == 'EDIT':
                context.window_manager.visualuv.select_overlap = True
        self.toggle_operation(context, 'UV_OVERLAP')
        return {'FINISHED'}

class VISUALUV_OT_overlay(Operator):
    bl_idname = "visualuv.overlay"
    bl_label = "VisualUV overlay operator"
    bl_description = "Draw VisualUV overlay"
    bl_options = {'REGISTER', 'INTERNAL'}

    def recalculate_poly_islands(self, mesh):
        obj = self.invoked_obj
        visualuv = obj.visualuv
        islands = mesh_utils.mesh_linked_uv_islands(mesh)
        color_value = HSV_MIN_HUE
        island_count = len(islands)
        if not island_count:
            return
        step = HSV_MAX_HUE / island_count
        object_location = Vector(obj.location)
        for island in islands:
            island_center = Vector()
            color_value += step
            for polygon_index in island:
                island_center += Vector(mesh.polygons[polygon_index].center)
                self.island_colors[polygon_index] = Vector((color_value, 0.0))
            island_center = island_center / len(island)
            if not visualuv.enable_explosion_view:
                continue
            direction = island_center - object_location
            if direction == Vector():
                direction = Vector((0.0, 0.0, 1.0))
            else:
                direction = direction.normalized()
            for polygon_index in island:
                self.directions[polygon_index] = direction

    def label_overlapped(self, mesh):
        self.overlapped_polygons = dict()
        for polygon in mesh.polygons:
            is_selected = True
            for loop_index in polygon.loop_indices:
                if not mesh.uv_layers.active.data[loop_index].select:
                    is_selected = False
            if is_selected:
                self.overlapped_polygons[polygon.index] = True

    def calc_uv_island_colors(self, triangle):
        color = self.island_colors[triangle.polygon_index]
        return 3 * [color]

    def recalculate_uv_normals(self, uv_coords):
            color = COLOR_BLUE if normal(uv_coords).z >= 0.0 else COLOR_RED
            return 3 * [Vector((color, 0.0))]

    def recalculate_uv_overlap(self, triangle):
        if self.overlapped_polygons.get(triangle.polygon_index):
            return 3 * [Vector((COLOR_BLUE, 0.0))]
        return 3 * [Vector((COLOR_NEGATIVE, 0.0))]

    def recalculate_stretching(self, triangle, triangle_coords, uv_coords):
            visualuv = self.invoked_obj.visualuv
            if visualuv.stretch_type == 'ANGLES':
                return self.recalculate_angle_stretching(triangle, triangle_coords, uv_coords)
            elif visualuv.stretch_type == 'AREA':
                return self.recalculate_area_stretching(triangle, triangle_coords, uv_coords)
            else:
                return self.recalculate_edge_length_stretching(triangle, triangle_coords, uv_coords)

    def recalculate_area_stretching(self, triangle, triangle_coords, uv_coords):
            triangle_directions = [(v1 - v0) for v0, v1 in zip(triangle_coords, triangle_coords[1:] + triangle_coords[0:1])]
            triangle_directions_normalized = [v.normalized() for v in triangle_directions]
            triangle_sides = Vector(v.length for v in triangle_directions).normalized()
            uv_directions = [(v1 - v0) for v0, v1 in zip(uv_coords, uv_coords[1:] + uv_coords[0:1])]
            uv_directions_normalized = [v.normalized() for v in uv_directions]
            uv_sides = Vector(v.length for v in uv_directions).normalized()

            normalized_uv_coords = []
            normalized_triangle_coords = []
            uv_co = Vector()
            tri_co = Vector()
            for i, _ in enumerate(triangle.vertices):
                uv_co += uv_sides[i] * uv_directions_normalized[i]
                tri_co += triangle_sides[i] * uv_directions_normalized[i]
                normalized_uv_coords.append(uv_co.copy())
                normalized_triangle_coords.append(tri_co.copy())            

            triangle_area = area_tri(*normalized_triangle_coords)
            uv_area = area_tri(*normalized_uv_coords)
            key = triangle.polygon_index

            if self.areas.get(key):
                area_input = self.areas.get(key)
                area_input.x += triangle_area
                area_input.y += uv_area
            else:
                area_input = Vector((triangle_area, uv_area))
                self.areas[key] = area_input
            return 3 * [area_input]

    def recalculate_edge_length_stretching(self, triangle, triangle_coords, uv_coords):
            triangle_vec = Vector((v1 - v0).length for v0, v1 in zip(triangle_coords, triangle_coords[1:] + triangle_coords[0:1])).normalized()
            uv_vec = Vector((v1 - v0).length for v0, v1 in zip(uv_coords, uv_coords[1:] + uv_coords[0:1])).normalized()

            key = triangle.polygon_index
            length_input = self.total_lengths.get(key)
            if not length_input:
                length_input = Vector((0.0, 1.0))
            for length, uv_length in zip(triangle_vec, uv_vec):
                if (length == 0.0 or uv_length == 0.0):
                    division = 0.0
                else:
                    division = length / uv_length if length > uv_length else uv_length / length
                length_input.x = (length_input.x + division) / 2.0
            self.total_lengths[key] = length_input
            return 3 * [length_input]

    def recalculate_angle_stretching(self, triangle, triangle_coords, uv_coords):
            tri_angles = self.get_angles(*triangle_coords)
            uv_angles = self.get_angles(*uv_coords)

            output = []
            for i, vert_index in enumerate(triangle.vertices):
                tri_angle = tri_angles[i]
                uv_angle = uv_angles[i]
                key = (vert_index, triangle.polygon_index)
                if self.angles.get(key):
                    angle_input = self.angles.get(key)
                    angle_input.x += tri_angle
                    angle_input.y += uv_angle
                else:
                    angle_input = Vector((tri_angle, uv_angle))
                    self.angles[key] = angle_input
                output.append(angle_input)
            return output

    def get_angles(self, vert1: Vector, vert2: Vector, vert3: Vector):
        edge1 = vert2 - vert1
        edge2 = vert3 - vert1
        angle1 = 0.0 if edge1.length == 0.0 or edge2.length == 0.0 else edge1.angle(edge2)

        edge1 = vert3 - vert2
        edge2 = vert1 - vert2
        angle2 = 0.0 if edge1.length == 0.0 or edge2.length == 0.0 else edge1.angle(edge2)

        edge1 = vert1 - vert3
        edge2 = vert2 - vert3
        angle3 = 0.0 if edge1.length == 0.0 or edge2.length == 0.0 else edge1.angle(edge2)

        return angle1, angle2, angle3

    def recalc_triangle_input(self, obj, mesh, triangle, triangle_coords, uv_coords):
        visualuv = obj.visualuv
        if visualuv.operation == 'UV_ISLANDS':
            return self.calc_uv_island_colors(triangle)
        elif visualuv.operation == 'UV_STRETCHING':
            return self.recalculate_stretching(triangle, triangle_coords, uv_coords)
        elif visualuv.operation == 'UV_NORMALS':
            return self.recalculate_uv_normals(uv_coords)
        elif visualuv.operation == 'UV_OVERLAP' and self.invoked_obj.mode == 'EDIT':
            return self.recalculate_uv_overlap(triangle)
        return 3 * [Vector((COLOR_NEGATIVE, EMPTY))]

    def clear_properties(self):
        self.directions = dict()
        self.areas = dict()
        self.angles = dict()
        self.total_lengths = dict()
        self.island_colors = dict()
        
        self.verts = []
        self.normals = []
        self.uvs = []
        self.vert_directions = []
        self.input = []
        self.uv_colors = []
        self.tex_coords = []

        self.wireframe_coords = []
        self.wireframe_normals = []
        self.wireframe_directions = []

        self.wireframe_vertex_colors = []
        self.wireframe_edge_colors = []
        self.wireframe_face_colors = []
        self.wireframe_seam_colors = []

    def recalculate_info(self, context, obj):
        visited_edges = dict()
        self.clear_properties()

        if context.window_manager.visualuv.select_overlap and obj.mode == 'EDIT':
            context.window_manager.visualuv.select_overlap = False
            if not bpy.context.tool_settings.use_uv_select_sync:
                bpy.ops.uv.select_overlap()
                for selected_obj in context.selected_objects:
                    selected_obj.visualuv.overlap_recalculate = True

        obj.update_from_editmode()
        depsgraph = context.evaluated_depsgraph_get()
        # this new object might differ from the original, but we only need it for the mesh
        obj = obj.evaluated_get(depsgraph)
        mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
        # we need the object for its properties, let's revert to the original
        obj = self.invoked_obj
        visualuv = obj.visualuv
        visualuv.recalculate = False
        uv_map_name = mesh.uv_layers.active.name
        active_uv_map = mesh.attributes[uv_map_name].data
        theme_colors = context.preferences.themes["Default"].view_3d

        if visualuv.overlap_recalculate:
            self.label_overlapped(mesh)
            visualuv.overlap_recalculate = False

        if visualuv.operation == 'UV_ISLANDS' or visualuv.enable_explosion_view:
            self.recalculate_poly_islands(mesh)

        mesh.calc_loop_triangles()

        verts = 3 * [ZERO_VECTOR_3D]
        normals = 3 * [ZERO_VECTOR_3D]
        vert_directions = 3 * [ZERO_VECTOR_3D]
        uv_coords = 3 * [ZERO_VECTOR_3D]
        
        wireframe_face_colors = 3 * [ZERO_VECTOR_4D]
        wireframe_coords = 6 * [ZERO_VECTOR_3D]
        wireframe_normals = 6 * [ZERO_VECTOR_3D]
        wireframe_directions  = 6 * [ZERO_VECTOR_3D]
        wireframe_seam_colors  = 6 * [ZERO_VECTOR_4D]
        wireframe_edge_colors  = 6 * [ZERO_VECTOR_4D]
        wireframe_vertex_colors  = 6 * [ZERO_VECTOR_4D]

        color_vertex_select = (*theme_colors.vertex_select, 1.0)
        color_vertex = (*theme_colors.vertex, 1.0)
        color_face_selected = theme_colors.face_select
        color_transparent = ZERO_VECTOR_4D
        color_edge_seam = (*theme_colors.edge_seam, 1.0)
        color_edge_select = (*theme_colors.edge_select, 1.0)
        color_edge = (*theme_colors.wire_edit, 1.0)

        for _, triangle in enumerate(mesh.loop_triangles):
            polygon = mesh.polygons[triangle.polygon_index]
            if polygon.hide:
                continue

            if visualuv.enable_explosion_view:
                direction = self.directions[polygon.index][:]
            else:
                direction = ZERO_VECTOR_3D

            for i, loop_index in enumerate(triangle.loops):
                
                vertex = mesh.vertices[triangle.vertices[i]]
                verts[i] = vertex.co
                normals[i] = vertex.normal
                vert_directions[i] = direction
                # we must keep a copy of UV coordinates, Blender generaly does not keep UV references
                uv_coords[i] = Vector((*(active_uv_map[loop_index].vector), 0.0))

                wireframe_face_colors[i] = color_face_selected if polygon.select else color_transparent
                
                if (visualuv.show_wire and obj.mode == 'EDIT'):
                    
                    # calculate wireframe
                    loop = mesh.loops[loop_index]
                    edge = mesh.edges[loop.edge_index]
                    if not visited_edges.get(loop.edge_index):
                        visited_edges[loop.edge_index] = True
                        for j, vert_index in enumerate(edge.vertices):
                            vertex = mesh.vertices[vert_index]
                            array_index = (i * 2) + j
                            wireframe_coords[array_index] = vertex.co
                            wireframe_normals[array_index] = vertex.normal
                            wireframe_directions[array_index] = direction

                            wireframe_vertex_colors[array_index] = color_vertex_select if vertex.select else color_vertex
                            wireframe_seam_colors[array_index] = color_edge_seam if edge.use_seam else color_transparent
                            wireframe_edge_colors[array_index] = color_edge_select if edge.select else color_edge

            self.wireframe_vertex_colors.extend(wireframe_vertex_colors)
            self.wireframe_edge_colors.extend(wireframe_edge_colors)
            self.wireframe_seam_colors.extend(wireframe_seam_colors)
            self.wireframe_face_colors.extend(wireframe_face_colors)

            self.wireframe_coords.extend(wireframe_coords)
            self.wireframe_normals.extend(wireframe_normals)
            self.wireframe_directions.extend(wireframe_directions)

            self.verts.extend(verts)
            self.normals.extend(normals)
            self.vert_directions.extend(vert_directions)

            # get info for the 3D Vieport shader
            triangle_input = self.recalc_triangle_input(obj, mesh, triangle, verts, uv_coords)

            self.input.extend(triangle_input)
            self.tex_coords.extend(uv_coords)

            if polygon.select or bpy.context.tool_settings.use_uv_select_sync:
                self.uv_colors.extend(triangle_input)
                self.uvs.extend(uv_coords)

        self.prepare_shader_batches(obj)

    def prepare_shader_batches(self, obj):
        visualuv = obj.visualuv
        uv_vertices = self.uvs if not visualuv.fill_texture else PLANE_VERTICES

        # batch UV Editor
        
        # self.batch_texture = batch_for_shader(
        #     SHADER_TEXTURE_2D,
        #     'TRIS',
        #     {
        #         "position": uv_vertices
        #     }
        # )

        self.batch_2d = batch_for_shader(
            SHADER_2D,
            'TRIS',
            {
                "position": self.uvs,
                "input": self.uv_colors
            }
        )

        # prepare mesh buffers
        mesh_buffer_size = len(self.verts)

        verts_format = gpu.types.GPUVertFormat()
        verts_format.attr_add(id="position", comp_type='F32', len=3, fetch_mode='FLOAT')
        verts_vbo = gpu.types.GPUVertBuf(verts_format, mesh_buffer_size)
        verts_vbo.attr_fill("position", self.verts)

        normals_format = gpu.types.GPUVertFormat()
        normals_format.attr_add(id="normal", comp_type='F32', len=3, fetch_mode='FLOAT')
        normals_vbo = gpu.types.GPUVertBuf(normals_format, mesh_buffer_size)
        normals_vbo.attr_fill("normal", self.normals)

        inputs_format = gpu.types.GPUVertFormat()
        inputs_format.attr_add(id="input", comp_type='F32', len=2, fetch_mode='FLOAT')
        inputs_vbo = gpu.types.GPUVertBuf(inputs_format, mesh_buffer_size)
        inputs_vbo.attr_fill("input", self.input)

        directions_format = gpu.types.GPUVertFormat()
        directions_format.attr_add(id="direction", comp_type='F32', len=3, fetch_mode='FLOAT')
        directions_vbo = gpu.types.GPUVertBuf(directions_format, mesh_buffer_size)
        directions_vbo.attr_fill("direction", self.vert_directions)

        uvs_format = gpu.types.GPUVertFormat()
        uvs_format.attr_add(id="uv", comp_type='F32', len=3, fetch_mode='FLOAT')
        uvs_vbo = gpu.types.GPUVertBuf(uvs_format, mesh_buffer_size)
        uvs_vbo.attr_fill("uv", self.tex_coords)

        self.batch_3d = gpu.types.GPUBatch(type='TRIS', buf=verts_vbo)
        self.batch_3d.vertbuf_add(normals_vbo)
        self.batch_3d.vertbuf_add(inputs_vbo)
        self.batch_3d.vertbuf_add(directions_vbo)
        self.batch_3d.vertbuf_add(uvs_vbo)
        
        # prepare wireframe buffers
        wireframe_buffer_size = len(self.wireframe_coords)

        wireframe_color_format = gpu.types.GPUVertFormat()
        wireframe_color_format.attr_add(id="color", comp_type='F32', len=4, fetch_mode='FLOAT')
        wireframe_vertex_colors_vbo = gpu.types.GPUVertBuf(wireframe_color_format, wireframe_buffer_size)
        wireframe_vertex_colors_vbo.attr_fill("color", self.wireframe_vertex_colors)

        wireframe_edge_colors_vbo = gpu.types.GPUVertBuf(wireframe_color_format, wireframe_buffer_size)
        wireframe_edge_colors_vbo.attr_fill("color", self.wireframe_edge_colors)

        wireframe_seam_colors_vbo = gpu.types.GPUVertBuf(wireframe_color_format, wireframe_buffer_size)
        wireframe_seam_colors_vbo.attr_fill("color", self.wireframe_seam_colors)

        wireframe_coords_format = gpu.types.GPUVertFormat()
        wireframe_coords_format.attr_add(id="position", comp_type='F32', len=3, fetch_mode='FLOAT')
        wireframe_coords_vbo = gpu.types.GPUVertBuf(wireframe_coords_format, wireframe_buffer_size)
        wireframe_coords_vbo.attr_fill("position", self.wireframe_coords)

        wireframe_normals_format = gpu.types.GPUVertFormat()
        wireframe_normals_format.attr_add(id="normal", comp_type='F32', len=3, fetch_mode='FLOAT')
        wireframe_normals_vbo = gpu.types.GPUVertBuf(wireframe_normals_format, wireframe_buffer_size)
        wireframe_normals_vbo.attr_fill("normal", self.wireframe_normals)

        wireframe_directions_format = gpu.types.GPUVertFormat()
        wireframe_directions_format.attr_add(id="direction", comp_type='F32', len=3, fetch_mode='FLOAT')
        wireframe_directions_vbo = gpu.types.GPUVertBuf(wireframe_directions_format, wireframe_buffer_size)
        wireframe_directions_vbo.attr_fill("direction", self.wireframe_directions)

        wireframe_face_color_format = gpu.types.GPUVertFormat()
        wireframe_face_color_format.attr_add(id="color", comp_type='F32', len=4, fetch_mode='FLOAT')
        wireframe_face_colors_colors_vbo = gpu.types.GPUVertBuf(wireframe_face_color_format, mesh_buffer_size)
        wireframe_face_colors_colors_vbo.attr_fill("color", self.wireframe_face_colors)

        # batch wireframe faces
        self.batch_wireframe_face = gpu.types.GPUBatch(type='TRIS', buf=verts_vbo)
        self.batch_wireframe_face.vertbuf_add(normals_vbo)
        self.batch_wireframe_face.vertbuf_add(directions_vbo)
        self.batch_wireframe_face.vertbuf_add(wireframe_face_colors_colors_vbo)

        # batch wireframe vertices 
        self.batch_wireframe_vertex = gpu.types.GPUBatch(type='POINTS', buf=wireframe_coords_vbo)
        self.batch_wireframe_vertex.vertbuf_add(wireframe_normals_vbo)
        self.batch_wireframe_vertex.vertbuf_add(wireframe_directions_vbo)
        self.batch_wireframe_vertex.vertbuf_add(wireframe_vertex_colors_vbo)
        
        self.batch_wireframe_vertex_lines = gpu.types.GPUBatch(type='LINES', buf=wireframe_coords_vbo)
        self.batch_wireframe_vertex_lines.vertbuf_add(wireframe_normals_vbo)
        self.batch_wireframe_vertex_lines.vertbuf_add(wireframe_directions_vbo)
        self.batch_wireframe_vertex_lines.vertbuf_add(wireframe_vertex_colors_vbo)

        # batch wireframe edges 
        self.batch_wireframe_edge = gpu.types.GPUBatch(type='LINES', buf=wireframe_coords_vbo)
        self.batch_wireframe_edge.vertbuf_add(wireframe_normals_vbo)
        self.batch_wireframe_edge.vertbuf_add(wireframe_directions_vbo)
        self.batch_wireframe_edge.vertbuf_add(wireframe_edge_colors_vbo)

        # batch wireframe seams
        self.batch_wireframe_seam = gpu.types.GPUBatch(type='LINES', buf=wireframe_coords_vbo)
        self.batch_wireframe_seam.vertbuf_add(wireframe_normals_vbo)
        self.batch_wireframe_seam.vertbuf_add(wireframe_directions_vbo)
        self.batch_wireframe_seam.vertbuf_add(wireframe_seam_colors_vbo)

    def draw_overlay_uv(self, handler_key):
        context = bpy.context
        try:
            obj = self.invoked_obj
            visualuv = obj.visualuv
            if not visualuv.enabled:
                remove_overlay_2d(handler_key)
                return
        except ReferenceError:
            remove_overlay_2d(handler_key)
            return

        if context.space_data.mode != 'UV':
            return
        if not visualuv.show_2D:
            return
        if not obj.select_get():
            return
        if obj.mode != 'EDIT':
            return

        texture = gpu.texture.from_image(visualuv.image)
        # Prepare texture shader for drawing
        # Create float buffer with padding => final size has to be multiple of vec4
        args = (
            visualuv.texture_scale,
            visualuv.texture_alpha,
            visualuv.overlay_layer,
            EMPTY
        )

        # buf_tex2d = gpu.types.Buffer('FLOAT', len(args), args)
        # ubo_tex2d = gpu.types.GPUUniformBuf(buf_tex2d)
        # SHADER_TEXTURE_2D.uniform_block("ubo_tex2d", ubo_tex2d)
        # SHADER_TEXTURE_2D.uniform_sampler("image", texture)

        # if visualuv.checker_texture and obj is bpy.context.object:
        #     gpu.state.depth_test_set('LESS_EQUAL')
        #     gpu.state.blend_set('ALPHA')
        #     self.batch_texture.draw(SHADER_TEXTURE_2D)

        # gpu.state.depth_test_set('NONE')
        # gpu.state.blend_set('NONE')
        
        # if visualuv.checker_texture and visualuv.operation == 'NONE':
        #     return

        # Prepare 2D shader for drawing
        gpu.state.depth_test_set('LESS_EQUAL')
        gpu.state.blend_set('ALPHA')

        hue_multiply = visualuv.hue_multiply if visualuv.operation == 'UV_ISLANDS' else HSV_HUE_MULTIPLY_DEFAULT
        hue_shift = visualuv.hue_shift if visualuv.enable_color_change else HSV_HUE_SHIFT_DEFAULT
        saturation = visualuv.saturation if visualuv.enable_color_change else HSV_SATURATION_DEFAULT
        value = visualuv.value if visualuv.enable_color_change else HSV_VALUE_DEFAULT
        max_division = visualuv.max_division if visualuv.operation == 'UV_STRETCHING' else EMPTY

        # Create float buffer with padding => final size has to be multiple of vec4
        args = (
            hue_shift, hue_multiply, saturation, value,
            visualuv.alpha, visualuv.overlay_layer, max_division,
            EMPTY, EMPTY, EMPTY, EMPTY, EMPTY
        )

        buf_color = gpu.types.Buffer('FLOAT', len(args), args)
        ubo_color = gpu.types.GPUUniformBuf(buf_color)
        SHADER_2D.uniform_block("ubo_color", ubo_color) 
        self.batch_2d.draw(SHADER_2D)

        gpu.state.depth_test_set('NONE')
        gpu.state.blend_set('NONE')

    def draw_overlay(self, handler_key): 
        try:
            obj = self.invoked_obj
            visualuv = obj.visualuv
            if not visualuv.enabled:
                remove_overlay_3d(handler_key)
                return
        except ReferenceError:
            remove_overlay_3d(handler_key)
            return
        
        if not visualuv.show_3D:
            return
        if visualuv.backface_culling:
            gpu.state.face_culling_set('BACK') 
        gpu.state.depth_test_set('LESS_EQUAL')
        gpu.state.blend_set('NONE')

        texture = gpu.texture.from_image(visualuv.image)
        # Prepare 3D shader for drawing
        SHADER_3D.uniform_float("viewProjectionMatrix", bpy.context.region_data.perspective_matrix)
        SHADER_3D.uniform_float("worldMatrix", obj.matrix_world)

        hue_multiply = visualuv.hue_multiply if visualuv.operation == 'UV_ISLANDS' else HSV_HUE_MULTIPLY_DEFAULT
        hue_shift = visualuv.hue_shift if visualuv.enable_color_change else HSV_HUE_SHIFT_DEFAULT
        saturation = visualuv.saturation if visualuv.enable_color_change else HSV_SATURATION_DEFAULT
        value = visualuv.value if visualuv.enable_color_change else HSV_VALUE_DEFAULT
        alpha = visualuv.alpha

        scale_factor = visualuv.texture_scale
        tex_enabled = ENABLED if visualuv.checker_texture else DISABLED
        tex_only = ENABLED if visualuv.checker_texture and visualuv.operation == 'NONE' else DISABLED

        x_offset = visualuv.location_offset.x if visualuv.enable_position_change else POSITION_OFFSET_DEFAULT
        y_offset = visualuv.location_offset.y if visualuv.enable_position_change else POSITION_OFFSET_DEFAULT
        z_offset = visualuv.location_offset.z if visualuv.enable_position_change else POSITION_OFFSET_DEFAULT
        explosion_offset = visualuv.explosion_offset if visualuv.enable_explosion_view else EXPLOSION_OFFSET_DEFAULT

        max_division = visualuv.max_division if visualuv.operation == 'UV_STRETCHING' else EMPTY

        # Create float buffer with padding => final size has to be multiple of vec4
        args = (
            hue_shift, hue_multiply, saturation, value, alpha,
            scale_factor, tex_enabled, tex_only, VERTEX_OFFSET,
            x_offset, y_offset, z_offset, explosion_offset,
            max_division, EMPTY, EMPTY
        )

        buf_3d = gpu.types.Buffer('FLOAT', len(args), args)
        ubo_3d = gpu.types.GPUUniformBuf(buf_3d)
        SHADER_3D.uniform_block("ubo_3d", ubo_3d)
        SHADER_3D.uniform_sampler("image", texture)
        self.batch_3d.draw(SHADER_3D)


        # # Prepare wireframe shader for drawing
        if obj.mode == 'EDIT' and visualuv.show_wire:
            gpu.state.depth_test_set('LESS_EQUAL')
            gpu.state.blend_set('ALPHA')

            SHADER_WIREFRAME.uniform_float("viewProjectionMatrix", bpy.context.region_data.perspective_matrix)
            SHADER_WIREFRAME.uniform_float("worldMatrix", obj.matrix_world)

            # Create float buffer with padding => final size has to be multiple of vec4
            wireframe_args = (
                x_offset, y_offset, z_offset, explosion_offset,
                WIREFRAME_OFFSET, EMPTY, EMPTY, EMPTY
            )

            buf_wire = gpu.types.Buffer('FLOAT', len(wireframe_args), wireframe_args)
            ubo_wire = gpu.types.GPUUniformBuf(buf_wire)
            SHADER_WIREFRAME.uniform_block("ubo_wire", ubo_wire)

            gpu.state.line_width_set(6)
            self.batch_wireframe_seam.draw(SHADER_WIREFRAME)
            gpu.state.line_width_set(4)

            # Create float buffer with padding => final size has to be multiple of vec4
            # Face wireframe has different offset than the rest
            wireframe_args = (
                x_offset, y_offset, z_offset, explosion_offset,
                WIREFRAME_OFFSET_FACE, EMPTY, EMPTY, EMPTY
            )

            buf_wire = gpu.types.Buffer('FLOAT', len(wireframe_args), wireframe_args)
            ubo_wire = gpu.types.GPUUniformBuf(buf_wire)
            SHADER_WIREFRAME.uniform_block("ubo_wire", ubo_wire)

            self.batch_wireframe_face.draw(SHADER_WIREFRAME)
            gpu.state.line_width_set(1)

            #  wireframe edges are visibile all the time if wirefrime is enabled
            self.batch_wireframe_edge.draw(SHADER_WIREFRAME)     

            # draws wireframe vertices only if vertex selection mode is enabled
            vertex_select_mode = bpy.context.tool_settings.mesh_select_mode[0]
            if vertex_select_mode:
                gpu.state.point_size_set(4)
                self.batch_wireframe_vertex.draw(SHADER_WIREFRAME)
                self.batch_wireframe_vertex_lines.draw(SHADER_WIREFRAME)      

        gpu.state.point_size_set(1)
        gpu.state.line_width_set(1)
        gpu.state.depth_test_set('NONE')
        gpu.state.blend_set('NONE')
        
        if visualuv.backface_culling:
            gpu.state.face_culling_set('NONE')

    def modal(self, context, event):
        try:
            obj = self.invoked_obj
            visualuv = obj.visualuv
            if not visualuv.enabled:
                MODAL_HANDLERS.pop(obj, None)
                check_image_remove()
                return {'FINISHED'}
        except ReferenceError:
            MODAL_HANDLERS.pop(obj, None)
            check_image_remove()
            return {'FINISHED'}

        for area in bpy.context.screen.areas :
            if area.type == 'IMAGE_EDITOR' or area.type == 'VIEW_3D':
                area.tag_redraw()

        self.check_image_exists()
        if visualuv.auto_update and event.value in ('RELEASE', 'CLICK') and event.value_prev not in ('RELEASE', 'CLICK'):
            visualuv.recalculate = True
            return {'PASS_THROUGH'}

        if visualuv.recalculate:
            self.recalculate_info(context, obj)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.invoked_obj = context.object
        obj = self.invoked_obj
        self.check_image_exists()
        self.recalculate_info(context, obj)
        create_overlay_3d(self.draw_overlay)
        create_overlay_2d(self.draw_overlay_uv) 
        MODAL_HANDLERS[obj] = self
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def check_image_exists(self):
        visualuv = self.invoked_obj.visualuv
        if not visualuv.image:
            visualuv.image = get_checker_image()


    


#___________________Init________________________


# from .visualuv_ui import VISUALUV_PT_3d_view, VISUALUV_PT_2d_view
# from .visualuv_ops import (VISUALUV_OT_update, VISUALUV_OT_toggle_texture, VISUALUV_OT_toggle_stretching,
    # VISUALUV_OT_toggle_islands, VISUALUV_OT_toggle_normals, VISUALUV_OT_toggle_overlap, VISUALUV_OT_overlay)
# from .visualuv_props import VISUALUV_ObjectProperties, VISUALUV_WindowManagerProperties






# bl_info = {
#     "name": "VisualUV",
#     "author": "Samuel Bílek",
#     "description": "Adds UV Mapping visualization overlays for objects. \
#         Useful for quick texture preview and visualising UV Stretching, Flipped UVs, Overlapped UVs and for coloring individual UV Islands.",
#     "blender": (3, 5, 0),
#     "version": (0, 0, 1),
#     "location": "3D Viewport / UV Editor > Tools > VisualUV",
#     "warning": "",
#     "category": "Object"
# }

# classes = (
#     VISUALUV_PT_3d_view,
#     VISUALUV_PT_2d_view,
#     VISUALUV_OT_update,
#     VISUALUV_OT_toggle_texture,
#     VISUALUV_OT_toggle_stretching,
#     VISUALUV_OT_toggle_islands,
#     VISUALUV_OT_toggle_normals,
#     VISUALUV_OT_toggle_overlap,
#     VISUALUV_OT_overlay,
#     VISUALUV_ObjectProperties,
#     VISUALUV_WindowManagerProperties
# )

# def register():
#     for c in classes:
#         bpy.utils.register_class(c)
#     bpy.types.Object.visualuv = PointerProperty(type=VISUALUV_ObjectProperties)
#     bpy.types.WindowManager.visualuv = PointerProperty(type=VISUALUV_WindowManagerProperties)


# def unregister():
#     del bpy.types.WindowManager.visualuv
#     del bpy.types.Object.visualuv

#     for c in classes:
#         bpy.utils.unregister_class(c)


# if __name__ == "__main__":
#     register()




