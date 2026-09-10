from qlearning.qLearningAgent import qLearningTraining, evaluateQLearning
from sarsa.sarsaAgent import sarsaTraining, evaluateSARSA
from helpers.agentHelper import saveTrainingResults
from evaluation.level4And5Results import createTrainingGraph

if __name__ == "__main__" :
    qLearningAgent, qLearningResults = qLearningTraining(level = 1)
    sarsaAgent, sarsaResults = sarsaTraining(level = 1)

    saveTrainingResults(qLearningResults, 1, 1)
    saveTrainingResults(sarsaResults, 1, 2)
    createTrainingGraph(
        qLearningResults,
        "Q-Learning Level 1 Training",
        "qLearningLevel1Training"
    )
    createTrainingGraph(
        sarsaResults,
        "SARSA Level 1 Training",
        "sarsaLevel1Training"
    )

    qLearningEvaluation = evaluateQLearning(qLearningAgent, level = 1)
    sarsaEvaluation = evaluateSARSA(sarsaAgent, level = 1)
    
    print("\nQ-Learning Level 1 Evaluation")
    print(f"Route: {qLearningEvaluation['route']}")
    print(f"Steps: {qLearningEvaluation['steps']}")
    print(f"Reward: {qLearningEvaluation['totalReward']}")
    print(f"Completed: {qLearningEvaluation['completed']}")
    print(f"Died: {qLearningEvaluation['died']}")

    print("\nSARSA Level 1 Evaluation")
    print(f"Route: {sarsaEvaluation['route']}")
    print(f"Steps: {sarsaEvaluation['steps']}")
    print(f"Reward: {sarsaEvaluation['totalReward']}")
    print(f"Completed: {sarsaEvaluation['completed']}")
    print(f"Died: {sarsaEvaluation['died']}")
