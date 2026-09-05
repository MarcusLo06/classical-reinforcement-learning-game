import csv
import matplotlib.pyplot as plt

from helpers.agentHelper import saveTrainingResults
from sarsa.sarsaTraining import sarsaTraining, evaluateSARSA

def movingAverage (values, window = 50) :
    averages = []
    
    for i in range(len(values)) :
        start = max(0, i - window + 1)
        currentValue = values[start : i + 1]
        
        averages.append (
            sum(currentValue) / len(currentValue)
        ) 
        
    return averages


def createTrainingGraph (trainingResults) :
    episodes = []
    steps = []
    completedValues = []
    diedValues = []
    epsilonValues = []

    for result in trainingResults :
        episodes.append(result["episode"])
        steps.append(result["steps"])
        epsilonValues.append(result["epsilon"])

        if result["completed"] :
            completedValues.append(1)
        else :
            completedValues.append(0)

        if result["died"] :
            diedValues.append(1)
        else :
            diedValues.append(0)

    averageSteps = movingAverage(steps)
    averageSuccessRate = movingAverage(completedValues)
    averageDeathRate = movingAverage(diedValues)

    plt.figure(figsize = (10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(episodes, averageSteps, label = "50-Episode Average Steps")
    plt.title("SARSA Level 1 Training")
    plt.ylabel("Steps")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(episodes, averageSuccessRate, label = "50-Episode Success Rate")
    plt.plot(episodes, averageDeathRate, label = "50-Episode Death Rate")
    plt.plot(episodes, epsilonValues, label = "Epsilon")
    plt.xlabel("Episode")
    plt.ylabel("Rate")
    plt.legend()
    plt.grid(True)

    graphPath = "results/sarsaLevel1Training.png"
    plt.savefig(graphPath)

    return graphPath

if __name__ == "__main__" :
    sarsaAgent, trainingResults = sarsaTraining(level = 1)
    csvPath = saveTrainingResults(trainingResults, 1, 2)
    graphPath = createTrainingGraph(trainingResults)
    evaluationResult = evaluateSARSA(sarsaAgent, level = 1)

    print(f"Training result saved to: {csvPath}")
    print(f"Training graph saved to: {graphPath}")
    print(f"Evaluation route: {evaluationResult['route']}")
    print(f"Evaluation steps: {evaluationResult['steps']}")
    print(f"Evaluation reward: {evaluationResult['totalReward']}")
    print(f"Evaluation completed: {evaluationResult['completed']}")
    print(f"Evaluation died: {evaluationResult['died']}")
