import pygame
import random
from pygame.math import Vector2
from helpers.pixelTranslate import translateCoordinateToPixel
from helpers.assetsGetter import get_random_grass_image, get_random_water_and_obstacle_image, get_random_path_image, get_pixels_font
from helpers.customTextRender import render_text_with_outline



class Tile:
    def __init__(
            self, surface: pygame.Surface, coordinate: Vector2, 
            tileSize: Vector2 =  Vector2(50,50),
            isObstacle: bool = False,
            topbarHeight: int = 0
            ):
        self.surface = surface
        self.coordinate = coordinate
        self.tileSize = tileSize
        self.isObstacle = isObstacle
        self.grass_path = ""
        self.topbarHeight = topbarHeight

        self.rectStartPos = translateCoordinateToPixel(self.coordinate, tileSize)
        self.rect = pygame.Rect(self.rectStartPos.x, self.rectStartPos.y + topbarHeight, self.tileSize.x, self.tileSize.y)

        self.weigthFont = pygame.font.Font(get_pixels_font() , 15)

        # 1. Always load the base grass background first
        self.grass_path = get_random_grass_image()
        grass_image = pygame.image.load(self.grass_path).convert_alpha()
        grass_image = pygame.transform.scale(grass_image, tileSize)

        if isObstacle:
            # 2. Load the obstacle overlay image
            raw_obstacle = pygame.image.load(get_random_water_and_obstacle_image(1)).convert_alpha()
            
            # Apply colorkey to remove white background if needed
            bg_color = raw_obstacle.get_at((0, 0))
            raw_obstacle.set_colorkey(bg_color)
            
            obstacle_image = pygame.transform.scale(raw_obstacle, tileSize)

            

            # 3. Create a canvas surface matching the tile size
            combined_surface = pygame.Surface(tileSize, pygame.SRCALPHA)

            # 4. Stack both images: draw grass first, then obstacle on top
            combined_surface.blit(grass_image, (0, 0))
            combined_surface.blit(obstacle_image, (0, 0))

            self.image = combined_surface
            if random.random() < 0.5:
                self.image = pygame.transform.flip(
                    combined_surface, True, False
                )
        else:
            # If not an obstacle, just use the grass image
            self.image = grass_image

    def refresh_path(self):
        if self.isObstacle: return

        grass_image = pygame.image.load(self.grass_path).convert_alpha()
        grass_image = pygame.transform.scale(grass_image, self.tileSize)

        self.image = grass_image


    def draw(self, debug: bool = False):
        # 1. Base tile sprite
        self.surface.blit(self.image, self.rect)