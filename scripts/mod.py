from Node_Tree import Node_Tree
from Injector import Injector

BLEND_FILE = "C:/Users/jmayh/Documents/Programming/TCA-Modding-Suite/models/A-4.blend"

tree: Node_Tree = Node_Tree("C:/Program Files (x86)/Steam/steamapps/common/TinyCombatArena/Arena_Data/resources.assets")
injector: Injector = Injector("C:/Program Files (x86)/Steam/steamapps/common/TinyCombatArena/Arena_Data/resources.assets") 

meshes = ["Fuselage", "Canopy", "CanopyEject", "WingLeftInner", "WingLeftOuter", "WingRightInner", "WingRightOuter", "ElevatorLeft", "ElevatorRight", "PylonLeftInner", "PylonLeftOuter", "PylonRightInner", "PylonRightOuter", "PylonCenter", "NozzleInterior", "Pitot", "TailInner", "TailOuter"]


mesh_ids: list[int] = tree.get_submeshes_by_go_name("Mig21bis")
mesh_data = [[id, tree.obj_dict[id].read_typetree()["m_Name"]] for id in mesh_ids]

mesh_data = [mesh for mesh in mesh_data if True]
for mesh in mesh_data:
    injector.add_injection(tree.get_transform_by_mesh_id(mesh[0]).id, mesh[1], mesh[0])

root = tree.get_nodes_by_go_name("Mig21bis")[0]
subnodes = [tree.nodes[tree.cache[id]] for id in root.get_subnodes()]

transforms = ["Pilot", "GunL", "GunR", "Radar", "Station1", "Station2", "Station3", "Station4", "Station5", "FlybyFocus", "GearMainL", "GearMainR", "GearNose", "CMLauncher1", "CMLauncher2", "CockpitCam", "TrailL", "TrailR"]
nodes = [node for node in subnodes if node.game_object_name in transforms]
for node in nodes:
    injector.add_injection(node.id, node.game_object_name)

injector.build(BLEND_FILE)

injector.save("C:/Program Files (x86)/Steam/Backups/TinyCombatArenaDev/Arena_Data/resources.assets")