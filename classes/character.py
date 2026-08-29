import pygame, asyncio
from helpers.assetsGetter import get_character_idle_image, get_character_walking_image
from helpers.pixelTranslate import translateCoordinateToPixel
from pygame.math import Vector2

class Character:
    def __init__(self, surface: pygame.surface, coordinate: Vector2 = (0,0), tileSize: Vector2 = Vector2(16, 16), topbarHeight: int = 0):
        self.surface = surface
        self.coordinate = coordinate
        self.tileSize = tileSize
        self.spriteSpeed = 0.5
        self.isWalking = False
        self.facingRight = True
        self.topbarHeight = topbarHeight

        # Timer to track accumulated time
        self.animationTimer = 0.0

        self.walkDuration = 1.0
        self.lastMove = 0.0

        # Load initial image
        self.image = pygame.image.load(
            get_character_idle_image()
        ).convert_alpha()

        self.rectStartPos = translateCoordinateToPixel(self.coordinate, tileSize)
        self.rect = pygame.Rect(self.rectStartPos.x, self.rectStartPos.y + self.topbarHeight, self.tileSize.x, self.tileSize.y)

    async def on_move(self):
        self.rectStartPos = translateCoordinateToPixel(self.coordinate, self.tileSize)
        self.rect = pygame.Rect(self.rectStartPos.x, self.rectStartPos.y + self.topbarHeight, self.tileSize.x, self.tileSize.y)

        self.isWalking = True
        self.walkTimer = self.walkDuration


    async def move_left(self):
        self.coordinate = Vector2(self.coordinate.x - 1, self.coordinate.y)
        self.facingRight = False
        await self.on_move()
        

    async def move_right(self):
        self.coordinate = Vector2(self.coordinate.x + 1, self.coordinate.y)
        self.facingRight = True
        await self.on_move()

    async def move_up(self):
        self.coordinate = Vector2(self.coordinate.x, self.coordinate.y - 1)
        await self.on_move()

    async def move_down(self):
        self.coordinate = Vector2(self.coordinate.x, self.coordinate.y + 1)
        await self.on_move()


    def update(self, dt: float):
        # 1. Handle walking duration buffer
        if self.isWalking:
            self.walkTimer -= dt
            if self.walkTimer <= 0:
                self.isWalking = False
                self.walkTimer = 0.0
                # Force immediate update to idle image when walking stops
                raw_image = pygame.image.load(
                    get_character_idle_image()
                ).convert_alpha()
                self.image = pygame.transform.scale(raw_image, self.tileSize)

        # 2. Handle sprite frame animation swaps
        self.animationTimer += dt
        if self.animationTimer >= self.spriteSpeed:
            self.animationTimer = 0.0

            if self.isWalking:
                raw_image = pygame.image.load(
                    get_character_walking_image()
                ).convert_alpha()
            else:
                raw_image = pygame.image.load(
                    get_character_idle_image()
                ).convert_alpha()

            scaled_image = pygame.transform.scale(raw_image, self.tileSize)

            if not self.facingRight:
               self.image = pygame.transform.flip(
                   scaled_image, True, False
               )  # True for horizontal, False for vertical
            else:
                self.image = scaled_image

    def draw(self):
        self.surface.blit(self.image, self.rect)