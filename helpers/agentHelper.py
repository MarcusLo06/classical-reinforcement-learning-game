import pickle, csv

def saveQTable(agent, level: int):
    with open(f"results/qTable_lvl{level}.pkl", "wb") as f:
        pickle.dump(agent.qTable, f)  # Assuming agent.qTable is your Q-value dict

def loadQTable(agent, level: int):
    with open(f"results/qTable_lvl{level}.pkl", "rb") as f:
        agent.qTable = pickle.load(f)
    return agent

def loadTrainingResults(level: int = 0):
    csvPath="results/qLearningLevel" + str(level) + "Training.csv"
    results = []
    with open(csvPath, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            results.append({
                "episode": int(row["episode"]),
                "steps": int(row["steps"]),
                "totalReward": float(row["totalReward"]),
                "epsilon": float(row["epsilon"]),
                "completed": row["completed"].lower() in ("true", "1"),
                "died": row["died"].lower() in ("true", "1")
            })
    return results

# RLAlgor == 1: Q Learning, == 2: SARSA
def saveTrainingResults (trainingResults, level: int, RLAlgor: int, bonusText: str = "") :
    fieldNames = [
        "episode",
        "steps",
        "totalReward",
        "epsilon",
        "completed",
        "died"
    ]

    if RLAlgor == 1:
        csvPath = "results/qLearningLevel" + str(level) + "Training" + bonusText + ".csv"
    elif RLAlgor == 2:
        csvPath = "results/sarsaLevel" + str(level) + "Training" + bonusText + ".csv"


    with open(csvPath, "w", newline = "", encoding = "utf-8") as csvFile :
        writer = csv.DictWriter(csvFile, fieldnames = fieldNames)
        writer.writeheader()
        writer.writerows(trainingResults)

    return csvPath
