import pygame, sys, random, asyncio
from pygame.math import Vector2
from pygame import mixer
from classes.character import Character
from classes.tile import Tile
from classes.tilemap import TileMap
from classes.uiButton import UIButton
from classes.levelManager import LevelManager
from helpers.pixelTranslate import translatePixelToCoordinate
from helpers.customTextRender import render_text_with_outline
from helpers.assetsGetter import get_pixels_font


from settings import WIDTH, HEIGHT, FPS, BG, ROWS, COLUMNS, TOPBARHEIGHT, FOOTERHEIGHT


async def draw_text(screen: pygame.surface, font: pygame.font, inp_text: str, x: int, y: int, inp_color: pygame.color):
    textLabel = render_text_with_outline(
        fontType=font,
        text= inp_text,
        color=inp_color
    )
    textRect = textLabel.get_rect(center=(x, y))
    screen.blit(textLabel, textRect)


async def game_scene(screen, clock, level: int):
    tileSize = Vector2(WIDTH // COLUMNS, HEIGHT // ROWS)
    infoFont = pygame.font.Font(get_pixels_font() , 20)

    tileMap, player = await LevelManager().loadLevel(level, screen, tileSize, TOPBARHEIGHT)


    running = True
    debug = False


    while running:
        dt = clock.tick(FPS) / 1000.0
        fps = clock.get_fps()

        target = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
    

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False       
                
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    debug = not debug

                if e.key == pygame.K_a and player.coordinate.x > 0 and not tileMap.tilesDictionary[(player.coordinate.x - 1, player.coordinate.y)].isObstacle:
                    await player.move_left()
                if e.key == pygame.K_d and player.coordinate.x < COLUMNS - 1 and not tileMap.tilesDictionary[(player.coordinate.x + 1, player.coordinate.y)].isObstacle:
                    await player.move_right()
                if e.key == pygame.K_w and player.coordinate.y > 0 and not tileMap.tilesDictionary[(player.coordinate.x, player.coordinate.y - 1)].isObstacle:
                    await player.move_up()
                if e.key == pygame.K_s and player.coordinate.y < ROWS - 1 and not tileMap.tilesDictionary[(player.coordinate.x, player.coordinate.y + 1)].isObstacle:
                    await player.move_down()
                


        screen.fill(BG)


        # THIS PART IS USED TO DRAW TEXT TO THE SCREEN
        # Debug tip text
        await draw_text(
            screen, 
            infoFont, 
            "(R) Debug Mode "+ ("On" if debug else "Off"), 
            WIDTH * 1 / 5,  
            TOPBARHEIGHT // 2,
            (255, 255, 255)
        )

        # Moving tip
        await draw_text(
            screen,
            infoFont,
            "WASD: Move",
            WIDTH * 2.5 / 5,  
            TOPBARHEIGHT // 2,
            (255, 255, 255)
        )




        # if debug:
        #     # nothing yet
        #     print("debug")

        player.update(dt)

        tileMap.draw(debug)

        player.draw()

        
        await asyncio.sleep(0)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


async def main():
    pygame.init()
    mixer.init()

    pygame.display.set_caption("Classical Reinforcement Learning")

    screen = pygame.display.set_mode((WIDTH,HEIGHT + TOPBARHEIGHT + FOOTERHEIGHT))
    clock = pygame.time.Clock()

    await game_scene(screen, clock, 1)


if __name__ == "__main__":
    asyncio.run(main())