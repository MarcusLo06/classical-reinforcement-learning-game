import csv
import matplotlib.pyplot as plt

from qlearning.qLearningTraining import qLearningTraining, evaluateQLearning
from qlearning.qLearningResults import movingAverage
from sarsa.sarsaTraining import sarsaTraining, evaluateSARSA

def saveTrainingResults (trainingResults, fileName) :
    fieldNames = list(trainingResults[0].keys())
    csvPath = f"results/{fileName}.csv"

    with open(csvPath, "w", newline = "", encoding = "utf-8") as csvFile :
        writer = csv.DictWriter(csvFile, fieldnames = fieldNames)
        writer.writeheader()
        writer.writerows(trainingResults)

    return csvPath

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
    maximumReward = [1] * len(episodes)

    plt.figure(figsize = (10, 10))

    plt.subplot(3, 1, 1)
    plt.plot(episodes, averageSteps, label = "50-Episode Average Steps")
    plt.title(graphTitle)
    plt.ylabel("Steps")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(episodes, averageRewards, label = "50-Episode Average Reward")
    plt.plot(episodes, maximumReward, label = "Maximum Reward")
    plt.ylabel("Reward")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(episodes, averageSuccessRate, label = "50-Episode Success Rate")
    plt.plot(episodes, averageDeathRate, label = "50-Episode Death Rate")
    plt.plot(episodes, epsilonValues, label = "Epsilon")
    plt.xlabel("Episode")
    plt.ylabel("Rate")
    plt.legend()
    plt.grid(True)

    graphPath = f"results/{fileName}.png"
    plt.savefig(graphPath)

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
            qLearningFileName
        )

        qLearningGraphPath = createTrainingGraph(
            qLearningResults,
            f"Q-Learning Level {level} Training",
            qLearningFileName
        )

        sarsaCsvPath = saveTrainingResults(
            sarsaResults,
            sarsaFileName
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
