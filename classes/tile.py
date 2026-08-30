import pygame
import random
from pygame.math import Vector2
from helpers.pixelTranslate import translateCoordinateToPixel
from helpers.assetsGetter import *
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
        self.hasApple = False
        self.hasKey = False
        self.hasChest = False
        self.chestOpened = False
        # Hazard tiles use the water image so they are easy to identify
        self.hasHazard = False

        self.rectStartPos = translateCoordinateToPixel(self.coordinate, tileSize)
        self.rect = pygame.Rect(self.rectStartPos.x, self.rectStartPos.y + topbarHeight, self.tileSize.x, self.tileSize.y)

        self.grass_path = get_random_grass_image()
        self.obstacle_image_path = get_random_water_and_obstacle_image(1)


        self.flipObstacle = random.random() < 0.5
        self.weigthFont = pygame.font.Font(get_pixels_font() , 15)

        


    def refresh_image(self):
        # Always load the base grass background first
        
        grass_image = pygame.image.load(self.grass_path).convert_alpha()
        grass_image = pygame.transform.scale(grass_image, self.tileSize)


        if (
            self.isObstacle
            or self.hasApple
            or self.hasKey
            or self.hasChest
            or self.hasHazard
        ):
            # Select the image for an obstacle, hazard, or collectible item
            if self.isObstacle:
                image_path = self.obstacle_image_path
            elif self.hasHazard:
                image_path = get_random_water_image()
            elif self.hasApple:
                image_path = get_apple_path_image()
            elif self.hasKey:
                image_path = get_key_path_image()
            elif self.hasChest:
                image_path = get_chest_path_image(self.chestOpened)

            raw_obstacle = pygame.image.load(image_path).convert_alpha()
            
            # Apply colorkey to remove white background if needed
            bg_color = raw_obstacle.get_at((0, 0))
            raw_obstacle.set_colorkey(bg_color)
            
            obstacle_image = pygame.transform.scale(raw_obstacle, self.tileSize)

            

            # Create a canvas surface matching the tile size
            combined_surface = pygame.Surface(self.tileSize, pygame.SRCALPHA)

            # Stack both images: draw grass first, then obstacle on top
            combined_surface.blit(grass_image, (0, 0))
            combined_surface.blit(obstacle_image, (0, 0))

            self.image = combined_surface
            if self.flipObstacle:
                self.image = pygame.transform.flip(
                    combined_surface, True, False
                )
        else:
            grass_image = pygame.image.load(self.grass_path).convert_alpha()
            grass_image = pygame.transform.scale(grass_image, self.tileSize)

            self.image = grass_image


    def draw(self, debug: bool = False):
        if hasattr(self, "image"):
            self.surface.blit(self.image, self.rect)
