# python extract_container.py
import UnityPy
import json

GGM_src = "../Arena_Data/globalgamemanagers"

GGM_env = UnityPy.load(GGM_src)

dependent_assets = [obj for obj in GGM_env.objects if obj.type.name == "ResourceManager"][0].read_typetree()["m_Container"]
with open("./dumps/container.json", "w") as file:
    json.dump(dependent_assets, file)