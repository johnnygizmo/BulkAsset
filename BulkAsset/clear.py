import bpy
import os
from .utilities import *
from .base_operator_class import BaseBulkOperator

class ASSET_OT_ClearOperator(BaseBulkOperator):
    """Bulk Clear Asset"""
    bl_idname = "asset.bulk_clear_asset"
    bl_label = "Clear Asset Marking"

    def draw(self, context):
        num = len(bpy.context.selected_assets)
        self.layout.label(icon='ERROR', text="This will clear " +
                          str(num)+" assets with NO UNDO. ")
        self.layout.label(text="Press ESC to cancel")

    def main(self, context):
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_assets:
            if f.local_id == None:
                path = get_file_path(f.full_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_clear();")
            else:
                f.local_id.asset_clear()


def ASSET_MT_clear_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_ClearOperator.bl_idname,
                         text=ASSET_OT_ClearOperator.bl_label)
