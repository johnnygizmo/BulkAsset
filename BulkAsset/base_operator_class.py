import bpy
import subprocess
import logging
from typing import Dict, List, Tuple, Optional

# Configure logging
logger = logging.getLogger(__name__)


class BaseBulkOperator(bpy.types.Operator):
    """Base operator class for bulk asset operations in Blender."""
    bl_options = {'REGISTER', 'INTERNAL'}
    
    # Configuration constants
    TIMER_INTERVAL = 0.25
    SUBPROCESS_SLEEP = 0.5
    
    # Class variables
    commands: Dict[str, List[str]] = {}
    command_count: int = 0
    _timer: Optional[bpy.types.Timer] = None
    processes: List[subprocess.Popen] = []

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """Check if operator can run in current context."""
        return (context.space_data.type == 'FILE_BROWSER' and 
                context.space_data.browse_mode == 'ASSETS')

    def modal(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """Handle modal events."""
        return self.handleModal(context, event)

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """Invoke the operator."""
        return context.window_manager.invoke_props_dialog(self)

    def cancel(self, context: bpy.types.Context) -> None:
        """Cancel the operator and clean up resources."""
        wm = context.window_manager
        if self._timer is not None:
            wm.event_timer_remove(self._timer)
            self._timer = None

    def main(self, context: bpy.types.Context) -> None:
        """Override this method to implement operator logic."""
        pass

    def execute(self, context: bpy.types.Context) -> set:
        """Execute the operator."""
        self.main(context)
        return self.finalizeExecute(context)

    def finalizeExecute(self, context: bpy.types.Context) -> set:
        """Finalize execution and set up modal handler."""
        wm = context.window_manager
        self.command_count = len(self.commands)
        wm.progress_begin(0, self.command_count)
        self._timer = wm.event_timer_add(self.TIMER_INTERVAL, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def handleModal(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """Handle modal events for background process management."""
        left = self.command_count - len(self.commands)
        context.window_manager.progress_update(round(left))

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.ops.asset.library_refresh()
            context.window_manager.progress_end()
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # Clean up finished processes
            self.processes = [proc for proc in self.processes if proc.poll() is None]

            if len(self.commands) == 0 and len(self.processes) == 0:
                bpy.ops.asset.library_refresh()
                context.window_manager.progress_end()
                return {'FINISHED'}

            # Get addon preferences
            prefs = bpy.context.preferences.addons[__package__].preferences
            max_threads = prefs.max_threads
            
            if self.commands and len(self.processes) < max_threads:
                path, commands = self.commands.popitem()
                self._execute_subprocess(path, commands, prefs)
            
            return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}
    
    def _execute_subprocess(self, path: str, commands: List[str], prefs) -> None:
        """Execute a subprocess with the given commands."""
        commandlist = "".join(commands)
        try:
            expr = (
                f"import bpy; import time; {commandlist} "
                f"time.sleep({self.SUBPROCESS_SLEEP});bpy.ops.wm.save_mainfile(); "
                f"time.sleep({self.SUBPROCESS_SLEEP});bpy.ops.wm.quit_blender();"
            )

            args = [bpy.app.binary_path]
            if prefs.factory_default:
                args.append("--factory-startup")
            if prefs.background:
                args.append("-b")
            else:
                args.append("--no-window-focus")
            args.extend([path, "--python-expr", expr, "--"])
            
            process = subprocess.Popen(args)
            self.processes.append(process)
        except Exception as e:
            logger.exception(f"Failed to execute subprocess for {path}: {e}")
