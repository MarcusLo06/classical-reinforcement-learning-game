import csv
import matplotlib.pyplot as plt

from qlearning.qLearningLv6Training import qLearningLv6Training
from qlearning.qLearningResults import movingAverage

def saveTrainingResults (trainingResults, fileName) :
    fieldNames = list(trainingResults[0].keys())
    csvPath = f"results/{fileName}.csv"

    with open(csvPath, "w", newline = "", encoding = "utf-8") as csvFile :
        writer = csv.DictWriter(csvFile, fieldnames = fieldNames)
        writer.writeheader()
        writer.writerows(trainingResults)

    return csvPath

def getTrainingValues (trainingResults, valueName) :
    values = []

    for result in trainingResults :
        values.append(result[valueName])

    return values

def createComparisonGraph (
    withoutIntrinsicResults,
    withIntrinsicResults
) :
    episodes = getTrainingValues(
        withoutIntrinsicResults,
        "episode"
    )

    averageRewardsWithoutIntrinsic = movingAverage(
        getTrainingValues(
            withoutIntrinsicResults,
            "totalEnvironmentReward"
        )
    )

    averageRewardsWithIntrinsic = movingAverage(
        getTrainingValues(
            withIntrinsicResults,
            "totalEnvironmentReward"
        )
    )

    averageSuccessWithoutIntrinsic = movingAverage(
        getTrainingValues(
            withoutIntrinsicResults,
            "completed"
        )
    )

    averageSuccessWithIntrinsic = movingAverage(
        getTrainingValues(
            withIntrinsicResults,
            "completed"
        )
    )

    averageStepsWithoutIntrinsic = movingAverage(
        getTrainingValues(
            withoutIntrinsicResults,
            "steps"
        )
    )

    averageStepsWithIntrinsic = movingAverage(
        getTrainingValues(
            withIntrinsicResults,
            "steps"
        )
    )

    maximumReward = [1] * len(episodes)

    plt.figure(figsize = (10, 10))

    plt.subplot(3, 1, 1)
    plt.plot(
        episodes,
        averageRewardsWithoutIntrinsic,
        label = "Without Intrinsic Reward"
    )
    plt.plot(
        episodes,
        averageRewardsWithIntrinsic,
        label = "With Intrinsic Reward"
    )
    plt.plot(episodes, maximumReward, label = "Maximum Reward")
    plt.title("Q-Learning Level 6 Intrinsic Reward Comparison")
    plt.ylabel("Environment Reward")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(
        episodes,
        averageSuccessWithoutIntrinsic,
        label = "Without Intrinsic Reward"
    )
    plt.plot(
        episodes,
        averageSuccessWithIntrinsic,
        label = "With Intrinsic Reward"
    )
    plt.ylabel("Success Rate")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(
        episodes,
        averageStepsWithoutIntrinsic,
        label = "Without Intrinsic Reward"
    )
    plt.plot(
        episodes,
        averageStepsWithIntrinsic,
        label = "With Intrinsic Reward"
    )
    plt.xlabel("Episode")
    plt.ylabel("Average Steps")
    plt.legend()
    plt.grid(True)

    graphPath = "results/qLearningLevel6IntrinsicComparison.png"
    plt.savefig(graphPath)

    return graphPath

if __name__ == "__main__" :
    withoutIntrinsicAgent, withoutIntrinsicResults = (
        qLearningLv6Training(useIntrinsicReward = False)
    )

    withIntrinsicAgent, withIntrinsicResults = (
        qLearningLv6Training(useIntrinsicReward = True)
    )

    withoutIntrinsicCsvPath = saveTrainingResults(
        withoutIntrinsicResults,
        "qLearningLevel6WithoutIntrinsic"
    )

    withIntrinsicCsvPath = saveTrainingResults(
        withIntrinsicResults,
        "qLearningLevel6WithIntrinsic"
    )

    graphPath = createComparisonGraph(
        withoutIntrinsicResults,
        withIntrinsicResults
    )

    print(f"Without intrinsic reward CSV: {withoutIntrinsicCsvPath}")
    print(f"With intrinsic reward CSV: {withIntrinsicCsvPath}")
    print(f"Comparison graph: {graphPath}")
