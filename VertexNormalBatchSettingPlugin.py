import bpy
import bmesh
import locale

from bpy.props import FloatVectorProperty
from bpy.types import Operator, Panel
from mathutils import Vector

languages = {
    'en_US': {
         "Vertex Normal Batch Setting Plugin": "Vertex Normal Batch Setting Plugin",
        "Apply Normals": "Apply Normals",
        "LoongLy:No mesh objects selected":"LoongLy:No mesh objects selected",
        "LoongLy:Vertex normals set to":"LoongLy:Vertex normals set to"
    },
    'zh_CN': {
        "Vertex Normal Batch Setting Plugin": "顶点法相批量设置插件",
        "Apply Normals": "应用法线",
        "LoongLy:No mesh objects selected":"LoongLy:没有被选中的物体",
        "LoongLy:Vertex normals set to":"LoongLy：法线已经设置为"
    }
}

lang = 'en_US'

bl_info = {
    "name": "Set Vertex Normals",
    "author": "LoongLy Software",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > UI > Tool",
    "description": "Set vertex normals to a specified vector",
    "category": "Object",
}

def detect_system_language():
    default_locale = locale.getdefaultlocale()
    return default_locale[0]


class OBJECT_OT_SetVertexNormals(Operator):
    bl_idname = "object.set_vertex_normals"
    bl_label = "Set Vertex Normals"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global lang
        # 获取目标法线向量
        target_normal = Vector(context.scene.target_normal).normalized()
        
        # 获取所有选中的网格物体
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_meshes:
            self.report({'ERROR'}, languages[lang]["LoongLy:No mesh objects selected"])
            return {'CANCELLED'}

        for obj in selected_meshes:
            # 确保处于编辑模式
            obj_mode = obj.mode
            if obj.mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')

            mesh = bmesh.from_edit_mesh(obj.data)

            for v in mesh.verts:
                v.normal = target_normal

            bmesh.update_edit_mesh(obj.data)
            # bpy.ops.object.mode_set(mode=obj_mode)

        self.report({'INFO'}, languages[lang]["LoongLy:Vertex normals set to"]+f" {target_normal}")
        return {'FINISHED'}


class VIEW3D_PT_NormalSetter(Panel):
    bl_label = "Vertex Normal Batch Setting Plugin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        global lang
        layout = self.layout
        scene = context.scene
        
        # 输入向量框
        layout.prop(scene, "target_normal", text="normal")
        
        # 应用按钮
        layout.operator("object.set_vertex_normals", text=languages[lang]["Apply Normals"] , icon='NORMALS_VERTEX')


def register():
    global lang
    lang = detect_system_language()
    bpy.utils.register_class(OBJECT_OT_SetVertexNormals)
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
    bpy.utils.unregister_class(VIEW3D_PT_NormalSetter)
    del bpy.types.Scene.target_normal


if __name__ == "__main__":
    register()