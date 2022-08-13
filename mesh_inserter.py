import UnityPy
import json

src = "../Arena_Data/resources_old.assets"

data_size = None
with open("./dumps/data.json", "r") as file:
    data_size = json.load(file)
#data_size = [hex(data) for data in data_size]

env = UnityPy.load(src)
mesh_obj = [obj for obj in env.objects if obj.path_id == 225][0]
mesh_tree = mesh_obj.read_typetree()

mesh_tree["m_VertexData"]["m_DataSize"] = bytes(data_size)
mesh_tree["m_VertexData"]["m_VertexCount"] = 3
mesh_tree["m_IndexBuffer"] = [1, 0, 2, 0, 0, 0]
mesh_tree["m_SubMeshes"][0]["indexCount"] = 3
mesh_tree["m_SubMeshes"][0]["vertexCount"] = 3
mesh_tree["m_SubMeshes"][0]["localAABB"]["m_Center"] = {"x": 0, "y": 0, "z": 0}
mesh_tree["m_SubMeshes"][0]["localAABB"]["m_Extent"] = {"x": 1, "y": 0, "z": 1}
for i in range(14):
    mesh_tree["m_VertexData"]["m_Channels"][i] = {"stream": 0, "offset": 0, "format": 0, "dimension": 0}
mesh_tree["m_VertexData"]["m_Channels"][0] = {"stream": 0, "offset": 0, "format": 0, "dimension": 3}
mesh_tree["m_VertexData"]["m_Channels"][1] = {"stream": 0, "offset": 12, "format": 0, "dimension": 3}
mesh_tree["m_VertexData"]["m_Channels"][4] = {"stream": 0, "offset": 24, "format": 0, "dimension": 2}
mesh_obj.save_typetree(mesh_tree)

with open("../Arena_Data/resources.assets", "wb") as file:
    file.write(env.file.save())

