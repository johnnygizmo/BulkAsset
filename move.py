import bpy
import os
from .utilities import *


def move_main(self, context):
    directory = get_catalog_directory(context)
    commands = {}
    for f in bpy.context.selected_asset_files:
        if f.local_id == None:
            path = get_file_path(f.relative_path, directory)
            type_out = id_type_to_type_name(f.id_type)
            if path not in commands.keys():
                commands[path] = []
            commands[path].append(
                "bpy.data."+type_out+"['"+f.name+"'].asset_data.catalog_id =\'"+self.catalog+"\';")
    run_commands(commands)


class AssetMoveOperator(bpy.types.Operator):
    """Move Assets to a Catalog"""
    bl_idname = "asset.bulk_asset_mover"
    bl_label = "Bulk Asset Mover"
    bl_options = {'REGISTER', 'UNDO'}

    catalog: bpy.props.EnumProperty(
        name="Destination Catalog", items=item_callback)

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'FILE_BROWSER' and space.browse_mode == 'ASSETS'

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        move_main(self, context)
        return {'FINISHED'}


def move_menu_func(self, context):
    self.layout.operator(AssetMoveOperator.bl_idname,
                         text=AssetMoveOperator.bl_label)
