#import time

import bpy
import bmesh
import locale

#import asyncio

from bpy.props import FloatVectorProperty
from bpy.types import Operator, Panel
from mathutils import Vector

languages = {
    'en_US': {
        "Vertex Normal Batch Setting Plugin": "Vertex Normal Batch Setting Plugin",
        "Apply Normals": "Apply Normals",
        "LoongLy:No mesh objects selected": "LoongLy:No mesh objects selected",
        "LoongLy:Vertex normals set to": "LoongLy:Vertex normals set to",
        "does not support custom normals": "does not support custom normals",
        "Show Normals": "Show Normals"
    },
    'zh_CN': {
        "Vertex Normal Batch Setting Plugin": "顶点法相批量设置插件",
        "Apply Normals": "应用顶点法线",
        "LoongLy:No mesh objects selected": "LoongLy:没有被选中的物体",
        "LoongLy:Vertex normals set to": "LoongLy：法线已经设置为",
        "does not support custom normals": "不支持自定义法线",
        "Show Normals": "显示顶点法线"
    }
}

lang_code = 'en_US'

bl_info = {
    "name": "Set Vertex Normals",
    "author": "LoongLy Software",
    "version": (3, 0),
    "blender": (3, 5, 0),
    "location": "View3D > UI > Tool",
    "description": "Set vertex normals to a specified vector",
    "category": "Object",
}

exchanged_obj = {}


def detect_system_language():
    default_locale = locale.getdefaultlocale()
    if default_locale[0] in languages.keys():
        return default_locale[0]
    return "en_US"


#is_show_normal_vertex = False
#ori_tool_settings_normal_size = 0.1


"""async def reset_scene_tool_settings():
    asyncio.create_task(reset_scene_tool_settings_task())


async def reset_scene_tool_settings_task():
    global is_show_normal_vertex
    global ori_tool_settings_normal_size
    await asyncio.sleep(2)
    # 在3D视图叠加层中开启顶点法向显示
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.overlay.show_vertex_normals = is_show_normal_vertex
                    space.overlay.normals_length = ori_tool_settings_normal_size
                    break"""


class OBJECT_OT_ShowVertexNormals(Operator):
    bl_idname = "object.show_vertex_normals"
    bl_label = "Show Vertex Normals"

    # bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global lang_code
        # 获取目标法线向量
        target_normal = Vector(context.scene.target_normal).normalized()

        # 获取所有选中的网格物体
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if not selected_meshes:
            self.report({'ERROR'}, languages[lang_code]["LoongLy:No mesh objects selected"])
            return {'CANCELLED'}
        #global is_show_normal_vertex
        #global ori_tool_settings_normal_size
        # 在3D视图叠加层中开启顶点法向显示
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        #is_show_normal_vertex = space.overlay.show_vertex_normals
                        #ori_tool_settings_normal_size = space.overlay.normals_length
                        space.overlay.show_vertex_normals = True
                        space.overlay.normals_length = 0.5
                        break

        for obj in selected_meshes:
            # 以下代码段即使删除也不会对模型法线有影响，仅为了让在编辑模式时显示编辑后的法线，注意！第二次进入编辑模式将无法显示编辑后的法线
            # 因为blander的normal update机制会把法线更新为blander自己计算的法线，但是我们将不会再在该模型使用blander的法线而是normals里面的数据
            # 这个机制太坑了！我今天都搭载这上面了！！！！
            # 确保处于编辑模式
            if hex(id(obj)) in exchanged_obj.keys():
                bpy.ops.object.mode_set(mode='EDIT')


                mesh = bmesh.from_edit_mesh(obj.data)

                for v in mesh.verts:
                    v.normal = Vector(exchanged_obj[hex(id(obj))])

                bmesh.update_edit_mesh(obj.data)

                mesh.free()
                bpy.context.view_layer.update()

        return {'FINISHED'}


class OBJECT_OT_SetVertexNormals(Operator):
    bl_idname = "object.set_vertex_normals"
    bl_label = "Set Vertex Normals"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global lang_code
        # 获取目标法线向量
        target_normal = Vector(context.scene.target_normal).normalized()

        # 获取所有选中的网格物体
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if not selected_meshes:
            self.report({'ERROR'}, languages[lang_code]["LoongLy:No mesh objects selected"])
            return {'CANCELLED'}

        for obj in selected_meshes:
            obj_mode = obj.mode

            mesh = obj.data

            # 确保自定义法线数据存在
            if not hasattr(mesh, 'normals_split_custom_set'):
                self.report({'WARNING'},
                            f"Object '{obj.name}' " + languages[lang_code]["does not support custom normals"])
                continue

            bpy.ops.object.mode_set(mode='OBJECT')
            # 确保启用自定义法线支持
            if not hasattr(mesh, 'use_auto_smooth'):
                bpy.ops.object.shade_smooth()
            else:
                mesh.use_auto_smooth = True  # 4.2不支持
            # bpy.ops.object.shade_smooth()

            # 创建一个与loop数量相同的法线列表
            normals = [target_normal for loop in mesh.loops]

            # 设置自定义法线
            mesh.normals_split_custom_set(normals)

            # 更新网格以应用更改
            mesh.update()

            exchanged_obj[hex(id(obj))] = target_normal

            bpy.context.view_layer.update()
            bpy.ops.object.mode_set(mode=obj_mode)

            # bpy.ops.object.mode_set(mode=obj_mode)

        self.report({'INFO'}, languages[lang_code]["LoongLy:Vertex normals set to"] + f" {target_normal}")
        return {'FINISHED'}


class VIEW3D_PT_NormalSetter(Panel):
    bl_label = "Vertex Normal Batch Setting Plugin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        global lang_code
        layout = self.layout
        scene = context.scene

        # 输入向量框
        layout.prop(scene, "target_normal", text="normal")

        # 应用按钮
        layout.operator("object.set_vertex_normals", text=languages[lang_code]["Apply Normals"], icon='NORMALS_VERTEX')

        layout.operator("object.show_vertex_normals", text=languages[lang_code]["Show Normals"], icon='NORMALS_VERTEX')


def register():
    global lang_code
    lang_code = detect_system_language()
    bpy.utils.register_class(OBJECT_OT_SetVertexNormals)
    bpy.utils.register_class(OBJECT_OT_ShowVertexNormals)
    bpy.utils.register_class(VIEW3D_PT_NormalSetter)
    bpy.types.Scene.target_normal = FloatVectorProperty(
        name="Target Normal",
        description="Target normal vector for vertices",
        subtype='XYZ',
        default=(0.0, 0.0, 1.0),
        size=3
    )


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SetVertexNormals)
    bpy.utils.unregister_class(OBJECT_OT_ShowVertexNormals)
    bpy.utils.unregister_class(VIEW3D_PT_NormalSetter)
    exchanged_obj.clear()
    del bpy.types.Scene.target_normal


if __name__ == "__main__":
    register()

    # LZX-Pycharm2021.3-2025-05-22-001
