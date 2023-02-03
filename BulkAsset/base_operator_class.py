import bpy
from .utilities import *
from .settings import max_threads


class BaseBulkOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'INTERNAL'}
    commands = {}
    command_count = 0
    _timer = None
    processes = []

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'FILE_BROWSER' and context.space_data.browse_mode == 'ASSETS'

    def modal(self, context, event: bpy.types.Event):
        return self.handleModal(context, event)

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
        return self.finalizeExecute(context)

    def finalizeExecute(self, context):
        wm = context.window_manager
        self.command_count = len(self.commands.keys())
        wm.progress_begin(0, self.command_count)
        self._timer = wm.event_timer_add(0.25, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def handleModal(self, context: bpy.types.Context, event: bpy.types.Event):
        left = self.command_count-len(self.commands.keys())
        context.window_manager.progress_update(round(left))

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.ops.asset.library_refresh()
            context.window_manager.progress_end()
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            import subprocess

            for proc in reversed(self.processes):
                if proc.poll() != None:
                    self.processes.remove(proc)

            if len(self.commands) == 0 and len(self.processes) == 0:
                bpy.ops.asset.library_refresh()
                context.window_manager.progress_end()
                return {'FINISHED'}

            if len(self.commands.keys()) > 0 and len(self.processes) < max_threads:
                (path, commands) = self.commands.popitem()

                commandlist = "".join(commands)
                try:
                    expr = "import bpy; "+commandlist + \
                        " bpy.ops.wm.save_mainfile(); bpy.ops.wm.quit_blender();"
                    self.processes.append(subprocess.Popen([bpy.app.binary_path, "-b",
                                                            path, "--python-expr", expr]))
                    print('launch proc')
                except:
                    print("Error on the new Blender instance")

            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}
