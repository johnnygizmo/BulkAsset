import bpy
import os

from .base_operator_class import BaseBulkOperator
from .utilities import *


class ASSET_OT_LicenseOperator(BaseBulkOperator):
    """Bulk Change License"""
    bl_idname = "asset.bulk_change_license"
    bl_label = "Change License"

    license: bpy.props.StringProperty(name="New License")

    def main(self, context):
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_assets:
            if f.local_id == None:
                path = get_file_path(f.full_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_data.license =\'"+self.license+"\';")
            else:
                f.local_id.asset_data.license = self.license


def ASSET_MT_license_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_LicenseOperator.bl_idname,
                         text=ASSET_OT_LicenseOperator.bl_label)
