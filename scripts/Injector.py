# Copyright (c) 2022 JMayh with MIT Licensce
import subprocess
import json
import UnityPy

class Injector():
    def __init__(self, file_path: str):
        self.env = UnityPy.load(file_path)
    
    def inject(self, asset_id: int, blend_file_path: str, mesh_name: str):
        completed_process = subprocess.run(["blender", blend_file_path, "--python", "Builder.py", "-b"])
        completed_process.check_returncode()

        print("Ran Builder")

        with open("./_dump.json", "r") as file:
            [index_buffer, data_size] = json.load(file).values()

        mesh_obj = [obj for obj in self.env.objects if obj.path_id == asset_id][0]
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

    def save(self, file_path_out: str):
        with open(file_path_out, "wb") as file:
            file.write(self.env.file.save())