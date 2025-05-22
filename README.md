![LoongLy Software](https://gitee.com/zixuan_long/Img/raw/master/LS3_LOW_PIX.png)
# 顶点法线批量设置插件

可以批量设置所选物体的顶点法线

支持blander版本：3.5-4.2

![](.\Img\before.png)

![](.\Img\after.png)

## 注意！
本插件在编辑模式下显示的顶点法线，并非真正作用于模型的法线。

当在 编辑模式 下使用本插件批量设置模型顶点法线时，Blender 仅在第一次进入编辑模式时正确显示实际作用于模型的顶点法线。

若再次进入编辑模式，Blender 将会显示其默认计算出的顶点法线，但此时实际作用于模型的顶点法线并不会被重置或改变。

而如果在 其他模式（如物体模式） 下使用本插件批量设置顶点法线后，再进入编辑模式查看，Blender 同样只会显示其默认计算的顶点法线，而非真正作用于模型的那些法线。

因此，请注意：

在编辑模式下所看到的顶点法线，可能与实际作用于模型的顶点法线并不一致。

(下面的gif展示了一个立方体因为其法向量被批量设置为（0,0,1），导致原本的亮面变成了暗面。并且编辑模式显示的顶点法线与实际不一样)



![warming](https://gitee.com/zixuan_long/Img/raw/master/VertexNormalBatchSettingPlugin.gif)

# Vertex Normal Batch Setting Plugin

You can batch set the vertex normals of the selected objects

Support：Blander V3.5-4.2

![](.\Img\before.png)

![](.\Img\after.png)

## Warming
The vertex normals displayed by this plugin in edit mode are not the normals that actually affect the model.

When using this plugin to batch set model vertex normals in editing mode, Blender only correctly displays the actual vertex normals acting on the model when entering editing mode for the first time.

If you enter editing mode again, Blender will display its default calculated vertex normals, but the actual vertex normals acting on the model will not be reset or changed.

If you use this plugin to batch set vertex normals in other modes (such as object mode) and then enter edit mode to view, Blender will only display its default calculated vertex normals, rather than the normals that actually affect the model.

Therefore, please note:

The vertex normals seen in editing mode may not be consistent with the vertex normals actually applied to the model.

(The following GIF shows a cube whose normal vector is batch set to (0,0,1), causing the originally bright surface to become dark, and the vertex normals displayed in edit mode are different from the actual ones.)

![warming](https://gitee.com/zixuan_long/Img/raw/master/VertexNormalBatchSettingPlugin.gif)

