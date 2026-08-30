# Movement choices available to the agent
import importlib

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

MOVE_DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

ALL_ACTIONS = [UP, RIGHT, DOWN, LEFT]

class WorldEnvironment: 
    def __init__(self, level = 0):
        self.level = level
        self.levelData = importlib.import_module(f"resources.level{level}")
        self.rows = self.levelData.MAP_ROWS
        self.columns = self.levelData.MAP_COLS
        self.levelMap = self.levelData.LEVEL_MAP
        self.playerSpawn = self.levelData.PLAYER_SPAWN
        self.applePositions = self.levelData.APPLE_POS
        self.keyPositions = self.levelData.KEY_POS
        self.chestPositions = self.levelData.CHEST_POS
        self.hazardPositions = getattr(
            self.levelData,
            "HAZARD_POS",
            []
        )
        self.reset()

    # Restore level and return the initial state
    def reset(self):
        self.playerPosition = tuple(self.playerSpawn)
        self.remainingApples = set(self.applePositions)
        self.remainingKeys = set(self.keyPositions)
        self.unopenedChests = set(self.chestPositions)
        self.keyCount = 0
        self.done = False
        self.stepCount = 0
        self.playerDied = False
        return self.getState()

    # Lv 0 & 1 use position, while later Lvs also use item states
    def getState (self) :
        if self.level <= 1 :
            return self.playerPosition

        appleState = self.getItemState(
            self.applePositions,
            self.remainingApples
        )

        keyState = self.getItemState(
            self.keyPositions,
            self.remainingKeys
        )

        chestState = self.getItemState(
            self.chestPositions,
            self.unopenedChests
        )

        return (
            self.playerPosition,
            appleState,
            keyState,
            chestState,
            self.keyCount
        )
    
    def getItemState (self, itemPositions, remainingItems) :
        itemState = 0
        
        for i, position in enumerate(itemPositions) :
            if position not in remainingItems : 
                itemState += 2 ** i
        
        return itemState
    
    def canMoveTo(self, position):
        x , y = position
        
        if x < 0 or x >= self.columns :
            return False
        
        if y < 0 or y >= self.rows : 
            return False
        
        return self.levelMap[x][y] == 0
    
    def step(self, action):
        moveX, moveY = MOVE_DIRECTIONS[action]
        x, y = self.playerPosition
        nextPosition = (x + moveX, y + moveY)
        
        if self.canMoveTo(nextPosition):
            self.playerPosition = nextPosition

        self.stepCount += 1
        
        if self.playerPosition in self.hazardPositions :
            self.playerDied = True
            self.done = True
            
            return self.getState(), 0, self.done

        reward = self.collectItem()

        self.done = (
            len(self.remainingApples) == 0
            and len(self.unopenedChests) == 0
        )

        return self.getState(), reward, self.done
    
    def collectItem(self): 
        reward = 0
        
        if self.playerPosition in self.remainingApples:
            self.remainingApples.remove(self.playerPosition)
            
            reward += 1
            
        if self.playerPosition in self.remainingKeys:
            self.remainingKeys.remove(self.playerPosition)
            self.keyCount += 1
            
        if (self.playerPosition in self.unopenedChests and self.keyCount > 0):
            self.unopenedChests.remove(self.playerPosition)
            self.keyCount -= 1
            
            reward += 2
            
        return reward 
