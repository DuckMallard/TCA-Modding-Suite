from Node_Tree import Node_Tree
from Injector import Injector

BLEND_FILE = "models/Example.blend"

tree: Node_Tree = Node_Tree("C:/Program Files (x86)/Steam/steamapps/common/TinyCombatArena/Arena_Data/resources.assets")
injector: Injector = Injector("C:/Program Files (x86)/Steam/steamapps/common/TinyCombatArena/Arena_Data/resources.assets") 

mesh_ids: list[int] = tree.get_submeshes_by_go_name("Mk82")
for id in mesh_ids:
    injector.inject(id, BLEND_FILE, "Test")
injector.save("C:/Program Files (x86)/Steam/Backups/TinyCombatArenaDev/Arena_Data/resources.assets")