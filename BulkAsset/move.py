import bpy
import os
from .utilities import *
from .base_operator_class import BaseBulkOperator

class ASSET_OT_MoveOperator(BaseBulkOperator):
    """Move Assets to a Catalog"""
    bl_idname = "asset.bulk_asset_mover"
    bl_label = "Asset Mover"

    catalog: bpy.props.EnumProperty(
        name="Destination Catalog", items=item_callback)

    def main(self, context):
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_asset_files:
            if f.local_id == None:
                path = get_file_path(f.relative_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_data.catalog_id =\'"+self.catalog+"\';")
            else:
                f.local_id.asset_data.catalog_id = self.catalog


def ASSET_MT_move_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_MoveOperator.bl_idname,
                         text=ASSET_OT_MoveOperator.bl_label)
