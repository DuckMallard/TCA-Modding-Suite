class Node():
    def __init__(self, id: int):
        self.id: int = id
        self.parent: Node = None
        self.children: list[Node] = [] # Arr of nodes
        self.game_object_id = None
        self.game_object_name = ""
        self.mesh_children: list[int] = []
        self.texture_children: list[int] = []
    
    def add_child(self, node):
        self.children.append(node)

    def set_parent(self, node):
        self.parent = node

    def get_path(self) -> str:
        node_name_arr: list[str] = self._get_path()
        node_name_arr.reverse()
        return "/".join(node_name_arr)

    def _get_path(self) -> list[str]:
        if self.parent:
            return ([self.game_object_name] + self.parent._get_path())
        return [self.game_object_name]

    def get_subnodes(self) -> list[object]:
        subnode_arr: list[Node] = []
        for child in self.children:
            subnode_arr.extend([child.id] + child.get_subnodes())
        return subnode_arr

    def get_submeshes(self) -> list[int]:
        mesh_arr: list[int] = self.mesh_children.copy()
        for child in self.children:
            mesh_arr.extend(child.get_submeshes())
        return mesh_arr

    
