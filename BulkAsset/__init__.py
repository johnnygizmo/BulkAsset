import bpy
import bpy.types
from .tag_copy import *
from .rename import *
from .tag_add import *
from .tag_remove import *
from .move import *
from .author import *
from .description import *
from .clear import *
from .copyright import *
from .license import *
from .utilities import header_menu_func
from .settings import *

bl_info = {
    "name": "Bulk Asset Tools",
    "author": "Johnny Matthews",
    "location": "Asset Viewer - Right Click Menu",
    "version": (1, 7),
    "blender": (4, 0, 1),
    "description": "A set of tools for managing multiple assets at the same time",
    "doc_url": "",
    "category": "Assets"
}

classes = (
    BulkAssetToolsPreferences,
    ASSET_OT_MoveOperator,
    ASSET_OT_AuthorOperator,
    ASSET_OT_DescriptionOperator,
    ASSET_OT_TagAddOperator,
    ASSET_OT_TagCopyOperator,
    ASSET_OT_TagRemoveOperator,
    ASSET_OT_RenameOperator,
    ASSET_OT_ClearOperator,
    ASSET_OT_LicenseOperator,
    ASSET_OT_CopyrightOperator
)

menus = (
    ASSET_MT_move_menu_func,
    ASSET_MT_author_menu_func,
    ASSET_MT_license_menu_func,
    ASSET_MT_copyright_menu_func,
    ASSET_MT_description_menu_func,
    ASSET_MT_tag_add_menu_func,
    ASSET_MT_tag_copy_menu_func,
    ASSET_MT_tag_remove_menu_func,
    ASSET_MT_rename_menu_func,
    ASSET_MT_clear_menu_func
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.ASSETBROWSER_MT_context_menu.append(header_menu_func)
    if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
        bpy.types.ASSETBROWSER_MT_asset.append(header_menu_func)
    elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
        bpy.types.ASSETBROWSER_MT_edit.append(header_menu_func)
        

    for menu in menus:
        if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
            bpy.types.ASSETBROWSER_MT_asset.append(menu)
        elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
            bpy.types.ASSETBROWSER_MT_edit.append(menu)
        bpy.types.ASSETBROWSER_MT_context_menu.append(menu)



def unregister():
    bpy.types.ASSETBROWSER_MT_context_menu.remove(header_menu_func)

    
    #if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
    bpy.types.ASSETBROWSER_MT_asset.remove(header_menu_func)
    #elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
    #    bpy.types.ASSETBROWSER_MT_edit.remove(header_menu_func)

    for menu in menus:
        #if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
        bpy.types.ASSETBROWSER_MT_asset.remove(menu)
        #elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
        #bpy.types.ASSETBROWSER_MT_edit.remove(menu)        
        bpy.types.ASSETBROWSER_MT_context_menu.remove(menu)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
