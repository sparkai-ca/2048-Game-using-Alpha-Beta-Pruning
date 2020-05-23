import time
from BaseAI import BaseAI


class PlayerAI(BaseAI):
    __x = float('inf')

    def __init__(self):
        self.depth=100

    def minimax(self, grid, depth, alpha, beta, maximizingPlayer):
        self.end = time.clock()
        if depth == 0 or self.end-self.start >= 0.15/self.lenmoves*self.movenum:
            return self.heuristic(grid)
        if maximizingPlayer:
            return self.maximize(grid,depth,alpha,beta)
        else:
            return self.minimize(grid,depth,alpha,beta)

    def maximize(self,grid,depth,alpha,beta):
        utility_val = -self.__x
        moves = grid.getAvailableMoves()
        for move in moves:
            child = grid.clone()
            child.move(move)
            utility_val = max(utility_val, self.minimax(child, depth - 1, alpha, beta, False))
            alpha = max(utility_val, alpha)
            if beta <= alpha:
                break
        return utility_val

    def minimize(self,grid,depth,alpha,beta):
        utility_val = self.__x
        av_cells = grid.getAvailableCells()
        spawns = av_cells + av_cells
        for spawn in spawns:
            childNode = grid.clone()
            insertVal = 2
            childNode.insertTile(spawn, insertVal)
            utility_val = min(utility_val, self.minimax(childNode, depth - 1, alpha, beta, True))
            beta = min(utility_val, beta)
            if beta <= alpha:
                break
        return utility_val

    def heuristic(self, grid):
        h = 0
        gsum = 0
        frow = 0
        srow = 0
        diff = 0
        gc = grid.getAvailableCells()
        m = grid.map

        for x in range(grid.size):
            for y in range(grid.size):
                v = m[x][y]
                gsum += v
                if x==0:
                    frow += v
                if x==1:
                    srow += v
        for y in range(grid.size-1):
            if m[0][y] > m[0][y+1]:
                diff += frow/4
        h += (diff/gsum) * 40
        h += frow / gsum * 40
        h += srow / gsum * 20
        h += len(gc) / 12 * 40
        return h

    def getMove(self, grid):

        moves = grid.getAvailableMoves()
        self.start = time.clock()
        self.movenum = 0
        self.lenmoves = len(moves)
        fn = 0
        best_move = moves[0]
        for move in moves:
            self.movenum += 1
            newGrid = grid.clone()
            newGrid.move(move)
            move_val = self.minimax(newGrid, self.depth, -self.__x, self.__x, False)
            if move_val > fn:
                best_move = move
                fn = move_val
        return best_move if best_move in moves else None
