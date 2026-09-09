import csv
import matplotlib.pyplot as plt

from helpers.agentHelper import saveTrainingResults
from qlearning.qLearningAgent import qLearningTraining, evaluateQLearning
from qlearning.qLearningResults import movingAverage
from sarsa.sarsaAgent import sarsaTraining, evaluateSARSA


def createTrainingGraph (trainingResults, graphTitle, fileName) :
    episodes = []
    steps = []
    totalRewards = []
    completedValues = []
    deathValues = []
    epsilonValues = []

    for result in trainingResults :
        episodes.append(result["episode"])
        steps.append(result["steps"])
        totalRewards.append(result["totalReward"])
        epsilonValues.append(result["epsilon"])

        if result["completed"] :
            completedValues.append(1)
        else :
            completedValues.append(0)

        if result["died"] :
            deathValues.append(1)
        else :
            deathValues.append(0)

    averageSteps = movingAverage(steps)
    averageRewards = movingAverage(totalRewards)
    averageSuccessRate = movingAverage(completedValues)
    averageDeathRate = movingAverage(deathValues)

    plt.figure(figsize = (10, 10))

    plt.subplot(3, 1, 1)
    plt.plot(episodes, averageSteps, color = "#2878B5", label = "50-Episode Average Steps")
    plt.title(graphTitle + "\nSeed 42 | Step -0.01 | Death -1 | Completion +20", fontsize = 11)
    plt.ylabel("Steps")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(episodes, averageRewards, color = "#2878B5", label = "50-Episode Average Reward")
    plt.ylabel("Environment Reward")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(episodes, averageSuccessRate, color = "#2878B5", label = "50-Episode Success Rate")
    plt.plot(episodes, averageDeathRate, color = "#D88028", linestyle = "--", label = "50-Episode Death Rate")
    plt.plot(episodes, epsilonValues, color = "#697A39", linestyle = ":", label = "Epsilon")
    plt.xlabel("Episode")
    plt.ylabel("Rate")
    plt.legend()
    plt.grid(True)

    graphPath = f"results/{fileName}.png"
    plt.tight_layout()
    plt.savefig(graphPath)
    plt.close()

    return graphPath

if __name__ == "__main__" :
    for level in [4, 5] :
        qLearningAgent, qLearningResults = qLearningTraining(level = level)
        sarsaAgent, sarsaResults = sarsaTraining(level = level)

        qLearningEvaluation = evaluateQLearning(
            qLearningAgent,
            level = level
        )

        sarsaEvaluation = evaluateSARSA(
            sarsaAgent,
            level = level
        )

        qLearningFileName = f"qLearningLevel{level}Training"
        sarsaFileName = f"sarsaLevel{level}Training"

        qLearningCsvPath = saveTrainingResults(
            qLearningResults,
            level,
            1
        )

        qLearningGraphPath = createTrainingGraph(
            qLearningResults,
            f"Q-Learning Level {level} Training",
            qLearningFileName
        )

        sarsaCsvPath = saveTrainingResults(
            sarsaResults,
            level,
            2
        )

        sarsaGraphPath = createTrainingGraph(
            sarsaResults,
            f"SARSA Level {level} Training",
            sarsaFileName
        ) 
        
        print(f"\nQ-Learning Level {level} Evaluation")
        print(f"CSV: {qLearningCsvPath}")
        print(f"Graph: {qLearningGraphPath}")
        print(f"Route: {qLearningEvaluation['route']}")
        print(f"Steps: {qLearningEvaluation['steps']}")
        print(f"Reward: {qLearningEvaluation['totalReward']}")
        print(f"Completed: {qLearningEvaluation['completed']}")
        print(f"Died: {qLearningEvaluation['died']}")

        print(f"\nSARSA Level {level} Evaluation")
        print(f"CSV: {sarsaCsvPath}")
        print(f"Graph: {sarsaGraphPath}")
        print(f"Route: {sarsaEvaluation['route']}")
        print(f"Steps: {sarsaEvaluation['steps']}")
        print(f"Reward: {sarsaEvaluation['totalReward']}")
        print(f"Completed: {sarsaEvaluation['completed']}")
        print(f"Died: {sarsaEvaluation['died']}")
