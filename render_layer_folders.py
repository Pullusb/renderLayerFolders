bl_info = {
    "name": "Render Layers Folders",
    "description": "Setup render layers in node tree to output each render layer in separate folder",
    "author": "Samuel Bernou",
    "version": (0, 4, 1),
    "blender": (2, 77, 0),
    "location": "Properties > Render layers",
    "warning": "",
    "wiki_url": "",
    "category": "Node" }
    
# TODO handle OpenExrMultilayer images (layer slots)
# TODO handle passes

import bpy
import os


def folder_gen(layer):
    base = bpy.path.abspath('//')
    base = os.path.join(base, 'Layers')
    # if not os.path.exists(base):
    #         os.mkdir(base)

    layer_folder = os.path.join(base, layer)
    # if not os.path.exists(layer_folder):
    os.makedirs(layer_folder, exist_ok=True)
    print (layer, 'folder created')


def rl_node(context, layer, refloc, i):
    nodes = context.scene.node_tree.nodes

    rlnodes = [n for n in nodes if n.type == 'R_LAYERS']
    for rl in rlnodes:
        if rl.layer == layer:
            # rl.name = layer
            # rl.label = layer
            return rl

    rl = nodes.new(type='CompositorNodeRLayers')
    rl.name = layer
    rl.label = layer
    rl.layer = layer
    rl.location[1] = refloc[1] + (300 * i)

    return (rl)


def create_layer(context, layer, refloc, i, file_output_node):
    '''Create the layer slot'''
    folder_gen(layer)
    rl = rl_node(context, layer, refloc, i)
    layerpath = layer + '/' + layer + '_'
    
    slots = file_output_node.file_slots
    slot = slots.new(layerpath)
    
    links = context.scene.node_tree.links
    links.new(rl.outputs[0], file_output_node.inputs[layerpath])
    

class RLFolderGen(bpy.types.Operator):
    bl_idname = "render.setup_render_layer"
    bl_label = "Setup Render layers"
    bl_description = "Generate nodes and folder for render layer"
    bl_options = {"REGISTER"}
    
    def execute(self, context):
        scene = context.scene

        if scene.node_tree is None:
            scene.use_nodes = True

        nodes = scene.node_tree.nodes

        # # Input base
        # try:
        #     render_layer_node = nodes["Input"]
        # except KeyError:
        #     render_layer_node = nodes.new(type='CompositorNodeRLayers')
        #     render_layer_node.name = "Input"
        #     render_layer_node.label = "Input"
        
        # refloc = render_layer_node.location
        refloc = (0.0,0.0)

        # Output base
        try:
            file_output_node = nodes["Output RenderLayers"]
        except KeyError:
            file_output_node = nodes.new(type='CompositorNodeOutputFile')
            file_output_node.name = "Output RenderLayers"
            file_output_node.label = "Output RenderLayers"
            file_output_node.base_path = '//Layers/'

        file_output_node.location = (refloc[0] + 400, refloc[1])

        # Delete all inputs
        for file_slot in file_output_node.file_slots:
            file_output_node.file_slots.remove(file_output_node.inputs[file_slot.path])

        for i, rl in enumerate(scene.render.layers):
            create_layer(context, rl.name, refloc, i, file_output_node)

        # Reorder inputs
        for i in range(len(file_output_node.inputs)-1):
            print(len(file_output_node.inputs)-1, i)
            file_output_node.inputs.move(len(file_output_node.inputs)-1, i)
        # file_output_node.inputs.move(len(file_output_node.inputs)-1, 0)

        return {'FINISHED'}

        

def rl_folder_panel(self, context):
    """Panel of buttons in UI"""
    layout = self.layout
    layout.operator(RLFolderGen.bl_idname, text = "Setup layers output nodes", icon = 'NEWFOLDER')

#----REGISTER

def register():
    bpy.utils.register_module(__name__)
    bpy.types.RENDERLAYER_PT_layers.append(rl_folder_panel)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.RENDERLAYER_PT_layers.remove(rl_folder_panel)

if __name__ == "__main__":
    register()

