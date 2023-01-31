import bpy
import os
from .move import *
from .author import *
from .description import *

bl_info = {
    "name": "Asset Bulk Tools",
    "author": "Johnny Matthews",
    "location": "Asset Viewer - Edit/Asset Menu",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "description": "A set of tools for managing multiple assets",
    "doc_url": "",
    "category": "Assets"
}

classes = (
    AssetMoveOperator,
    AssetAuthorOperator,
    AssetDescriptionOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    if hasattr(bpy.types, "ASSETBROWSER_MT_asset"):
        bpy.types.ASSETBROWSER_MT_asset.append(move_menu_func)
        bpy.types.ASSETBROWSER_MT_asset.append(author_menu_func)
        bpy.types.ASSETBROWSER_MT_asset.append(description_menu_func)
    else:
        bpy.types.ASSETBROWSER_MT_edit.append(move_menu_func)
        bpy.types.ASSETBROWSER_MT_edit.append(author_menu_func)
        bpy.types.ASSETBROWSER_MT_edit.append(description_menu_func)
        

def unregister():
    if hasattr(bpy.types, "ASSETBROWSER_MT_asset"):
        bpy.types.ASSETBROWSER_MT_asset.remove(move_menu_func)
        bpy.types.ASSETBROWSER_MT_asset.remove(author_menu_func)
        bpy.types.ASSETBROWSER_MT_asset.remove(description_menu_func)
    else:
        bpy.types.ASSETBROWSER_MT_edit.remove(move_menu_func)
        bpy.types.ASSETBROWSER_MT_edit.remove(author_menu_func)
        bpy.types.ASSETBROWSER_MT_edit.remove(description_menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
