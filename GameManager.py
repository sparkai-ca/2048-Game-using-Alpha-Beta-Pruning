from Grid       import Grid
from ComputerAI import ComputerAI
from Displayer  import Displayer
from PlayerAI   import PlayerAI
import random
import time
from itertools import chain
import math

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 1
allowance = 0.1

class GameManager:
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.displayer  = None
        self.over       = False

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
        else:
            while time.perf_counter() - self.prevTime < timeLimit + allowance:
                pass

            self.prevTime = time.perf_counter()

    def start(self):
        for i in range(self.initTiles):
            self.insertRandomTile()

        self.displayer.display(self.grid)

        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        self.prevTime = time.perf_counter()

        timecount = 0

        while not self.isGameOver() and not self.over:
            timecount += 1
            print(timecount, "th TURN:")
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()
            move = None
            if turn == PLAYER_TURN:
                print("Player's Turn:", end="")
                move = self.playerAI.getMove(gridCopy)
                print(actionDic[move])

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        maxTile = self.grid.getMaxTile()
                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True
                else:
                    print("Invalid PlayerAI Move - 1")
                    self.over = True

                print(self.evaluator(self.top5()))
            else:
                print("Computer's turn:")
                move = self.computerAI.getMove(gridCopy)

                # Validate Move
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True

            if not self.over:
                self.displayer.display(self.grid)

            # Exceeding the Time Allotted for Any Turn Terminates the Game
            self.updateAlarm(time.perf_counter())

            turn = 1 - turn
        print(maxTile)

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        random.seed(218)
        if random.randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

    def insertRandomTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        random.seed(218)
        cell = cells[random.randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

    def sumOfScore(self):
        sum = 0
        for i in range(4):
            for j in range(4):
                sum += self.grid.map[i][j]
        return sum
        
    #Modified part for evaluation:
    def top5(self):
        flatten_list = list(chain.from_iterable(self.grid.map))
        flatten_list.sort(reverse=True)
        return flatten_list[0:5]
    
    def evaluator(self, res):
        score = 10
        std = [2048, 2048, 1024, 1024, 1024]
        for i in range(5):
            if res[i] == 0:
                score -= 10
            elif res[i] > std[i]:
                score += 2 * math.log2(std[i]/res[i])
            else:
                score -= 0.5 * math.log2(std[i]/res[i])
        return score




def main():
    gameManager = GameManager()
    playerAI  	= PlayerAI()
    computerAI  = ComputerAI()
    displayer 	= Displayer()
    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)

    gameManager.start()
    print("Total score: ", gameManager.sumOfScore())
    print("Your score in Assignment#2: ", gameManager.evaluator(gameManager.top5()))

if __name__ == '__main__':
    main()
