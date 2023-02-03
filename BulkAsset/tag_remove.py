import bpy
import os
from .utilities import *
from .base_operator_class import BaseBulkOperator

class ASSET_OT_TagRemoveOperator(BaseBulkOperator):
    """Bulk Remove Tag"""
    bl_idname = "asset.bulk_remove_tag"
    bl_label = "Remove Tag"

    tag: bpy.props.EnumProperty(
        name="Tag to Remove", items=tag_callback)

    def main(self, context):
        directory = get_catalog_directory(context)
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


def ASSET_MT_tag_remove_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_TagRemoveOperator.bl_idname,
                         text=ASSET_OT_TagRemoveOperator.bl_label)
