import bpy
import os


class BaseBulkOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'INTERNAL'}
    commands = {}
    command_count = 0
    _timer = None

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'FILE_BROWSER' and context.space_data.browse_mode == 'ASSETS'

    def modal(self, context, event: bpy.types.Event):
        return handleModal(self, context, event)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def cancel(self, context):
        wm = context.window_manager
        if self._timer != None:
            wm.event_timer_remove(self._timer)
        return None

    def main(self, context):
        pass

    def execute(self, context):
        self.main(context)
        return finalizeExecute(self, context)


def header_menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.separator()
    self.layout.label(text="=== Bulk Asset Tools ===")


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


def run_commands(commands):
    import subprocess
    for path in commands.keys():
        commandlist = "".join(commands[path])
        try:
            expr = "import bpy; "+commandlist + \
                " bpy.ops.wm.save_mainfile(); bpy.ops.wm.quit_blender();"
            subprocess.run([bpy.app.binary_path, "-b",
                           path, "--python-expr", expr])
        except:
            print("Error on the new Blender instance")


def finalizeExecute(self, context):
    wm = context.window_manager
    self.command_count = len(self.commands.keys())
    wm.progress_begin(0, self.command_count)
    self._timer = wm.event_timer_add(0.25, window=context.window)
    wm.modal_handler_add(self)
    return {'RUNNING_MODAL'}


def handleModal(self, context: bpy.types.Context, event: bpy.types.Event):
    left = self.command_count-len(self.commands.keys())
    context.window_manager.progress_update(left)

    if event.type in {'RIGHTMOUSE', 'ESC'}:
        bpy.ops.asset.library_refresh()
        context.window_manager.progress_end()
        self.cancel(context)
        return {'CANCELLED'}

    if event.type == 'TIMER':
        if len(self.commands.keys()) > 0:
            (path, commands) = self.commands.popitem()
            run_command(path=path, commands=commands)
            return {'RUNNING_MODAL'}
        bpy.ops.asset.library_refresh()
        context.window_manager.progress_end()
        return {'FINISHED'}

    return {'PASS_THROUGH'}


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