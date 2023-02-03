import bpy
import os
from .utilities import *
from .base_operator_class import BaseBulkOperator

class ASSET_OT_DescriptionOperator(BaseBulkOperator):
    """Bulk Change Description"""
    bl_idname = "asset.bulk_change_description"
    bl_label = "Change Description"

    description: bpy.props.StringProperty(name="New Description")

    def main(self, context):
        directory = get_catalog_directory(context)
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


def ASSET_MT_description_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_DescriptionOperator.bl_idname,
                         text=ASSET_OT_DescriptionOperator.bl_label)
