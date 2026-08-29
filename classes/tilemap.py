import pygame
from pygame import mixer
from pygame.math import Vector2
from .tile import Tile

class TileMap:
    def __init__(self, surface: pygame.surface, rows: int = 10, columns: int = 10, tileSize: Vector2 = Vector2(50, 50), topbarHeight: int = 0):
        self.surface = surface
        self.tilesDictionary: dict[Vector2, Tile] = {}
        self.rows = rows
        self.columns = columns
        self.tileSize = tileSize
        self.topbarHeight = topbarHeight

        self.selectedTile: Tile = None


    def tileIsInMap(self, coordinate: Vector2) -> bool:
        coord = Vector2(coordinate)
        if (
            0 <= coord.x < self.columns
            and 0 <= coord.y < self.rows
            and tuple(coordinate) in self.tilesDictionary
        ):
            # print("Tile at", coord, "is in map")
            return True
        else:
            # print("Tile at", coord, "is not in map")
            return False

    def tileIsWalkable(self, coordinate: Vector2) -> Tile:
        if self.tileIsInMap(coordinate) and not self.tilesDictionary[tuple(coordinate)].isObstacle:
            return self.tilesDictionary[tuple(coordinate)]

        return None


    def addTile(self, 
            tileCoordinate: Vector2, tileColor: pygame.Color = (255,255,255), 
            outline: int = 0, isObstacle: bool = False, obstacleColor: pygame.Color = (0,0,0)
        ) -> bool:
        if self.tileIsInMap(tileCoordinate):
            # print("Tiles at", Vector2(tileCoordinate), "is in map")
            return False

        newTile = Tile(self.surface, Vector2(tileCoordinate), self.tileSize, tileColor, outline, isObstacle, obstacleColor, self.topbarHeight)
        self.tilesDictionary[tileCoordinate] = newTile
        return True


    def removeTile(self, tileCoordinate: Vector2) -> bool:
        if not self.tileIsInMap(tileCoordinate):
            
            return False

        self.tilesDictionary[tileCoordinate] = None
        return True


    def draw(self, debug: bool = False):
        for tile in self.tilesDictionary.values():
            tile.draw(debug)
            tile.refresh_path()

        if self.selectedTile:
            self.selectedTile.draw_highlight()