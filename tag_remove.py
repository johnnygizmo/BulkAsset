import bpy
import os
from .utilities import *


def tag_main(self, context):
    directory = get_catalog_directory(context)
    commands = {}
    ct = 0
    for f in bpy.context.selected_asset_files:
        if f.local_id == None:
            path = get_file_path(f.relative_path, directory)
            type_out = id_type_to_type_name(f.id_type)
            if path not in commands.keys():
                commands[path] = []
            commands[path].append(
                "d"+str(ct)+" = bpy.data."+type_out+"['"+f.name+"'].asset_data; d"+str(ct)+".tags.remove(d"+str(ct)+".tags[\'"+self.tag+"\']);")
            ct += 1
        else:
            f.local_id.asset_data.tags.remove(
                f.local_id.asset_data.tags[self.tag])
    run_commands(commands)
    bpy.ops.asset.library_refresh()


class AssetTagRemoveOperator(bpy.types.Operator):
    """Bulk Remove Tag"""
    bl_idname = "asset.bulk_remove_tag"
    bl_label = "Bulk Asset Remove Tag"
    bl_options = {'REGISTER', 'UNDO'}

    tag: bpy.props.StringProperty(name="Tag to Remove")

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


def tag_remove_menu_func(self, context):
    self.layout.operator(AssetTagRemoveOperator.bl_idname,
                         text=AssetTagRemoveOperator.bl_label)
