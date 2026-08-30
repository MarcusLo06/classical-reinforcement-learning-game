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
        try:
            res = importlib.import_module(f"resources.level{level}")
        except ModuleNotFoundError:
            print(f"[Warning] resources.level{level} not found. Loading default empty map.")
            res = None

        cols = getattr(res, "MAP_COLS", 10)
        rows = getattr(res, "MAP_ROWS", 10)
        player_spawn = getattr(res, "PLAYER_SPAWN", (0, 0))
        level_map = getattr(res, "LEVEL_MAP", [[0] * cols for _ in range(rows)])
        
        apple_pos = getattr(res, "APPLE_POS", [])
        key_pos = getattr(res, "KEY_POS", [])
        chest_pos = getattr(res, "CHEST_POS", [])
        hazard_pos = getattr(res, "HAZARD_POS", [])

        tileMap = TileMap(screen, rows, cols, tileSize, topbarheight)
        player = Character(screen, Vector2(player_spawn), tileSize, topbarheight)
        

        for i in range(0, rows):
            for j in range(0, cols):
                tileMap.addTile((i, j), level_map[i][j] == 1)

        for pos in apple_pos:
            tileMap.tilesDictionary[pos].hasApple = True
        for pos in key_pos:
            tileMap.tilesDictionary[pos].hasKey = True
        for pos in chest_pos:
            tileMap.tilesDictionary[pos].hasChest = True
        # Mark hazard tiles and display with the water image
        for pos in hazard_pos:
            tileMap.tilesDictionary[pos].hasHazard = True
        

        return (tileMap, player)
