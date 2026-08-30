from classes.qTable import QTable
from helpers.learningPolicy import epsilonGreedy


class SARSA:
    def __init__(self, alpha, gamma):
        self.qTable = QTable()
        self.alpha = alpha
        self.gamma = gamma

    def selectAction(self, state, epsilon):
        return epsilonGreedy(
            self.qTable,
            state,
            epsilon
        )

    def update(
        self,
        state,
        action,
        reward,
        nextState,
        nextAction,
        done
    ):
        currentValue = self.qTable.get(state, action)

        if done:
            target = reward
        else:
            # Use the next action selected by the current policy
            target = reward + (
                self.gamma
                * self.qTable.get(nextState, nextAction)
            )

        newValue = currentValue + (
            self.alpha
            * (target - currentValue)
        )

        self.qTable.set(state, action, newValue)
