import csv
import matplotlib.pyplot as plt

from helpers.agentHelper import saveQTable
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

    curvesOverlap = all(
        withoutResult[field] == withResult[field]
        for withoutResult, withResult in zip(withoutIntrinsicResults, withIntrinsicResults)
        for field in ["steps", "completed", "totalEnvironmentReward"]
    )

    plt.figure(figsize = (10, 10))

    plt.subplot(3, 1, 1)
    plt.plot(
        episodes,
        averageRewardsWithoutIntrinsic,
        color = "#2878B5",
        linewidth = 2.5,
        label = "Without Intrinsic Reward"
    )
    plt.plot(
        episodes,
        averageRewardsWithIntrinsic,
        color = "#D88028",
        linestyle = "--",
        label = "With Intrinsic Reward"
    )
    plt.title("Q-Learning Level 6 Intrinsic Reward Comparison\nSeed 42 | 50-episode averages | Step -0.01 | Death -1 | Completion +20", fontsize = 11)
    if curvesOverlap :
        plt.gcf().text(0.5, 0.01, "Both curves overlap: identical environment metrics in this seeded run.", ha = "center")
    plt.ylabel("Environment Reward")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(
        episodes,
        averageSuccessWithoutIntrinsic,
        color = "#2878B5",
        linewidth = 2.5,
        label = "Without Intrinsic Reward"
    )
    plt.plot(
        episodes,
        averageSuccessWithIntrinsic,
        color = "#D88028",
        linestyle = "--",
        label = "With Intrinsic Reward"
    )
    plt.ylabel("Success Rate")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(
        episodes,
        averageStepsWithoutIntrinsic,
        color = "#2878B5",
        linewidth = 2.5,
        label = "Without Intrinsic Reward"
    )
    plt.plot(
        episodes,
        averageStepsWithIntrinsic,
        color = "#D88028",
        linestyle = "--",
        label = "With Intrinsic Reward"
    )
    plt.xlabel("Episode")
    plt.ylabel("Average Steps")
    plt.legend()
    plt.grid(True)

    graphPath = "results/qLearningLevel6IntrinsicComparison.png"
    plt.tight_layout(rect = (0, 0.03, 1, 1))
    plt.savefig(graphPath)
    plt.close()

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

    saveQTable(withIntrinsicAgent, 6, 1)

    graphPath = createComparisonGraph(
        withoutIntrinsicResults,
        withIntrinsicResults
    )

    print(f"Without intrinsic reward CSV: {withoutIntrinsicCsvPath}")
    print(f"With intrinsic reward CSV: {withIntrinsicCsvPath}")
    print("With intrinsic reward Q-table: results/qlearningqTable_lvl6.pkl")
    print(f"Comparison graph: {graphPath}")
