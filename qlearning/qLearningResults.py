import csv
import matplotlib.pyplot as plt

from qlearning.qLearningTraining import qLearningTraining

def movingAverage (values, window = 50) :
    averages = []
    
    for i in range(len(values)) :
        start = max(0, i - window + 1)
        currentValue = values[start : i + 1]
        
        averages.append (
            sum(currentValue) / len(currentValue)
        )
        
    return averages

def saveTrainingResults (trainingResults) :
    fieldNames = [
        "episode",
        "steps",
        "totalReward",
        "epsilon",
        "completed"
    ]

    csvPath = "results/qLearningLevel0Training.csv"

    with open(csvPath, "w", newline = "", encoding = "utf-8") as csvFile :
        writer = csv.DictWriter(csvFile, fieldnames = fieldNames)
        writer.writeheader()
        writer.writerows(trainingResults)

    return csvPath

def createTrainingGraph (trainingResults) :
    episodes = []
    steps = []
    completedValues = []
    epsilonValues = []

    for result in trainingResults :
        episodes.append(result["episode"])
        steps.append(result["steps"])
        epsilonValues.append(result["epsilon"])

        if result["completed"] :
            completedValues.append(1)
        else :
            completedValues.append(0)

    averageSteps = movingAverage(steps)
    averageSuccessRate = movingAverage(completedValues)
    optimalSteps = [18] * len(episodes)

    plt.figure(figsize = (10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(episodes, averageSteps, label = "50-Episode Average Steps")
    plt.plot(episodes, optimalSteps, label = "Optimal Steps")
    plt.title("Q-Learning Level 0 Training")
    plt.ylabel("Steps")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(episodes, averageSuccessRate, label = "50-Episode Success Rate")
    plt.plot(episodes, epsilonValues, label = "Epsilon")
    plt.xlabel("Episode")
    plt.ylabel("Rate")
    plt.legend()
    plt.grid(True)

    graphPath = "results/qLearningLevel0Training.png"
    plt.savefig(graphPath)

    return graphPath

if __name__ == "__main__" :
    qLearningAgent, trainingResults = qLearningTraining(level = 0)
    csvPath = saveTrainingResults(trainingResults)
    graphPath = createTrainingGraph(trainingResults)
    
    print(f"Training result saved to: {csvPath}")
    print(f"Training graph saved to: {graphPath}")
