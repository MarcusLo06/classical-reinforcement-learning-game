import random, pickle, csv
from classes.worldEnvironment import WorldEnvironment
from qlearning.qLearning import QLearning
from helpers.learningPolicy import linearEpsilon
from helpers.loadSetting import loadSetting
from helpers.agentHelper import saveQTable, loadQTable, loadTrainingResults



async def getQLearningAgent(level: int = 0, train: bool = False):
    if train:
        print("Training agent of level", level)
        return qLearningTraining(level)
    else:
        print("Loading agent of level", level)
        return qLearningLoad(level)
        


def qLearningLoad(level: int = 0):
    setting = loadSetting()
    agent = QLearning(setting["alpha"], setting["gamma"])
    agent = loadQTable(agent, level)  # Load the trained Q-values!
    trainingResults = loadTrainingResults(level)
    return agent, trainingResults


def qLearningTraining (level: int = 0):
    setting = loadSetting()
    random.seed(setting["seed"])
    
    environment = WorldEnvironment(level)
    
    agent = QLearning(
        setting["alpha"],
        setting["gamma"]
    )
    
    trainingResults = []

    for episode in range(setting["episodes"]) :
        state = environment.reset()
        
        epsilon = linearEpsilon (
            episode,
            setting["epsilonStart"],
            setting["epsilonEnd"],
            setting["epsilonDecayEpisodes"]
        )
        
        totalReward = 0

        for step in range(setting["maxStepsPerEpisode"]):
            action = agent.selectAction(state, epsilon)

            nextState, reward, done, move_direction = environment.step(action)

            agent.update(
                state,
                action,
                reward,
                nextState,
                done
            )

            state = nextState
            totalReward += reward

            if done:
                break
        
        trainingResults.append({
            "episode" : episode + 1,
            "steps" : step + 1,
            "totalReward" : totalReward,
            "epsilon" : epsilon,
            "completed" : done and not environment.playerDied,
            "died" : environment.playerDied
        })


    saveQTable(agent, level)
    return agent, trainingResults

def evaluateQLearning(agent, level = 0):
    setting = loadSetting()
    environment = WorldEnvironment(level)
    state = environment.reset()
    route = [state]
    totalReward = 0
    done = False
    
    for step in range(setting["maxStepsPerEpisode"]):
        action = agent.selectAction(state, epsilon = 0.0)
        state, reward, done, move_direction = environment.step(action)
        
        route.append(state)
        totalReward += reward
        
        if done: 
            break
    
    return {
        "route" : route,
        "steps" : len(route) - 1,
        "totalReward" : totalReward,
        "completed" : done and not environment.playerDied,
        "died" : environment.playerDied
    }
