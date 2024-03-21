import bpy
import os

from .base_operator_class import BaseBulkOperator
from .utilities import *


class ASSET_OT_CopyrightOperator(BaseBulkOperator):
    """Bulk Change Copyright"""
    bl_idname = "asset.bulk_change_copyright"
    bl_label = "Change Copyright"

    copyright: bpy.props.StringProperty(name="New Copyright")

    def main(self, context):
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_assets:
            if f.local_id == None:
                path = get_file_path(f.full_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_data.copyright =\'"+self.copyright+"\';")
            else:
                f.local_id.asset_data.copyright = self.copyright


def ASSET_MT_copyright_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_CopyrightOperator.bl_idname,
                         text=ASSET_OT_CopyrightOperator.bl_label)
