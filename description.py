import bpy
import os
from .utilities import *


def description_main(self, context):
    directory = get_catalog_directory(context)
    commands = {}
    for f in bpy.context.selected_asset_files:
        if f.local_id == None:
            path = get_file_path(f.relative_path, directory)
            type_out = id_type_to_type_name(f.id_type)
            if path not in commands.keys():
                commands[path] = []
            commands[path].append(
                "bpy.data."+type_out+"['"+f.name+"'].asset_data.description =\'"+self.description+"\';")
        else:
            f.local_id.asset_data.description = self.description
    run_commands(commands)
    bpy.ops.asset.library_refresh()


class AssetDescriptionOperator(bpy.types.Operator):
    """Bulk Change Description"""
    bl_idname = "asset.bulk_change_description"
    bl_label = "Bulk Asset Change Description"
    bl_options = {'REGISTER', 'UNDO'}

    description: bpy.props.StringProperty(name="New Description")

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'FILE_BROWSER' and space.browse_mode == 'ASSETS'

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        description_main(self, context)
        return {'FINISHED'}


def description_menu_func(self, context):
    self.layout.operator(AssetDescriptionOperator.bl_idname,
                         text=AssetDescriptionOperator.bl_label)
