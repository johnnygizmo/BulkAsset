import bpy
import os
from .utilities import *


def tag_main(self, context):
    if self.tag.strip() == "":
        return
    directory = get_catalog_directory(context)
    commands = {}
    for f in bpy.context.selected_asset_files:
        if f.local_id == None:
            path = get_file_path(f.relative_path, directory)
            type_out = id_type_to_type_name(f.id_type)
            if path not in commands.keys():
                commands[path] = []
            commands[path].append(
                "bpy.data."+type_out+"['"+f.name+"'].asset_data.tags.new(\'"+self.tag+"\',skip_if_exists=True);")
    run_commands(commands)


class AssetTagAddOperator(bpy.types.Operator):
    """Bulk Add Tag"""
    bl_idname = "asset.bulk_add_tag"
    bl_label = "Bulk Asset Add Tag"
    bl_options = {'REGISTER', 'UNDO'}

    tag: bpy.props.StringProperty(name="Tag to Add")

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'FILE_BROWSER' and space.browse_mode == 'ASSETS'

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        tag_main(self, context)
        return {'FINISHED'}


def tag_add_menu_func(self, context):
    self.layout.operator(AssetTagAddOperator.bl_idname,
                         text=AssetTagAddOperator.bl_label)
