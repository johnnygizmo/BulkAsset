import bpy
import os
from .utilities import *


def author_main(self, context):
    directory = get_catalog_directory(context)
    commands = {}
    for f in bpy.context.selected_asset_files:
        if f.local_id == None:
            path = get_file_path(f.relative_path, directory)
            type_out = id_type_to_type_name(f.id_type)
            if path not in commands.keys():
                commands[path] = []
            commands[path].append(
                "bpy.data."+type_out+"['"+f.name+"'].asset_data.author =\'"+self.author+"\';")
    run_commands(commands)


class AssetAuthorOperator(bpy.types.Operator):
    """Bulk Change Author"""
    bl_idname = "asset.bulk_change_author"
    bl_label = "Bulk Asset Change Author"
    bl_options = {'REGISTER', 'UNDO'}

    author: bpy.props.StringProperty(name="New Author")

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'FILE_BROWSER' and space.browse_mode == 'ASSETS'

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        author_main(self, context)
        return {'FINISHED'}


def author_menu_func(self, context):
    self.layout.operator(AssetAuthorOperator.bl_idname,
                         text=AssetAuthorOperator.bl_label)
