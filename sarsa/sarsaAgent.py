import random
from classes.worldEnvironment import WorldEnvironment
from sarsa.sarsa import SARSA
from helpers.learningPolicy import linearEpsilon
from helpers.loadSetting import loadSetting
from helpers.agentHelper import saveQTable, loadQTable, loadTrainingResults


async def getSARSAAgent(level: int = 0, train: bool = False):
    if train:
        print("Training SARSA agent of level", level)
        return sarsaTraining(level)
    else:
        print("Loading SARSA agent of level", level)
        return sarsaLoad(level)


def sarsaLoad(level: int = 0):
    setting = loadSetting()
    agent = SARSA(setting["alpha"], setting["gamma"])
    agent = loadQTable(agent, level, 2)  # Load the trained Q-values!
    trainingResults = loadTrainingResults(2, level)
    return agent, trainingResults

def sarsaTraining (level = 1):
    setting = loadSetting()
    random.seed(setting["seed"])

    episodes = setting["episodes"]
    epsilonDecayEpisodes = setting["epsilonDecayEpisodes"]

    if level in [4, 5] :
        episodes = setting["monsterEpisodes"]
        epsilonDecayEpisodes = setting["monsterEpsilonDecayEpisodes"]

    environment = WorldEnvironment(level)

    agent = SARSA(
        setting["alpha"],
        setting["gamma"]
    )

    trainingResults = []

    for episode in range(episodes) :
        state = environment.reset()

        epsilon = linearEpsilon (
            episode,
            setting["epsilonStart"],
            setting["epsilonEnd"],
            epsilonDecayEpisodes
        )

        action = agent.selectAction(state, epsilon)
        totalReward = 0
        done = False

        for step in range(setting["maxStepsPerEpisode"]):
            nextState, reward, done, move_direction = environment.step(action)

            if done :
                nextAction = None

            else :
                nextAction = agent.selectAction(
                    nextState,
                    epsilon
                )

            agent.update(
                state,
                action,
                reward,
                nextState,
                nextAction,
                done
            )

            totalReward += reward

            if done:
                break

            state = nextState
            action = nextAction

        trainingResults.append({
            "episode" : episode + 1,
            "steps" : step + 1,
            "totalReward" : totalReward,
            "epsilon" : epsilon,
            "completed" : done and not environment.playerDied,
            "died" : environment.playerDied
        })


    saveQTable(agent, level, 2)
    return agent, trainingResults

def evaluateSARSA (agent, level = 1):
    setting = loadSetting()
    environment = WorldEnvironment(level)
    state = environment.reset()
    route = [state]
    totalReward = 0
    done = False

    for step in range(setting["maxStepsPerEpisode"]) :
        action = agent.selectAction(state, epsilon = 0.0)
        state, reward, done, move_direction = environment.step(action)

        route.append(state)
        totalReward += reward

        if done :
            break

    return {
        "route" : route,
        "steps" : len(route) - 1,
        "totalReward" : totalReward,
        "completed" : done and not environment.playerDied,
        "died" : environment.playerDied
    }
