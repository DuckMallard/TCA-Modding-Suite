# Copyright (c) 2022 JMayh with MIT Licensce
import struct
import json
import itertools
import sys
import bpy
import os

def mesh_asset_from_blend(blend_names: list[str]):

    byte_mask = (1 << 8) - 1
    to_bytes = lambda x: list(struct.pack('<f', x))

    output_dict: dict[str, dict] = dict()

    for blend_name in blend_names:
        
        if bpy.data.meshes.find(blend_name) != -1:
            output_dict[blend_name] = {"state": "MESH"}
            
            mesh = bpy.data.meshes.get(blend_name)
            
            position = [vert.co.to_3d() for vert in mesh.vertices]
            normals = [vert.normal.to_3d() for vert in mesh.vertices]
            uvs = [[0, 0] for vert in mesh.uv_layers[0].data]
            
            data_size: list[int] = []
            for vert in zip(position, normals, uvs):
                data_size.extend(itertools.chain(*[to_bytes(float) for float in itertools.chain(*vert)]))

            index_buffer = []
            for poly in mesh.polygons:
                for vert in poly.vertices:
                    index_buffer += [vert & byte_mask, vert >> 8]

            output_dict[blend_name]["data_size"] = data_size
            output_dict[blend_name]["index_buffer"] = index_buffer         

            if bpy.data.objects.find(blend_name) != -1:
                obj = bpy.data.objects.get(blend_name)
                output_dict[blend_name]["state"] = "MESH_OBJ"
                output_dict[blend_name]["location"] = [f for f in obj.location]
                output_dict[blend_name]["rotation"] = [f for f in obj.rotation_euler]

        elif (bpy.data.objects.find(blend_name) != -1) and (bpy.data.objects.get(blend_name).type == "EMPTY"):
            obj = bpy.data.objects.get(blend_name)
            output_dict[blend_name] = {"state": "EMPTY"}
            output_dict[blend_name]["location"] = [f for f in obj.location]
            output_dict[blend_name]["rotation"] = [f for f in obj.rotation_euler]
        
        else:
            output_dict[blend_name] = {"state": "FAIL"}

    with open(os.path.join(os.path.dirname(sys.argv[2]), "_output.json"), "w") as file:
        json.dump(output_dict, file)
  
mesh_asset_from_blend(sys.argv[6:])

bpy.ops.wm.quit_blender()
 