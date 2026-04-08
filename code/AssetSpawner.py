bl_info = {
    "name": "Asset Spawner - Import GTAV Assets",
    "author": "Boold",
    "version": (1, 0),
    "blender": (5, 0, 1),
    "location": "View3D > Sidebar > Asset Spawner",
    "description": "Import GTAV Assets and apply Textures using Game files",
    "category": "Import-Export",
}

import bpy
import os
import threading

fs_loader_thread = None

def get_model_folder():
    return bpy.context.preferences.addons[__name__].preferences.model_folder

def get_textures_folder():
    return bpy.context.preferences.addons[__name__].preferences.textures_folder

class FS_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    model_folder: bpy.props.StringProperty(subtype='DIR_PATH', name="Assets Folder")
    textures_folder: bpy.props.StringProperty(subtype='DIR_PATH', name="Textures Folder")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_folder")
        layout.prop(self, "textures_folder")

class FS_Properties(bpy.types.PropertyGroup):
    search_query: bpy.props.StringProperty(name="Object Name")
    find_textures: bpy.props.BoolProperty(default=False, name="Find Textures")
    hide_collisions: bpy.props.BoolProperty(default=False, name="Hide Collisions")

class TextureLoaderThread(threading.Thread):
    def __init__(self, objs, textures_folder):
        super().__init__()
        self.objs = objs
        self.textures_folder = textures_folder
        self.results = []

    def run(self):
        for obj in self.objs:
            for mat_slot in obj.material_slots:
                mat = mat_slot.material
                if not mat or not mat.use_nodes:
                    continue
                for node in mat.node_tree.nodes:
                    if node.type != 'TEX_IMAGE' or not node.image:
                        continue
                    texture_name = node.image.name.split('.')[0].lower()
                    for f in os.listdir(self.textures_folder):
                        if f.lower().endswith(texture_name + ".dds"):
                            self.results.append((node, os.path.join(self.textures_folder, f)))
                            break

def apply_textures_from_thread(thread):
    for node, path in thread.results:
        node.image.filepath = path
        node.image.reload()

class FS_OT_import(bpy.types.Operator):
    bl_idname = "fs.import_file"
    bl_label = "Import Object"

    def execute(self, context):
        props = context.scene.fs_props
        model_folder = get_model_folder()
        textures_folder = get_textures_folder()

        if not model_folder or not os.path.exists(model_folder):
            self.report({'ERROR'}, "Assets folder not set or invalid")
            return {'CANCELLED'}

        query = props.search_query.lower()
        model_path = None
        for root, _, files in os.walk(model_folder):
            for f in files:
                if f.lower().startswith(query) and f.lower().endswith((".ydr", ".yft")):
                    model_path = os.path.join(root, f)
                    break
            if model_path:
                break

        if not model_path:
            self.report({'WARNING'}, "Object not found")
            return {'CANCELLED'}

        existing_objs = set(bpy.context.scene.objects)
        bpy.ops.sollumz.import_assets(
            directory=os.path.dirname(model_path),
            files=[{"name": os.path.basename(model_path)}]
        )

        new_objs = set(bpy.context.scene.objects) - existing_objs
        imported_objs = [obj for obj in new_objs if obj.type == 'MESH']

        if props.find_textures and textures_folder and os.path.exists(textures_folder):
            self.start_texture_thread(imported_objs, textures_folder)

        if props.hide_collisions:
            def hide_collisions_timer():
                for obj in imported_objs:
                    if obj.name.lower().endswith(".col") or obj.name.lower().startswith("bound box"):
                        obj.hide_set(True)
                        obj.hide_render = True
                    for child in obj.children_recursive:
                        if child.name.lower().endswith(".col") or child.name.lower().startswith("bound box"):
                            child.hide_set(True)
                            child.hide_render = True
                return None
            bpy.app.timers.register(hide_collisions_timer)

        return {'FINISHED'}

    def start_texture_thread(self, imported_objs, textures_folder):
        global fs_loader_thread
        if not imported_objs:
            return
        fs_loader_thread = TextureLoaderThread(imported_objs, textures_folder)
        fs_loader_thread.start()

        def check_thread():
            global fs_loader_thread
            if fs_loader_thread is None:
                return None
            if not fs_loader_thread.is_alive():
                apply_textures_from_thread(fs_loader_thread)
                fs_loader_thread = None
                return None
            return 0.1
        bpy.app.timers.register(check_thread)

class FS_OT_open_preferences(bpy.types.Operator):
    bl_idname = "fs.open_preferences"
    bl_label = "Open Addon Preferences"

    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        self.report({'INFO'}, "Go to Add-ons > Search for 'Asset Spawner - Import GTAV Assets' to set folders")
        return {'FINISHED'}

class FS_PT_panel(bpy.types.Panel):
    bl_label = "Asset Spawner"
    bl_idname = "FS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Asset Spawner'

    def draw(self, context):
        layout = self.layout
        prefs = bpy.context.preferences.addons[__name__].preferences
        props = context.scene.fs_props

        if not prefs.model_folder or not os.path.exists(prefs.model_folder):
            layout.label(text="⚠ Assets folder is required!", icon='ERROR')
            layout.operator("fs.open_preferences", icon='PREFERENCES')
            return

        layout.prop(props, "search_query")
        textures_folder = get_textures_folder()
        if textures_folder and os.path.exists(textures_folder):
            layout.prop(props, "find_textures")
        layout.prop(props, "hide_collisions")
        layout.operator("fs.import_file", icon='IMPORT')

classes = [FS_Preferences, FS_Properties, FS_OT_import, FS_PT_panel, FS_OT_open_preferences]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.fs_props = bpy.props.PointerProperty(type=FS_Properties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.fs_props

if __name__ == "__main__":
    register()