import asyncio
import pygame

from pygame.math import Vector2

from classes.levelManager import LevelManager
from classes.worldEnvironment import WorldEnvironment
from qlearning.qLearningAgent import qLearningTraining, getQLearningAgent
from helpers.assetsGetter import get_pixels_font
from helpers.customTextRender import render_text_with_outline
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    BG,
    ROWS,
    COLUMNS,
    TOPBARHEIGHT,
    FOOTERHEIGHT
)

def drawText(screen, font, text, x, y):
    textLabel = render_text_with_outline(
        fontType=font,
        text=text,
        color=(255,255,255)
    )
    
    textRect = textLabel.get_rect(center=(x,y))
    screen.blit(textLabel,textRect)


async def qLearningDemo():
    agent, trainingResults = getQLearningAgent(level=0, train= True)

    environment = WorldEnvironment(0)
    state = environment.reset()

    pygame.init()
    pygame.display.set_caption("Q-Learning Level 0 Demo")

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT + TOPBARHEIGHT + FOOTERHEIGHT)
    )
    clock = pygame.time.Clock()
    infoFont = pygame.font.Font(
        get_pixels_font(),
        16
    )
    tileSize = Vector2(
        WIDTH // COLUMNS,
        HEIGHT // ROWS
    )

    tileMap, player, monsters = await LevelManager().loadLevel(
        0,
        screen,
        tileSize,
        TOPBARHEIGHT
    )

    moveDelay = 300
    lastMoveTime = pygame.time.get_ticks()
    done = False
    totalReward = 0

    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        currentTime = pygame.time.get_ticks()

        if (
            not done
            and currentTime - lastMoveTime >= moveDelay
        ):
            action = agent.selectAction(
                state,
                epsilon=0.0
            )

            state, reward, done, move_direction = environment.step(action)
            totalReward += reward

            player.coordinate = Vector2(state)
            await player.on_move()

            if reward > 0:
                tileMap.tilesDictionary[state].hasApple = False
                player.appleCount += 1

            lastMoveTime = currentTime

        screen.fill(BG)

        await player.update(dt)
        tileMap.draw()
        player.draw()

        status = "Complete" if done else "Running"

        drawText(
            screen,
            infoFont,
            "Q-Learning | Level 0 | Epsilon: 0.0",
            WIDTH // 2,
            TOPBARHEIGHT // 2
        )

        drawText(
            screen,
            infoFont,
            (
                f"Steps: {environment.stepCount} | "
                f"Reward: {totalReward} | "
                f"Status: {status}"
            ),
            WIDTH // 2,
            TOPBARHEIGHT + HEIGHT + FOOTERHEIGHT // 2
        )

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(qLearningDemo())
