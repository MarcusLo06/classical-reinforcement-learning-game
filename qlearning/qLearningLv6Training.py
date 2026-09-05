# intrinsic reward for lv 6
import math
import random

from classes.worldEnvironment import WorldEnvironment
from qlearning.qLearning import QLearning
from helpers.learningPolicy import linearEpsilon
from helpers.loadSetting import loadSetting

# count state visits and calculate the intrinsic reward
def calculateIntrinsicReward (
    state,
    visitCounts,
    intrinsicRewardStrength
) :
    stateVisitCount = visitCounts.get(state, 0)

    intrinsicReward = (
        intrinsicRewardStrength
        / math.sqrt(stateVisitCount + 1)
    )

    visitCounts[state] = stateVisitCount + 1

    return intrinsicReward

def qLearningLv6Training (useIntrinsicReward = True) :
    setting = loadSetting()
    random.seed(setting["seed"])

    environment = WorldEnvironment(6)

    agent = QLearning(
        setting["alpha"],
        setting["gamma"]
    )

    intrinsicRewardStrength = setting["intrinsicRewardStrength"]
    trainingResults = []

    for episode in range(setting["episodes"]) :
        state = environment.reset()

        # Reset state visits for each episode
        visitCounts = {state : 1}

        epsilon = linearEpsilon(
            episode,
            setting["epsilonStart"],
            setting["epsilonEnd"],
            setting["epsilonDecayEpisodes"]
        )

        totalEnvironmentReward = 0
        totalIntrinsicReward = 0
        done = False

        for step in range(setting["maxStepsPerEpisode"]) :
            action = agent.selectAction(state, epsilon)

            nextState, environmentReward, done = environment.step(action)

            intrinsicReward = 0

            if useIntrinsicReward :
                intrinsicReward = calculateIntrinsicReward(
                    nextState,
                    visitCounts,
                    intrinsicRewardStrength
                )

            learningReward = environmentReward + intrinsicReward

            agent.update(
                state,
                action,
                learningReward,
                nextState,
                done
            )

            state = nextState
            totalEnvironmentReward += environmentReward
            totalIntrinsicReward += intrinsicReward

            if done :
                break

        trainingResults.append({
            "episode" : episode + 1,
            "steps" : step + 1,
            "totalEnvironmentReward" : totalEnvironmentReward,
            "totalIntrinsicReward" : totalIntrinsicReward,
            "totalLearningReward" : (
                totalEnvironmentReward + totalIntrinsicReward
            ),
            "epsilon" : epsilon,
            "completed" : done and not environment.playerDied,
            "died" : environment.playerDied
        })

    return agent, trainingResults
