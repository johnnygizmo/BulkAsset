import bpy
import os
from .utilities import *
from .base_operator_class import BaseBulkOperator

class ASSET_OT_RenameOperator(BaseBulkOperator):
    """Bulk Rename"""
    bl_idname = "asset.bulk_rename"
    bl_label = "Rename"

    text: bpy.props.StringProperty(name="Text")
    mode: bpy.props.EnumProperty(items=[("PREFIX", "Prefix", "Add a Prefix", 0),
                                        ("SUFFIX", "Suffix", "Add a Suffix", 1),
                                        ("RENAME", "Rename", "Rename", 2),],
                                 default="RENAME")

    def main(self, context):
        directory = get_catalog_directory(context)
        for f in bpy.context.selected_assets:
            if f.local_id == None:
                path = get_file_path(f.full_path, directory)
                type_out = id_type_to_type_name(f.id_type)
                if path not in self.commands.keys():
                    self.commands[path] = []
                if (self.mode == "PREFIX"):
                    self.commands[path].append(
                        "bpy.data."+type_out+"['"+f.name+"'].name =\'"+self.text+"\'+bpy.data."+type_out+"['"+f.name+"'].name;")
                elif (self.mode == "SUFFIX"):
                    self.commands[path].append(
                        "bpy.data."+type_out+"['"+f.name+"'].name =bpy.data."+type_out+"['"+f.name+"'].name+\'"+self.text+"\';")
                elif (self.mode == "RENAME"):
                    self.commands[path].append(
                        "bpy.data."+type_out+"['"+f.name+"'].name =\'"+self.text+"\';")

            else:
                if (self.mode == "PREFIX"):
                    f.local_id.name = self.text+f.local_id.name
                elif (self.mode == "SUFFIX"):
                    f.local_id.name = f.local_id.name+self.text
                elif (self.mode == "RENAME"):
                    f.local_id.name = self.text


def ASSET_MT_rename_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ASSET_OT_RenameOperator.bl_idname,
                         text=ASSET_OT_RenameOperator.bl_label)
