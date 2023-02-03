import bpy
import os


## UI Functions

def header_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.separator()
    self.layout.label(text="=== Bulk Asset Tools ===")

def tag_callback(self, context):
    tags = {}
    for f in bpy.context.selected_asset_files:
        for tag in f.asset_data.tags:
            tags[tag.name] = True
    output = []
    i = 0
    for tag in tags.keys():
        output.append((tag, tag, "", i))
        i += 1
    return output


def item_callback(self, context):
    directory = context.space_data.params.directory
    d = str(directory).split('\'')
    directory = d[1]
    cat = open(os.path.join(str(directory), "blender_assets.cats.txt"))
    cats = cat.readlines()
    cat.close()

    output = [("", "Catalog", "", 0),
              ("00000000-0000-0000-0000-000000000000", "Unassigned", "", 0)]
    i = 1
    for line in cats:
        if line[0:1] == "#":
            continue
        if line.strip() == "":
            continue
        if line[0:7] == "VERSION":
            continue
        data = line.split(":")
        output.append((data[0], data[1], "", i))
        i += 1
    return output


## Utility Functions

def get_catalog_directory(context):
    catalog = context.space_data.params.catalog_id
    directory = context.space_data.params.directory
    if directory == "b''":
        return ""
    d = str(directory).split('\'')
    return d[1]

def get_file_path(relative_path, directory):
    p = relative_path.split(".blend\\")
    p[0] = p[0]+".blend"
    return os.path.join(directory, p[0])

def id_type_to_type_name(id_type):
    type_out = id_type.lower()+"s"
    if id_type == "NODETREE":
        type_out = "node_groups"
    return type_out

def run_command(path, commands):
    import subprocess
    commandlist = "".join(commands)
    try:
        expr = "import bpy; "+commandlist + \
            " bpy.ops.wm.save_mainfile(); bpy.ops.wm.quit_blender();"
        subprocess.run([bpy.app.binary_path, "-b",
                        path, "--python-expr", expr])
    except:
        print("Error on the new Blender instance")
