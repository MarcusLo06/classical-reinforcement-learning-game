from classes.worldEnvironment import ALL_ACTIONS

class QTable :
    def __init__(self) :
        self.q ={}
        
    def get(self, state, action) :
        return self.q.get((state, action), 0.0)
    
    def set(self, state, action, value) :
        self.q[(state, action)] = value

    def bestValue(self, state) :
        return max(
            self.get(state, action) for action in ALL_ACTIONS
        )
        
    def bestActions(self, state) :
        values = [
            self.get(state, action) for action in ALL_ACTIONS
        ]
        
        highestValue = max(values)
        
        return [
            action for action, value in zip(ALL_ACTIONS, values)
            if value == highestValue
        ]
