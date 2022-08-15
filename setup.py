#python -m pip install --no-index --find-links=wheels UnityPy
#"BLENDER_FILE_PATH": "C:/Program Files/Blender Foundation/Blender 3.0",
#"TCA_FILE_PATH": "C:/Program Files (x86)/Steam/Backups/TinyCombatArenaDev"

import os
import json
import subprocess

CONFIG: str
BLENDER_FILE_PATH: str
PYTHON_EXE_PATH: str
TCA_FILE_PATH: str

with open("config.json", "r") as file:
    CONFIG = json.load(file)
    BLENDER_FILE_PATH = CONFIG["env"]["BLENDER_FILE_PATH"]
    TCA_FILE_PATH = CONFIG["env"]["TCA_FILE_PATH"]

version: str = BLENDER_FILE_PATH.split("/")[-1].split(" ")[-1]
PYTHON_EXE_PATH = os.path.join(BLENDER_FILE_PATH, version, "python\\bin\\python.exe")

if not os.path.exists(PYTHON_EXE_PATH):
    raise OSError("python.exe for blender not in correct location, should be in `Blender 3.X/3.X/python/bin/python.exe`")

os.chdir(os.path.dirname(__file__))
#subprocess.run([PYTHON_EXE_PATH, "-m", "pip", "install", "--no-index", "--find-links=wheels", "UnityPy"])
#completed_process = subprocess.run([f'"{PYTHON_EXE_PATH}"', "-m", "pip", "install", "--no-index", "--report", "--ignore-installed", "--dry-run", "--find-links=wheels", "UnityPy"])
#print(" ".join(completed_process.args))
print(" ".join([f'"{PYTHON_EXE_PATH}"', "-m", "pip", "install", "--no-index", "--find-links=wheels", "UnityPy"]))