# Copyright (c) 2022 JMayh with MIT Licensce

import bpy
import struct
import json
import itertools

# --> CHANNEL_BIT_FLAG <--
# 1 >> 0 -> Position
# 1 >> 1 -> Normalx
# 1 >> 2 -> Tangent (Not implemented)
# 1 >> 3 -> Colour (Not implemented)
# 1 >> 4 -> Texture 0
# ...                  (Not implemented)
# 1 >> 13 -> Texture 7 (Not implemented)

def mesh_asset_from_blend(blend_mesh_name, dump_file_path, channel_bit_flag = 0b11001):
    mesh = bpy.data.meshes.get(blend_mesh_name)
    
    if mesh == None:
        raise ValueError(f'Mesh {blend_mesh_name} not in .blend file.')
    
    position = [vert.co.to_3d() for vert in mesh.vertices]
    normals = [vert.normal.to_3d() for vert in mesh.vertices]
    uvs = [[0, 0] for vert in mesh.uv_layers[0].data]

    float32_to_hex = lambda x: list(struct.pack('<f', x))
    
    data_size = []
    for vert in zip(position, normals, uvs):
        data_size.extend(itertools.chain(*[float32_to_hex(float) for float in itertools.chain(*vert)]))
    
    [index_buffer, byte_mask] = [[], (1 << 8) - 1]
    for poly in mesh.polygons:
        for vert in poly.vertices:
            index_buffer += [vert & byte_mask, vert >> 8]

    with open(dump_file_path, "w") as file:
        json.dump({"index_buffer": index_buffer, "data_size": data_size}, file)

print("Got run")
mesh_asset_from_blend("Test", "./_dump.json")

bpy.ops.wm.quit_blender()