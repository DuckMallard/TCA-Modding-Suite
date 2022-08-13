#"C:\Program Files\Blender Foundation\Blender 3.0\blender.exe" "\models\Triangle.blend" --python mesh_builder.py
import bpy
import mathutils
import struct
import json

triangle = bpy.data.meshes[0]
vertices = [vert.co.to_3d() for vert in triangle.vertices]
normals = [vert.normal.to_3d() for vert in triangle.vertices]
tangents = [mathutils.Vector((*loop.tangent, loop.bitangent_sign)) for loop in triangle.loops]
uvs = [vert.uv for vert in triangle.uv_layers[0].data]
indexes = [vert for vert in triangle.polygons[0].vertices]

def float32toHex(value):
    hx = hex(struct.unpack('>I', struct.pack('<f', value))[0])
    return hx

hxArr = []
for i in range(len(vertices)):
    hxArr += [float32toHex(val) for val in vertices[i]]
    hxArr += [float32toHex(val) for val in normals[i]]
    #hxArr += [float32toHex(val) for val in tangents[i]]
    hxArr += [float32toHex(val) for val in uvs[i]]

m_DataSize = []
for hx in [_hx.removeprefix("0x").rjust(8, '0') for _hx in hxArr]:
    m_DataSize += [int(val, 16) for val in [hx[0:2], hx[2:4], hx[4:6], hx[6:8]]]

print(m_DataSize)
print(len(m_DataSize))
print(indexes)
bpy.ops.wm.quit_blender()

with open("./dumps/data.json", "w") as file:
    json.dump(m_DataSize, file)