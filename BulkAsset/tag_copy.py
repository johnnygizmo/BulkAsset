import bpy
import os
from .utilities import *
from .base_operator_class import BaseBulkOperator

class ASSET_OT_TagCopyOperator(BaseBulkOperator):
    """Bulk Copy Tag"""
    bl_idname = "asset.bulk_copy_tag"
    bl_label = "Copy Tag"

    tag: bpy.props.EnumProperty(
        name="Tag to Copy", items=tag_callback)

    def main(self, context):
        if self.tag.strip() == "":
            return
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_asset_files:
            if f.local_id == None:
                path = get_file_path(f.relative_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                self.commands[path].append(
                    "bpy.data."+type_out+"['"+f.name+"'].asset_data.tags.new(\'"+self.tag+"\',skip_if_exists=True);")
            else:
                f.local_id.asset_data.tags.new(self.tag, skip_if_exists=True)


def ASSET_MT_tag_copy_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_TagCopyOperator.bl_idname,
                         text=ASSET_OT_TagCopyOperator.bl_label)
