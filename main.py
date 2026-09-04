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


async def draw_text(screen: pygame.surface, font: pygame.font, inp_text: str, x: int, y: int, inp_color: pygame.color = (255,255,255)):
    textLabel = render_text_with_outline(
        fontType=font,
        text= inp_text,
        color=inp_color
    )
    textRect = textLabel.get_rect(center=(x, y))
    screen.blit(textLabel, textRect)
    
# Check if the level has been cleared
def allRewardsCollected (tileMap) :
    for tile in tileMap.tilesDictionary.values() :
        if tile.hasApple :
            return False

        if tile.hasChest and not tile.chestOpened :
            return False

    return True


async def game_scene(screen, clock, level: int = 1):
    tileSize = Vector2(WIDTH // COLUMNS, HEIGHT // ROWS)
    infoFont = pygame.font.Font(get_pixels_font() , 20)

    tileMap, player = await LevelManager().loadLevel(level, screen, tileSize, TOPBARHEIGHT)


    running = True
    debug = False
    levelComplete = False


    while running:
        dt = clock.tick(FPS) / 1000.0
        fps = clock.get_fps()

        target = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
    
        # INPUT GETTING
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False       
                
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    debug = not debug
                if level > 1 and e.key == pygame.K_q:
                    level -= 1
                    tileMap, player = await LevelManager().loadLevel(
                        level,
                        screen,
                        tileSize,
                        TOPBARHEIGHT
                    )
                    levelComplete = False
                if level < 6 and e.key == pygame.K_e:
                    level += 1
                    tileMap, player = await LevelManager().loadLevel(
                        level,
                        screen,
                        tileSize,
                        TOPBARHEIGHT
                    )
                    levelComplete = False

                if not levelComplete :
                    if e.key == pygame.K_a and player.coordinate.x > 0 and not tileMap.tilesDictionary[(player.coordinate.x - 1, player.coordinate.y)].isObstacle:
                        await player.move_left()
                    if e.key == pygame.K_d and player.coordinate.x < COLUMNS - 1 and not tileMap.tilesDictionary[(player.coordinate.x + 1, player.coordinate.y)].isObstacle:
                        await player.move_right()
                    if e.key == pygame.K_w and player.coordinate.y > 0 and not tileMap.tilesDictionary[(player.coordinate.x, player.coordinate.y - 1)].isObstacle:
                        await player.move_up()
                    if e.key == pygame.K_s and player.coordinate.y < ROWS - 1 and not tileMap.tilesDictionary[(player.coordinate.x, player.coordinate.y + 1)].isObstacle:
                        await player.move_down()
                


        screen.fill(BG)

        if levelComplete :
            levelText = "Level Complete"
            levelTextColor = (255, 215, 0)
        else :
            levelText = "Level " + str(level)
            levelTextColor = (255, 255, 255)

        # THIS PART IS USED TO DRAW TEXT TO THE SCREEN
        await draw_text(
            screen,
            infoFont,
            levelText,
            WIDTH // 2,  
            TOPBARHEIGHT // 2,
            levelTextColor
        )

        await draw_text(
            screen, infoFont,
            "Previous level (Q)",
            WIDTH * 1 / 5,  
            TOPBARHEIGHT // 2,
        )

        await draw_text(
            screen, infoFont,
            "Next level (E)",
            WIDTH * 4 / 5,  
            TOPBARHEIGHT // 2,
        )


        # Total Score
        player_score = player.appleCount + player.chestCount * 2
        await draw_text(
            screen, infoFont,
            "Score: " + str(player_score),
            WIDTH * 1 / 5,  
            TOPBARHEIGHT + HEIGHT + FOOTERHEIGHT // 2,
        )

        await draw_text(
            screen, infoFont,
            "Apple: " + str(player.appleCount),
            WIDTH * 2 / 5,  
            TOPBARHEIGHT + HEIGHT + FOOTERHEIGHT // 2,
        )

        await draw_text(
            screen, infoFont,
            "Key: " + str(player.keyCount),
            WIDTH * 3 / 5,  
            TOPBARHEIGHT + HEIGHT + FOOTERHEIGHT // 2,
        )

        await draw_text(
            screen, infoFont,
            "Chest: " + str(player.chestCount),
            WIDTH * 4 / 5,  
            TOPBARHEIGHT + HEIGHT + FOOTERHEIGHT // 2,
        )


        # Check if player collected anything.
        tilePlayerOn = tileMap.tilesDictionary[tuple(player.coordinate)]
        # Reset level when the player enters a hazard tile
        if tilePlayerOn.hasHazard:
            tileMap, player = await LevelManager().loadLevel(
                level,
                screen,
                tileSize,
                TOPBARHEIGHT
            )
            levelComplete = False
            continue
        if tilePlayerOn.hasApple:
            tilePlayerOn.hasApple = False
            player.appleCount += 1
        if tilePlayerOn.hasKey:
            tilePlayerOn.hasKey = False
            player.keyCount += 1
        if (
            tilePlayerOn.hasChest
            and not tilePlayerOn.chestOpened
            and player.keyCount > 0
        ) :
            tilePlayerOn.chestOpened = True
            player.chestCount += 1
            player.keyCount -= 1

        levelComplete = allRewardsCollected(tileMap)



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

    await game_scene(screen, clock)


if __name__ == "__main__":
    asyncio.run(main())
