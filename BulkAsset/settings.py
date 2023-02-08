import bpy


class BulkAssetToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    max_threads: bpy.props.IntProperty(name="Max Threads", default=10, min=1)
    background: bpy.props.BoolProperty(
        name="Run child processes in background mode", default=True)
    factory_default: bpy.props.BoolProperty(
        name="Use factory default startup", description="Run child processes in factory default mode", default=True)

    def draw(self, context):
        layout = self.layout
        layout.label(text='Bulk Asset Tools:')
        layout.prop(self, 'max_threads', expand=True)
        layout.prop(self, 'background', expand=True)
        layout.prop(self, 'factory_default', expand=True)
        layout.label(
            text='--Prevents other addons from loading in child processes.')
