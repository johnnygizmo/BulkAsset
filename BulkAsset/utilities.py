import bpy
import os
from .settings import *
from .compat import get_preferences

# UI Functions


def header_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.separator()
   


def tag_callback(self, context):
    global items1
    items1 = [] 
    
    items1.clear()
    tags = {}
    for f in bpy.context.selected_assets:
        for tag in f.metadata.tags:
            tags[tag.name] = True
    output = []
    i = 0
    for tag in tags.keys():
        output.append((tag, tag, "", i))
        i += 1
    items1 = output
    return items1


def item_callback(self, context):    
    global items
    items = [] 
    
    items.clear()
    
    
    output = [("", "Catalog", "", 0),
              ("00000000-0000-0000-0000-000000000000", "Unassigned", "", 0)]

    if bpy.context.space_data.params.asset_library_reference == "ALL":
        return [("", "Select a catalog other than 'All'", "", 0)]
    
    filepath_bytes = os.fsencode(context.space_data.params.directory)
    directory = filepath_bytes.decode('utf-8', "replace")
    
    # directory = context.space_data.params.directory    
    # d = str(directory).split('\'')
    
    # directory = d[1]
    cat = open(os.path.join(str(directory), "blender_assets.cats.txt"), encoding='utf-8')
    cats = cat.readlines()
    cat.close()
    # print(cats)
    
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
    # print('output:_yn_:',output)
    items=output
    return items


# Utility Functions

def get_catalog_directory(context):
    catalog_bytes = os.fsencode(context.space_data.params.catalog_id)
    catalog = catalog_bytes.decode('utf-8', "replace")
    
    filepath_bytes = os.fsencode(context.space_data.params.directory)
    directory = filepath_bytes.decode('utf-8', "replace")
    if directory == "b''":
        return ""
    # d = str(directory).split('\'')
    # return d[1]
    return str(directory)


def get_file_path(relative_path, directory):
    # Handle both forward and backward slashes for cross-platform support
    sep = "\\" if ".blend\\" in relative_path else "/"
    p = relative_path.split(".blend" + sep)
    p[0] = p[0] + ".blend"
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
        list = [bpy.app.binary_path]
        prefs = get_preferences()
        if prefs and prefs.background == True:
            list.append("-b")
        list.append(path)
        list.append("--python-expr")
        list.append(expr)
        subprocess.run(list)
    except:
        print("Error on the new Blender instance")
