import pygame, sys, random, asyncio
from pygame.math import Vector2
from pygame import mixer
from classes.character import Character
from classes.tile import Tile
from classes.tilemap import TileMap
from classes.uiButton import UIButton
from classes.worldEnvironment import WorldEnvironment
from classes.levelManager import LevelManager
from qlearning.qLearningAgent import getQLearningAgent
from sarsa.sarsaAgent import getSARSAAgent
from helpers.pixelTranslate import translatePixelToCoordinate
from helpers.customTextRender import render_text_with_outline
from helpers.assetsGetter import get_pixels_font


from settings import WIDTH, HEIGHT, FPS, BG, ROWS, COLUMNS, TOPBARHEIGHT, FOOTERHEIGHT

DIRECTIONS = {
    "left": (-1, 0, "move_left"),
    "right": (1, 0, "move_right"),
    "up": (0, -1, "move_up"),
    "down": (0, 1, "move_down"),
}

VECTORDIRECTION = {
    (-1,0): "left",
    (1,0): "right",
    (0,-1): "up",
    (0,1): "down"
}

KEY_MAP = {
    pygame.K_a: "left",
    pygame.K_d: "right",
    pygame.K_w: "up",
    pygame.K_s: "down",
}


def is_valid_tile(x: int, y: int, tileMap, columns: int, rows: int) -> bool:
    """Checks bounds and obstacles for a target coordinate."""
    if not (0 <= x < columns and 0 <= y < rows):
        return False
    tile = tileMap.tilesDictionary.get((x, y))
    return tile is not None and not tile.isObstacle


async def onMove(
    player: Character,
    monsters: list[Character],
    player_direction: str,
    tileMap,
    columns: int,
    rows: int,
):
    # 1. Player Move Check & Execution
    p_dx, p_dy, p_method = DIRECTIONS[player_direction]
    target_px = player.coordinate.x + p_dx
    target_py = player.coordinate.y + p_dy

    if is_valid_tile(target_px, target_py, tileMap, columns, rows):
        await getattr(player, p_method)()

    # 2. Monster Move Checks & Execution
    monster_tasks = []
    for monster in monsters:
        if random.random() < 0.4 :
            # Pick only from valid directions around the monster
            valid_dirs = []
            for dir_name, (dx, dy, method_name) in DIRECTIONS.items():
                mx = monster.coordinate.x + dx
                my = monster.coordinate.y + dy
                if is_valid_tile(mx, my, tileMap, columns, rows):
                    valid_dirs.append(method_name)

            if valid_dirs:
                chosen_move = random.choice(valid_dirs)
                monster_tasks.append(getattr(monster, chosen_move)())

    # Execute all valid monster moves concurrently
    if monster_tasks:
        await asyncio.gather(*monster_tasks)



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


async def onLevelLoad(level: int, screen: pygame.surface, tileSize: Vector2, topbarHeight: int, RLAlgor: int):
    tileMap, player, monsters = await LevelManager().loadLevel(
        level,
        screen,
        tileSize,
        TOPBARHEIGHT
    )

    if RLAlgor == 1:
        agent, results = await getQLearningAgent(level, True)
    elif RLAlgor == 2:
        agent, results = await getSARSAAgent(level, True)
    else:
        agent = None

    return tileMap, player, monsters, agent




async def game_scene(screen, clock, level: int = 1):
    tileSize = Vector2(WIDTH // COLUMNS, HEIGHT // ROWS)
    infoFont = pygame.font.Font(get_pixels_font() , 20)

    RLAlgor = 0
    environment = WorldEnvironment(level)
    state = environment.reset()
    tileMap, player, monsters, agent = await onLevelLoad(level, screen, tileSize, TOPBARHEIGHT, RLAlgor)


    running = True
    debug = False
    levelComplete = False
    runAgent = False





    moveDelay = 10
    lastMoveTime = pygame.time.get_ticks()


    while running:
        dt = clock.tick(FPS) / 1000.0
        fps = clock.get_fps()

        target = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
    
        # INPUT GETTING
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False       
                
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    debug = not debug
                if e.key == pygame.K_t:
                    RLAlgor = (RLAlgor + 1) % 3


                    if RLAlgor == 1:
                        agent, results = await getQLearningAgent(level, True)
                    elif RLAlgor == 2:
                        agent, results = await getSARSAAgent(level, True)
                if e.key == pygame.K_SPACE:
                    runAgent = not runAgent

                if level > 1 and e.key == pygame.K_q:
                    level -= 1

                    environment = WorldEnvironment(level)
                    state = environment.reset()
                    tileMap, player, monsters, agent = await onLevelLoad(level, screen, tileSize, TOPBARHEIGHT, RLAlgor)

                    runAgent = False
                    levelComplete = False
                if level < 6 and e.key == pygame.K_e:
                    level += 1

                    environment = WorldEnvironment(level)
                    state = environment.reset()
                    tileMap, player, monsters, agent = await onLevelLoad(level, screen, tileSize, TOPBARHEIGHT, RLAlgor)

                    runAgent = False
                    levelComplete = False

                if not levelComplete and e.key in KEY_MAP:
                    await onMove(
                        player,
                        monsters,
                        KEY_MAP[e.key],
                        tileMap,
                        COLUMNS,
                        ROWS,
                    )



        if (
            runAgent
            and RLAlgor != 0
            and not levelComplete
            and currentTime - lastMoveTime >= moveDelay
        ):
            action = agent.selectAction(
                state,
                epsilon=0.0
            )

            state, reward, done, move_direction = environment.step(action)

            # player.coordinate = Vector2(state)
            # await player.on_move()
            await onMove(
                player,
                monsters,
                VECTORDIRECTION[move_direction],
                tileMap,
                COLUMNS,
                ROWS,
            )


            # if reward > 0:
            #     tileMap.tilesDictionary[state].hasApple = False
            #     player.appleCount += 1

            lastMoveTime = currentTime
                


        screen.fill(BG)

        if levelComplete:
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

        bottom_text = "(T) Reinforcement Learning Algorithm: " + ("None" if RLAlgor == 0 else "Q-Learning" if RLAlgor == 1 else "SARSA") + " - Running: " + str(runAgent)
        await draw_text(
            screen, infoFont,
            bottom_text,
            WIDTH // 2,  
            TOPBARHEIGHT + HEIGHT + FOOTERHEIGHT * 1/3,
        )

        
        bottom_text = f"Score: {str(player_score)} - Apple: {str(player.appleCount)} - Key: {str(player.keyCount)} - Chest: {str(player.chestCount)} - Steps: {environment.stepCount}"
        await draw_text(
            screen, infoFont,
            bottom_text,
            WIDTH // 2,  
            TOPBARHEIGHT + HEIGHT + FOOTERHEIGHT * 2/3,
        )




        # Check if player collected anything.
        tilePlayerOn = tileMap.tilesDictionary[tuple(player.coordinate)]
        # Reset level when the player enters a hazard tile
        if tilePlayerOn.hasHazard or any(m.coordinate == player.coordinate for m in monsters):
            tileMap, player, monsters = await LevelManager().loadLevel(
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
        await player.update(dt)
        tileMap.draw(debug)
        player.draw()

        for monster in monsters:
            await monster.update(dt)
            monster.draw()

        
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
