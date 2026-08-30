from classes.qTable import QTable
from helpers.learningPolicy import epsilonGreedy

class QLearning : 
    def __init__(self, alpha, gamma):
        self.qTable = QTable()
        self.alpha = alpha
        self.gamma = gamma
        
    def selectAction(self, state, epsilon):
        return epsilonGreedy(self.qTable, state, epsilon)
    
    def update(
        self,
        state,
        action,
        reward,
        nextState,
        done
    ) :
        currentValue = self.qTable.get(state, action)
        
        if done :
            target = reward
        
        else :
            target = reward + (self.gamma * self.qTable.bestValue(nextState))
            
        newValue = currentValue + (self.alpha * (target - currentValue))
        
        self.qTable.set(state, action, newValue)
