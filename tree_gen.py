# python tree_gen.py
import UnityPy
import json

class Node():
    def __init__(self, uuid):
        self.uuid = uuid
        self.parents = set()
        self.children = set()
    
    def add_parent(self, uuid):
        self.parents.add(uuid)

    def add_child(self, uuid):
        self.children.add(uuid)

    def get_tree_(self, nodes, caller_id, depth):
        if depth <= 10:
            children = {}
            for child_id in self.children:
                if child_id != caller_id:
                    children[child_id] = nodes[child_id].get_tree(nodes, self.uuid, depth + 1)
            if(len(children) > 0):
                return children
        return None

    def get_tree(self, nodes, depth):
        if depth <= 10:
            children = {}
            for child_id in self.children:
                if self.uuid in nodes[child_id].children:
                    children[child_id] = nodes[child_id].get_tree(nodes, depth + 1)
            if len(children) > 0:
                return children
        return None


GGM_src = "../Arena_Data/globalgamemanagers"
src = "../Arena_Data/resources.assets"

FILE_ID = 4
TARGET_PATH_ID = 1170

GGM_env = UnityPy.load(GGM_src)
env = UnityPy.load(src)

dependent_assets = [obj for obj in GGM_env.objects if obj.type.name == "ResourceManager"][0].read_typetree()["m_DependentAssets"]

nodes = {}
cache = set()

for dependency in dependent_assets:
    uuid = dependency["m_Object"]["m_PathID"]
    if dependency["m_Object"]["m_FileID"] != FILE_ID:
        pass
    if uuid not in cache:
        cache.add(uuid)
        nodes[uuid] = Node(uuid)
    for child in dependency["m_Dependencies"]:
        if child["m_FileID"] != FILE_ID:
            pass
        nodes[uuid].add_child(child["m_PathID"])
        if child["m_PathID"]not in cache:
            cache.add(child["m_PathID"])
            nodes[child["m_PathID"]] = Node(child["m_PathID"])
        nodes[child["m_PathID"]].add_parent(uuid)  


tree = {TARGET_PATH_ID: nodes[TARGET_PATH_ID].get_tree(nodes, 0)}

with open("./dumps/tree.json", "w") as file:
    json.dump(tree, file)



