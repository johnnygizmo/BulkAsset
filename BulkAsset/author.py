import bpy
import os

from .base_operator_class import BaseBulkOperator
from .utilities import *


class ASSET_OT_AuthorOperator(BaseBulkOperator):
    """Bulk Change Author"""
    bl_idname = "asset.bulk_change_author"
    bl_label = "Change Author"

    author: bpy.props.StringProperty(name="New Author")

    def main(self, context):
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_assets:
            if f.local_id == None:
                path = get_file_path(f.full_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_data.author =\'"+self.author+"\';")
            else:
                f.local_id.asset_data.author = self.author


def ASSET_MT_author_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_AuthorOperator.bl_idname,
                         text=ASSET_OT_AuthorOperator.bl_label)
