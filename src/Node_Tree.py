import UnityPy
from Node import Node

class Node_Tree():
    def __init__(self, src: str):
        self.env: UnityPy.environment = UnityPy.load(src)

        self.obj_dict: dict[int, UnityPy.environment.ObjectReader] = dict()
        for obj in self.env.objects:
            self.obj_dict[obj.path_id] = obj

        transforms: list[UnityPy.environment.ObjectReader]
        transforms = [obj for obj in self.env.objects if obj.type.name == "Transform"]

        transform_map: dict[int, int] = dict()
        for trans in transforms:
            transform_map[trans.path_id] = trans.read_typetree()["m_Father"]["m_PathID"]

        self.nodes: list[Node] = [Node(0)]
        self.cache: dict[int, int] = {0: 0}

        for [id, parent_id] in transform_map.items():
            if id not in self.cache.keys(): # Add current child if need
                self.cache[id] = len(self.nodes) # Add their id to cache
                self.nodes.append(Node(id)) # Create their node

            if parent_id not in self.cache.keys(): # Add child parent if needed
                self.cache[parent_id] = len(self.nodes) # Add their parent's id to cache
                self.nodes.append(Node(parent_id)) # Create their parent's node

            child_node = self.nodes[self.cache[id]]
            parent_node = self.nodes[self.cache[parent_id]]
            # It is the child job to setup the parent-child relation ship for themselves
            child_node.set_parent(parent_node) # Set their parent
            parent_node.add_child(child_node) # Set their parents child as themself

            child_node.game_object_id = self.obj_dict[id].read_typetree()["m_GameObject"]["m_PathID"] # Add child's gameobject id
            child_node.game_object_name = self.obj_dict[child_node.game_object_id].read_typetree()["m_Name"] # Add child's gameobject name

        for [id, obj] in self.obj_dict.items():
            if obj.type.name == "MeshFilter":
                tree: dict = obj.read_typetree()
                game_object_id: int = tree["m_GameObject"]["m_PathID"] # Finds the attached gameobject, uses that to find node
                mesh_id: int = tree["m_Mesh"]["m_PathID"]
                self.get_node_by_go_id(game_object_id).mesh_children.append(mesh_id) # Adds mesh id to nodes mesh_children arr

    def get_node_by_go_id(self, id: int) -> Node:
        try:
            return [node for node in self.nodes if node.game_object_id == id][0]
        except IndexError:
            return []

    def get_node_by_id(self, id: int) -> Node:
        if id in self.cache:
            return self.nodes[self.cache[id]]
        return None

    def get_nodes_by_go_name(self, name: str) -> list[Node]:
        try:
            return [node for node in self.nodes if node.game_object_name == name]
        except IndexError:
            return []

    def get_node_by_go_path(self, path: str) -> list[Node]:
        name: str = path.split("/")[-1]
        try:
            return [node for node in self.nodes if (node.game_object_name == name and node.get_path() == path)][0]
        except IndexError:
            return []

    def get_meshes_by_go_name(self, name: str) -> list[int]:
        mesh_arr: list[int] = []
        nodes: list[Node] = self.get_nodes_by_go_name(name)
        for n in nodes:
            mesh_arr.extend(n.mesh_children.copy())
        return list(set(mesh_arr)) # Filter potential duplicates     

    def get_submeshes_by_go_name(self, name: str) -> list[int]:
        mesh_arr: list[int] = []
        nodes: list[Node] = self.get_nodes_by_go_name(name)
        for node in nodes:
            mesh_arr.extend(node.get_submeshes())
        return list(set(mesh_arr)) # Filter potential duplicates 

    def get_submeshes_by_go_path(self, path: str) -> list[int]:
        node: Node = self.get_node_by_go_path(path)
        return node.get_submeshes()
