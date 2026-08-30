import random
from classes.worldEnvironment import WorldEnvironment
from qlearning.qLearning import QLearning
from helpers.learningPolicy import linearEpsilon
from helpers.loadSetting import loadSetting


def qLearningTraining (level = 0):
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

            nextState, reward, done = environment.step(action)

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
            "completed" : done and not environment.playerDied
        })
    
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
        state, reward, done = environment.step(action)
        
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
