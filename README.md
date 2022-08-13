## TCA-Modding-Suite
A suite of tools for injection based modding on the unity game TCA

Copyright (c) 2022 JMayh with MIT Licensce

Credit to [Why485](https://twitter.com/Why485) and [Microprose](https://www.microprose.com/games/tiny-combat-arena/) for Tiny Combat Arena

___

### Model Injection:

Current model injection allows for user created meshes in blender to be placed into the game. At present this takes the form of swaps, an original TCA mesh will be replaced.

#### Prerequisites:
- [Blender](https://www.blender.org/download/) (Version requirements unknown)
- [Python](https://www.python.org/downloads) (3.x.x)
- [TCA Testers branch](https://store.steampowered.com/news/app/1347550/view/3376030426065446508) (0.9.0.1T)
- [UnityPy](https://pypi.org/project/UnityPy/) (1.9.6+)

#### Getting Started:
- Generally for any modding it is advisable to use a **copy** of the game. I would recommend copying everything from `Steam\steamapps\common\TinyCombatArena` to `C:\Program Files (x86)\Steam\Backups\TinyCombatArenaDev`. This format will be used throughout the documentation and will make it easier to follow.
- Download and unzip this repository placing it anywhere on your system. **Not near any TCA game files.**
- The default paths supplied to the program may not be identical to your setup. First go into `src/mesh_injector.py`and focus on lines 8-12. Using the definitions below amend if neccersary using the default settings as a guide. For all but `BLEND_PATH` avoid using relative paths
```py
BLENDER_PATH = #Location of blender.exe
BLEND_PATH = # Location of the .blend file you are using
ASSET_FILE_PATH_IN = # Location of the original TCA Arena.exe file
ASSET_FILE_PATH_OUT = # Location of your backed up TCA Arena.exe file
ASSET_PATH_ID = # ID of the asset we are swapping (Default of 225 is fine for now)
```
- Run `mesh_injector.py` using command prompt, or simply by double clicking the file.
- Once the process has completed you can then run Arena.exe in your backup folder.
- If the previous steps were followed correctly you should see any instance of the Mk82 be replaced with your custom mesh
---
###Notes:
- This is a very early release and is likely to have many bugs. Either open an issue, or hop on the [TCA Modding Server](https://discord.gg/D5ScNgcTJh) to receieve support.



