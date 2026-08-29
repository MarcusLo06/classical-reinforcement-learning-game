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

        for pos in res.APPLE_POS:
            tileMap.tilesDictionary[pos].hasApple = True
        for pos in res.KEY_POS:
            tileMap.tilesDictionary[pos].hasKey = True
        for pos in res.CHEST_POS:
            tileMap.tilesDictionary[pos].hasChest = True
        

        return (tileMap, player)
