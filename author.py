import bpy
import os
from .utilities import *


class AssetAuthorOperator(bpy.types.Operator):
    """Bulk Change Author"""
    bl_idname = "asset.bulk_change_author"
    bl_label = "Bulk Asset Change Author"
    bl_options = {'REGISTER'}

    author: bpy.props.StringProperty(name="New Author")
    commands = {}
    command_count = 0
    _timer = None

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'FILE_BROWSER' and context.space_data.browse_mode == 'ASSETS'

    def modal(self, context, event: bpy.types.Event):
        return handleModal(self, context, event)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        self.author_main(context)
        return finalizeExecute(self, context)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        return {'FINISHED'}

    def author_main(self, context):
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_asset_files:
            if f.local_id == None:
                path = get_file_path(f.relative_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_data.author =\'"+self.author+"\';")
            else:
                f.local_id.asset_data.author = self.author


def author_menu_func(self, context):
    self.layout.operator(AssetAuthorOperator.bl_idname,
                         text=AssetAuthorOperator.bl_label)
