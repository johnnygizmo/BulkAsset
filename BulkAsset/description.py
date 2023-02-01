import bpy
import os
from .utilities import *


class AssetDescriptionOperator(bpy.types.Operator):
    """Bulk Change Description"""
    bl_idname = "asset.bulk_change_description"
    bl_label = "Bulk Asset Change Description"
    bl_options = {'REGISTER', 'UNDO'}

    description: bpy.props.StringProperty(name="New Description")
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
        self.description_main(context)
        return finalizeExecute(self, context)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        return {'FINISHED'}

    def description_main(self, context):
        directory = get_catalog_directory(context)
        commands = {}
        for f in bpy.context.selected_asset_files:
            if f.local_id == None:
                path = get_file_path(f.relative_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_data.description =\'"+self.description+"\';")
            else:
                f.local_id.asset_data.description = self.description


def description_menu_func(self, context):
    self.layout.operator(AssetDescriptionOperator.bl_idname,
                         text=AssetDescriptionOperator.bl_label)
