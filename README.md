# render Layer Folders
setup automatically composite nodes to export render layers separately

### Description

The renderlayers, input nodes are created from renderlayers scene names. Then connected to one "output file" node with multiple input.
everything will be in a folder named "Layers" at the same level of the blend file (this is easily tweakable after, it is set by the base path of the output file node)
each render layer will be exported in a separate subfolder.

e.g:
for a renderlayer nammed 'background' image will be:
//Layers/background/background_0001.png

note that it will generate folders hierarchy at the moment you launch the operator (without render needed)
If you don't want that to happen, comment the line 52 of the script '*folder_gen(layer)*'.

---

### where ?

**panel version**  
The panel is located in properties > layers
<!--
**operator only version**  
For the "no pannel" version, as it's name states, you just have to search "Setup Render layers" in spacebar search menu.
Best if you don't want to overload your (already crowded) UI. ;).
-->
UI panel:  
![RLfolder panel](https://github.com/Pullusb/images_repo/raw/master/Blender_RLfolder_panel_mouse.png)

generated nodes:  
![RLfolder panel](https://github.com/Pullusb/images_repo/raw/master/Blender_RLfolder_nodetree.png)
