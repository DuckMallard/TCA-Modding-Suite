import subprocess
import json
import UnityPy

completed_process = subprocess.run(["C:/Program Files/Blender Foundation/Blender 3.0/blender.exe", "/models/Triangle.blend", "--python", "/src/mesh_builder_blender.py", "-b"])
completed_process.check_returncode()

ASSET_FILE_PATH = "C:/Program Files (x86)/Steam/Backups/Tiny Combat Arena Dev/Arena_Data/resources.assets"
ASSET_PATH_ID = 225

with open("./_dump.json", "r") as file:
    [index_buffer, data_size] = json.load(file).values()

env = UnityPy.load(ASSET_FILE_PATH)

mesh_obj = [obj for obj in env.objects if obj.path_id == 225][0]
mesh_tree = mesh_obj.read_typetree()

mesh_tree["m_VertexData"]["m_DataSize"] = bytes(data_size)
mesh_tree["m_VertexData"]["m_VertexCount"] = int(len(data_size) / 32)
mesh_tree["m_IndexBuffer"] = index_buffer
mesh_tree["m_SubMeshes"][0]["indexCount"] = int(len(index_buffer) / 2)
mesh_tree["m_SubMeshes"][0]["vertexCount"] = int(len(data_size) / 32)
mesh_tree["m_SubMeshes"][0]["localAABB"]["m_Center"] = {"x": 0, "y": 0, "z": 0}
mesh_tree["m_SubMeshes"][0]["localAABB"]["m_Extent"] = {"x": 100, "y": 100, "z": 100}
for i in range(14):
    mesh_tree["m_VertexData"]["m_Channels"][i] = {"stream": 0, "offset": 0, "format": 0, "dimension": 0}
mesh_tree["m_VertexData"]["m_Channels"][0] = {"stream": 0, "offset": 0, "format": 0, "dimension": 3}
mesh_tree["m_VertexData"]["m_Channels"][1] = {"stream": 0, "offset": 12, "format": 0, "dimension": 3}
mesh_tree["m_VertexData"]["m_Channels"][4] = {"stream": 0, "offset": 24, "format": 0, "dimension": 2}

mesh_obj.save_typetree(mesh_tree)

with open(ASSET_FILE_PATH, "wb") as file:
    file.write(env.file.save())