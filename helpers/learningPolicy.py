import random

from classes.worldEnvironment import ALL_ACTIONS

def linearEpsilon(episode, start, end, decayEpisodes) :
    if decayEpisodes <= 0:
        return end
    progress = min(episode / decayEpisodes, 1.0)
    return start + progress * (end - start)

def epsilonGreedy(qTable, state, epsilon):
    if random.random() < epsilon:
        return random.choice(ALL_ACTIONS)
    
    bestActions = qTable.bestActions(state)
    
    return random.choice(bestActions)
