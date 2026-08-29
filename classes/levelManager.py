import os, importlib, pygame
from pygame.math import Vector2
from .tile import Tile
from .tilemap import TileMap
from .character import Character

class LevelManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Guard __init__ so it doesn't re-run every time LevelManager() is called
        if not hasattr(self, "_initialized"):
            self.current_level = None
            self._initialized = True



    async def loadLevel(self, level: int, screen: pygame.surface, tileSize: tuple[int,int], topbarheight: int) -> tuple[TileMap, Character]:
        res = importlib.import_module(f"resources.level{level}")
        cols, rows = res.MAP_COLS, res.MAP_ROWS

        tileMap = TileMap(screen, rows, cols, tileSize, topbarheight)
        player = Character(screen, Vector2(res.PLAYER_SPAWN), tileSize, topbarheight)
        

        for i in range(0, rows):
            for j in range(0, cols):
                tileMap.addTile((i, j), res.LEVEL_MAP[i][j] == 1)



                # print(resGrid[i + 1][j], end=" ")
            # print("\n")

        return (tileMap, player)

    # def get_random_image_in_folder(folder_path: str) -> str:
    # # 1. Get a list of all files in the folder that end with .png
    #     png_files = [
    #         file for file in os.listdir(folder_path) if file.lower().endswith(".png")
    #     ]

    #     # 2. Check if any PNG files were found
    #     if not png_files:
    #         raise FileNotFoundError(f"No PNG files found in {folder_path}")

    #     # 3. Choose a random file name
    #     chosen_file = random.choice(png_files)

    #     # 4. Join the folder path and file name to create the full path
    #     return os.path.join(folder_path, chosen_file)

