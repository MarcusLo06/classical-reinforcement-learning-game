"""Regenerate Part I artifacts with the current code and fixed configuration.

Use --output-dir to stage results without changing the project's results folder.
Each algorithm/level is trained once. Evaluation never updates Q-values.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import pickle
import random
import subprocess
from collections import deque

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from classes.worldEnvironment import WorldEnvironment, MOVE_DIRECTIONS
from evaluation.level4And5Results import createTrainingGraph
from evaluation.level6IntrinsicResults import createComparisonGraph
from helpers.agentHelper import saveTrainingResults, saveQTable
from helpers.loadSetting import loadSetting
from qlearning.qLearningAgent import qLearningTraining
from qlearning.qLearningLv6Training import qLearningLv6Training
from sarsa.sarsaAgent import sarsaTraining


def getSourceHashes (projectFolder) :
    paths = list(projectFolder.rglob("*.py")) + [projectFolder / "classicalRLSettings.json"]
    return {
        str(path.relative_to(projectFolder)) : hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(paths)
        if ".git" not in path.parts and "__pycache__" not in path.parts
    }


def evaluateSavedAgent (agent, level, seed, maxSteps) :
    random.seed(seed)
    environment = WorldEnvironment(level)
    state = environment.reset()
    route = [environment.playerPosition]
    totalReward = 0
    done = False
    for step in range(maxSteps) :
        action = agent.selectAction(state, epsilon = 0.0)
        state, reward, done, direction = environment.step(action)
        totalReward += reward
        route.append(environment.playerPosition)
        if done :
            break
    return {
        "seed" : seed,
        "completed" : done and not environment.playerDied,
        "died" : environment.playerDied,
        "steps" : environment.stepCount,
        "totalEnvironmentReward" : round(totalReward, 8),
        "applesCollected" : len(environment.applePositions) - len(environment.remainingApples),
        "keysCollected" : len(environment.keyPositions) - len(environment.remainingKeys),
        "chestsOpened" : len(environment.chestPositions) - len(environment.unopenedChests),
        "keysHeld" : environment.keyCount,
        "route" : route
    }


def shortestStaticPath (level) :
    environment = WorldEnvironment(level)
    if environment.monsterPositions or len(environment.applePositions) != 1 or environment.chestPositions :
        return None
    goal = tuple(environment.applePositions[0])
    start = environment.playerPosition
    queue = deque([(start, 0)])
    visited = {start}
    while queue :
        position, distance = queue.popleft()
        if position == goal :
            return distance
        for moveX, moveY in MOVE_DIRECTIONS :
            nextPosition = (position[0] + moveX, position[1] + moveY)
            if nextPosition not in visited and environment.canMoveTo(nextPosition) and nextPosition not in environment.hazardPositions :
                visited.add(nextPosition)
                queue.append((nextPosition, distance + 1))
    return None


def recordRun (agent, trainingResults, level, modelPath, settings, csvPath, graphPath) :
    expectedEpisodes = settings["monsterEpisodes"] if level in [4, 5] else settings["episodes"]
    assert [row["episode"] for row in trainingResults] == list(range(1, expectedEpisodes + 1))
    with Path(modelPath).open("rb") as modelFile :
        savedTable = pickle.load(modelFile)
    assert savedTable.q == agent.qTable.q
    with Path(csvPath).open(newline = "", encoding = "utf-8") as csvFile :
        savedRows = list(csv.DictReader(csvFile))
    assert len(savedRows) == expectedEpisodes
    for saved, original in zip(savedRows, trainingResults) :
        for field, value in original.items() :
            assert saved[field] == str(value), (csvPath, field)
    evaluations = [evaluateSavedAgent(agent, level, seed, settings["maxStepsPerEpisode"]) for seed in range(100)]
    tail = trainingResults[-300:]
    rewardField = "totalEnvironmentReward" if level == 6 else "totalReward"
    return {
        "model" : modelPath, "csv" : csvPath, "graph" : graphPath,
        "trainingEpisodes" : expectedEpisodes,
        "last300TrainingSuccessPercent" : sum(row["completed"] for row in tail) / len(tail) * 100,
        "last300TrainingAverageSteps" : sum(row["steps"] for row in tail) / len(tail),
        "last300TrainingAverageEnvironmentReward" : sum(row[rewardField] for row in tail) / len(tail),
        "evaluationSuccessCount" : sum(row["completed"] for row in evaluations),
        "evaluationCount" : len(evaluations),
        "evaluationSteps" : sorted({row["steps"] for row in evaluations}),
        "seed42Evaluation" : evaluations[42],
        "shortestStaticPathSteps" : shortestStaticPath(level)
    }


def main () :
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type = Path)
    args = parser.parse_args()
    projectFolder = Path(__file__).resolve().parents[1]
    outputFolder = (args.output_dir or projectFolder).resolve()
    outputFolder.mkdir(parents = True, exist_ok = True)
    sourceHashes = getSourceHashes(projectFolder)
    sourceCommit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd = projectFolder, text = True).strip()
    settings = loadSetting()
    os.chdir(outputFolder)
    Path("results").mkdir(exist_ok = True)
    manifest = {"sourceCommit" : sourceCommit, "sourceHashes" : sourceHashes, "settings" : settings, "evaluationEpsilon" : 0.0, "runs" : {}}
    for level in range(6) :
        for name, train, algorithm in [("qLearning", qLearningTraining, 1), ("sarsa", sarsaTraining, 2)] :
            # Refresh the existing legacy SARSA Level 0 model too, although the GUI does not offer it.
            agent, trainingResults = train(level = level)
            csvPath = saveTrainingResults(trainingResults, level, algorithm)
            label = "Q-Learning" if algorithm == 1 else "SARSA"
            graphPath = createTrainingGraph(trainingResults, f"{label} Level {level} Training", f"{name}Level{level}Training")
            modelPath = f"results/{name.lower()}qTable_lvl{level}.pkl"
            result = recordRun(agent, trainingResults, level, modelPath, settings, csvPath, graphPath)
            manifest["runs"][f"{name}Level{level}"] = result
            print(name, level, "evaluation:", result["seed42Evaluation"]["steps"], result["seed42Evaluation"]["completed"], "last300:", round(result["last300TrainingSuccessPercent"], 3), flush = True)
            plt.close("all")
    intrinsicResults = {}
    for useIntrinsic in [False, True] :
        agent, rows = qLearningLv6Training(useIntrinsicReward = useIntrinsic)
        suffix = "WithIntrinsic" if useIntrinsic else "WithoutIntrinsic"
        csvPath = f"results/qLearningLevel6{suffix}.csv"
        with Path(csvPath).open("w", newline = "", encoding = "utf-8") as csvFile :
            writer = csv.DictWriter(csvFile, fieldnames = list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        modelPath = "results/qlearningqTable_lvl6.pkl" if useIntrinsic else "results/qlearningqTable_lvl6WithoutIntrinsic.pkl"
        with Path(modelPath).open("wb") as modelFile :
            pickle.dump(agent.qTable, modelFile)
        intrinsicResults[useIntrinsic] = rows
        result = recordRun(agent, rows, 6, modelPath, settings, csvPath, "results/qLearningLevel6IntrinsicComparison.png")
        manifest["runs"][f"qLearningLevel6{suffix}"] = result
        print("Level 6", suffix, "evaluation:", result["seed42Evaluation"]["steps"], result["seed42Evaluation"]["completed"], flush = True)
    createComparisonGraph(intrinsicResults[False], intrinsicResults[True])
    manifest["level6EnvironmentMetricsIdentical"] = all(
        without[field] == withBonus[field]
        for without, withBonus in zip(intrinsicResults[False], intrinsicResults[True])
        for field in ["steps", "completed", "totalEnvironmentReward"]
    )
    assert sourceHashes == getSourceHashes(projectFolder), "Source changed while training. Do not publish these results."
    artifacts = sorted(path for path in Path("results").iterdir() if path.suffix in [".csv", ".pkl", ".png"])
    manifest["artifactHashes"] = {str(path) : hashlib.sha256(path.read_bytes()).hexdigest() for path in artifacts}
    Path("results/trainingManifest.json").write_text(json.dumps(manifest, indent = 2), encoding = "utf-8")
    print("Verified", len(manifest["runs"]), "runs and", len(artifacts), "artifacts. Source files unchanged.", flush = True)


if __name__ == "__main__" :
    main()
