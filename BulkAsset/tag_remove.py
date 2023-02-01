import bpy
import os
from .utilities import *


class AssetTagRemoveOperator(bpy.types.Operator):
    """Bulk Remove Tag"""
    bl_idname = "asset.bulk_remove_tag"
    bl_label = "Bulk Asset Remove Tag"
    bl_options = {'REGISTER', 'UNDO'}

    tag: bpy.props.StringProperty(name="Tag to Remove")
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
        self.tag_main(context)
        return finalizeExecute(self, context)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        return {'FINISHED'}

    def tag_main(self, context):
        directory = get_catalog_directory(context)
        commands = {}
        ct = 0
        for f in bpy.context.selected_asset_files:
            if f.local_id == None:
                path = get_file_path(f.relative_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "d"+str(ct)+" = bpy.data."+type_out+"['"+f.name+"'].asset_data; d"+str(ct)+".tags.remove(d"+str(ct)+".tags[\'"+self.tag+"\']);")
                ct += 1
            else:
                f.local_id.asset_data.tags.remove(
                    f.local_id.asset_data.tags[self.tag])


def tag_remove_menu_func(self, context):
    self.layout.operator(AssetTagRemoveOperator.bl_idname,
                         text=AssetTagRemoveOperator.bl_label)
