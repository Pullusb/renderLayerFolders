bl_info = {
    "name": "RenderLayersFolders",
    "description": "Setup renderLayers in node tree to output each renderlayers in separate folder",
    "author": "Samuel Bernou",
    "version": (0, 0, 1),
    "blender": (2, 77, 0),
    "location": "Properties > RenderLayers",
    "warning": "",
    "wiki_url": "",
    "category": "Node" }
    

import bpy
import os

C = bpy.context
scene = bpy.context.scene
nodes = scene.node_tree.nodes
links = scene.node_tree.links

def SetEditor():
    editorcheck = False
    for area in bpy.context.screen.areas :
        if area.type == 'NODE_EDITOR' :
            if area.spaces.active.tree_type != 'CompositorNodeTree':
                area.spaces.active.tree_type = 'CompositorNodeTree'
            editorcheck = True
    
    ##check use node 
    #bpy.context.scene.use_nodes = True



def FolderGen(layer):
    base = bpy.path.abspath('//')
    base = os.path.join(base, 'Layers')
    if not os.path.exists(base):
            os.mkdir(base)

    layerFolder = os.path.join(base, layer)
    if not os.path.exists(layerFolder):
        os.mkdir(layerFolder)
        print (layer, 'folder created')


def RLnode(layer, i):
    if CIn.layer == layer:
        return (CIn)
    try:
        rl = nodes[layer]
    except:
        rl = nodes.new(type='CompositorNodeRLayers')
        rl.name = layer
        rl.label = layer
        rl.layer = layer
        rl.location[1] = refloc[1] + (300 * i)

    return (rl)


def CreateLayer(layer, i):
    '''create the layer slot'''
    FolderGen(layer)
    rl = RLnode(layer, i)
    layerpath = layer + '/' + layer + '_'
    
    slots = FOut.file_slots
    try:
        SL = slots[layerpath]
        #print ('SLOT FOUND')
    except:
        #print ('SLOT created')
#        if len(slots) == 1 and slots[0].path == 'Image':
#            SL = slots[0]
#            SL.path = layerpath
        SL = slots.new(layerpath)
        if slots[0].path == 'Image':
            slots.remove(FOut.inputs['Image'])
    
    l = links.new(rl.outputs[0], FOut.inputs[layerpath])
            


class RLfolderGen(bpy.types.Operator):
    bl_idname = "render.setup_render_layer"
    bl_label = "Setup Render layers"
    bl_description = "generate nodes and folder for render layer"
    bl_options = {"REGISTER"}
    
    def execute(self, context):
        SetEditor()
        # Input base
        try:
            CIn = nodes["Input"]
        except:
            CIn = nodes.new(type='CompositorNodeRLayers')
            CIn.name = "Input"
            CIn.label = "Input"
        
        refloc = (0.0,0.0)
        refloc = CIn.location

        # Output base
        try:
            FOut  = nodes["Output RenderLayers"]
        except:
            FOut = nodes.new(type='CompositorNodeOutputFile')
            FOut.name = "Output RenderLayers"
            FOut.label = "Output RenderLayers"
            FOut.base_path = '//Layers/'

        FOut.location = (refloc[0] + 400, refloc[1] + 600)

        global CIn
        global FOut
        global refloc
        
        rlnodes = []
        for n in C.scene.node_tree.nodes :
            if n.type == 'R_LAYERS':
                rlnodes.append(n.name)

        for i, rl in enumerate(C.scene.render.layers):
            CreateLayer(rl.name, i)

        return {'FINISHED'}

        

def RLfolder_Panel(self, context):
    """Panel of buttons in UI"""
    layout = self.layout
    #split = layout.split(percentage=.4, align=True)
    #split.label("Renderlayer: ")
    #split.operator(RLfolderGen.bl_idname, text = "setup layers nodes", icon = 'FILE_FOLDER')
    layout.operator(RLfolderGen.bl_idname, text = "setup layers output nodes", icon = 'NEWFOLDER')


#----REGISTER

def register():
    bpy.utils.register_module(__name__)
    bpy.types.RENDERLAYER_PT_layers.append(RLfolder_Panel)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.RENDERLAYER_PT_layers.remove(RLfolder_Panel)

if __name__ == "__main__":
    register()

