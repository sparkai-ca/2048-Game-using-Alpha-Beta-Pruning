import random
from BaseAI import BaseAI

class ComputerAI(BaseAI):
    def getMove(self, grid):
        cells = grid.getAvailableCells()
        random.seed(218)
        return cells[random.randint(0, len(cells) - 1)] if cells else None
