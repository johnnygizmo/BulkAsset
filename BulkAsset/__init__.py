import bpy

from .tag_add import *
from .tag_remove import *
from .move import *
from .author import *
from .description import *

bl_info = {
    "name": "Bulk Asset Tools",
    "author": "Johnny Matthews",
    "location": "Asset Viewer - Edit Menu",
    "version": (1, 1),
    "blender": (3, 4, 1),
    "description": "A set of tools for managing multiple assets at the same time",
    "doc_url": "",
    "category": "Assets"
}

classes = (
    AssetMoveOperator,
    AssetAuthorOperator,
    AssetDescriptionOperator,
    AssetTagAddOperator,
    AssetTagRemoveOperator
)

menus = (
    move_menu_func,
    author_menu_func,
    description_menu_func,
    tag_add_menu_func,
    tag_remove_menu_func
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    if hasattr(bpy.types, "ASSETBROWSER_MT_asset"):
        for menu in menus:
            bpy.types.ASSETBROWSER_MT_asset.append(menu)
    else:
        for menu in menus:
            bpy.types.ASSETBROWSER_MT_edit.append(menu)


def unregister():

    if hasattr(bpy.types, "ASSETBROWSER_MT_asset"):
        for menu in menus:
            bpy.types.ASSETBROWSER_MT_asset.remove(menu)
    else:
        for menu in menus:
            bpy.types.ASSETBROWSER_MT_edit.remove(menu)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
