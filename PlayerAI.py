from random import randint
from BaseAI import BaseAI
from typing import Tuple, List
from Grid import Grid
from sys import maxsize as MAX_INT
import math
import time


class PlayerAI(BaseAI):

    global MIN_INT
    MIN_INT = -MAX_INT - 1
       
    def getChildren(self, grid, minmax: str) -> Tuple[int, Grid, int]:
        """gets all children and the moving directions for max player
           gets all empty cells and attempts new tiles configurations for "2" and "4" for min player
        """
        children = []
        moving = []
        scores = []

        if minmax == "max":
            for direction in grid.getAvailableMoves():
                #print(grid.getAvailableMoves())
                #clone the current grid here to avoid loosing it after .move()
                gridcopy = grid.clone()
                #move method returns True if moved and makes the change to gridcopy itself
                moved = gridcopy.move(direction)
                if moved == True:
                    children.append(gridcopy)
                    moving.append(direction)
                    scores.append(self.utility(gridcopy))
            evaluated = list(zip(scores, children, moving))
            sorted(evaluated, key=lambda x: x[0], reverse=False)
            return evaluated
        if minmax == "min":
            for cell in grid.getAvailableCells():
                #insert a new tile "2" and "4" in empty cell to cover this posibility
                for tile in (2,4):
                    #clone the grid object first 
                    gridcopy = grid.clone()
                    gridcopy.insertTile(cell, tile)
                    children.append(gridcopy)
                    scores.append(self.utility(gridcopy))
            evaluated = list(zip(scores, children))
            sorted(evaluated, key=lambda x: x[0], reverse=True)
            return evaluated


    def middle(self, L) -> int:
        L = sorted(L)
        n = int(len(L)/2)
        m = int((n - 1) / 2)
        return int((L[n] + L[m]) / 2)

    
    def utility(self, grid: Grid) -> int:
        """
        This method evaluates “how good” our game grid is by calculating:
        how many tiles of same value,
        how close to each other,
        highest tile,
        number of non-zero elements.
        """
        #how many tiles are non-zero
        count = 0
        #how many tiles are zero
        count_0 = 0
        #sum all the tiles which are non-zero
        sum = 0
        #sum all tiles per column
        sum_col = 0
        sum_cols = []
        #list of all tile values
        tileval = []
        #count number of cells with adjacent values being same
        adjCellCount = 0
        adjCellValues = [1]
        #clone the current grid to avoid modifying after using .move() on it
        gridCopy = grid.clone()
        #establish weights for each heuristics
        w1 = 10
        w2 = 0
        w3 = 2000 #weight for tile of max value
        w4 = 0
        w5 = 10000 #weight for number of zeros

        for i in range(grid.size):
            for j in range(grid.size):
                sum += grid.map[i][j]
                tileval.append(grid.map[i][j])
                if grid.map[i][j] != 0:
                    count += 1
                if grid.map[i][j] == 0:
                    count_0 += 1
                sum_col += sum
                sum_cols.append(sum_col)
        max_tile = max(tileval)
        upleft_corner = grid.map[0][0]
        sum_corners = grid.map[0][0]+(grid.map[0][1]+grid.map[1][0])
        max_sum_cols = 0 #max(sum(grid.map[0]),sum(grid.map[1]),sum(grid.map[2]),sum(grid.map[3]))

        return int(w1 * (sum) + w2* sum_corners + w3 * (max_tile) + w4 * upleft_corner + w5 * count_0) #+ w4 * (adjCellCount + max_adjCellCount)

    
    def maximise(self, grid: Grid, a: int, b: int, d: int)-> Tuple[Grid, int, int]:

        """
        This is the max method representing PlayerAI from the minimax algorithm takes the following parameters:
        grid: is an object of the Grid class
        a: alpha from α-β pruning
        b: beta from α-β pruning
        d: maximum allowed depth
        returns: a tuple of the form (maxChild, maxUtility, move), where:
                    maxChild is the children of the current grid object (in the minimax algorithm tree) 
                    that maximizes the utility, and 
                    maxUtility is the utility value of maxChild game grid.
                    move is the move of the child object
        """
        # at the beginning we set maxUtility to (-sys.maxint - 1) and maxChild to None
        (maxChild, maxUtility, move) = (None, MIN_INT, -1)

        if not grid.canMove():
            return (None, self.utility(grid), -1)
        if d == 0:
            return (None, self.utility(grid), -1)
        d -= 1

        #if no children are generated, stop here
        if not self.getChildren(grid, "max"):
            return (maxChild, maxUtility, -1)

        # iterate on children to find child with minimum  utility value
        for _, child, dir in self.getChildren(grid, "max"):
            move = dir
            #get the utility of the minimise method on the child grid
            (_, utility) = self.minimise(child, a, b, d)
            if utility > maxUtility:
                (maxChild, maxUtility, move) = (child, utility, dir)
                return (maxChild, maxUtility, move)
            if maxUtility >= b:
                break
                return (maxChild, maxUtility, move)
            if maxUtility > a:
                a = maxUtility
                return (maxChild, maxUtility, move)

    def minimise(self, grid: Grid, a: int, b: int, d: int)-> Tuple[Grid, int]:

        """
        This is the min method from the minimax algorithm representing the ComputerAI player
        and takes the following parameters:
        grid: is an object of the Grid class
        a: alpha from α-β pruning
        b: beta from α-β pruning
        d: maximum allowed depth

        returns: a tuple of the form (minChild, minUtility), where:
                    minChild is the children of the current grid object (in the minimax algorithm tree) 
                    that minimises the utility, and 
                    minUtility is the utility value of minChild game grid.
        """

        # at the begining we set minUtility to the max it can be ('MAX_INT') and minChild to None
        (minChild, minUtility) = (None, MAX_INT)
        
        if not grid.canMove():
            return (None, self.utility(grid))
        if d == 0:
            return (None, self.utility(grid))
        d -= 1
        
        # no children are obtained, stop here
        if not self.getChildren(grid, "min"):
            return (minChild, minUtility)
        
        # iterate on children to find child with minimum utility value
        for _, child in self.getChildren(grid, "min"):
            (_, utility, _) = self.maximise(child, a, b, d)
            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
                return (minChild, minUtility)
            if minUtility <= a:
                return (minChild, minUtility)
                break
            if minUtility < b:
                b = minUtility
                return (minChild, minUtility)


    def getMove(self, grid: Grid, depth: int = 10) -> int:
         timeLimit = 0.2
         prevTime = time.process_time()
         while time.process_time() - prevTime < timeLimit:
            (child, utility, bestmove) = self.maximise(grid, MIN_INT, MAX_INT, depth)
            print("utility: ", utility, sep=' ')
            print("bestmove: ", bestmove, sep=' ')
            return bestmove

