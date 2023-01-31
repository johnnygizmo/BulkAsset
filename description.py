import bpy
import os
from .utilities import item_callback

def description_main(self, context):
    space = context.space_data
    catalog = context.space_data.params.catalog_id
    directory = context.space_data.params.directory    
    d = str(directory).split('\'')
    directory = d[1]
    
    import subprocess
    commands = {}
    for f in bpy.context.selected_asset_files:
        if f.local_id == None:
            p = f.relative_path.split(".blend\\")
            p[0] = p[0]+".blend"
            
            
            type_out = f.id_type.lower()+"s"            
            if f.id_type == "NODETREE":
                type_out = "node_groups"
            
            path = os.path.join(directory,p[0])
            
            if path not in commands.keys():
                commands[path] = []
            
            commands[path].append("bpy.data."+type_out+"['"+f.name+"'].asset_data.description =\'"+self.description+"\';")
        
    for path in commands.keys():
        commandlist = "".join(commands[path])
        try:
            expr = "import bpy; "+commandlist+" bpy.ops.wm.save_mainfile(); bpy.ops.wm.quit_blender();"
            subprocess.run([bpy.app.binary_path, "-b", path, "--python-expr", expr])
        except:
           print("Error on the new Blender instance")

        bpy.ops.asset.library_refresh()
    
class AssetDescriptionOperator(bpy.types.Operator):
    """Bulk Change Description"""
    bl_idname = "asset.bulk_change_description"
    bl_label = "Bulk Asset Change Description"
    bl_options = {'REGISTER','UNDO'}
       
    description: bpy.props.StringProperty(name="Description")
    
    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'FILE_BROWSER' and space.browse_mode == 'ASSETS'

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        description_main(self, context)
        return {'FINISHED'}


def description_menu_func(self, context):
    self.layout.operator(AssetDescriptionOperator.bl_idname, text=AssetDescriptionOperator.bl_label)