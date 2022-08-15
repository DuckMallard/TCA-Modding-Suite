# Copyright (c) 2022 JMayh with MIT Licensce
import subprocess
import json
import UnityPy
import os

class Injector():
    def __init__(self, file_path: str):

        self.env = UnityPy.load(file_path)
        self.injections = []
        self.output_dict: dict[str, dict]
    
    def build(self, blend_file_path: str) -> bool:

        names = [injection[1] for injection in self.injections]
        completed_process = subprocess.run(["blender", "-b", blend_file_path, "--python", "scripts/Builder.py", "--", *names])
        if completed_process.returncode != 0:
            return False

        with open(os.path.join(os.path.dirname(blend_file_path), f'_output.json'), "r") as file:
            self.output_dict = json.load(file)

        for injection in self.injections:
            self.inject(*injection)

        return True


    def add_injection(self, transform_id: int, mesh_name: str, asset_id: int = None):

        self.injections.append([transform_id, mesh_name, asset_id])

    def inject(self, transform_id: int, mesh_name: str, asset_id: int = None):
        
        data: dict = self.output_dict[mesh_name]
        
        if data["state"] == "FAIL":
            return
        
        if data["state"] in ["MESH", "MESH_OBJ"] and (asset_id != None):
            data_size = data["data_size"]
            index_buffer = data["index_buffer"]

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
        
        if data["state"] in ["EMPTY", "MESH_OBJ"]:
            location = data["location"]
            rotation = data["rotation"]

            transform_obj = [obj for obj in self.env.objects if obj.path_id == transform_id][0]
            transform_tree = transform_obj.read_typetree()

            axis = ["x", "y", "z"]
            for i in range(3):
                transform_tree["m_LocalPosition"][axis[i]] = location[i] 
                transform_tree["m_LocalRotation"][axis[i]] = rotation[i] 

            transform_obj.save_typetree(transform_tree)

    def save(self, file_path_out: str):
        with open(file_path_out, "wb") as file:
            file.write(self.env.file.save())