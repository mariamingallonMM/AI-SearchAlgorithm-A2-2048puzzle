from random import randint
from BaseAI import BaseAI
from typing import Tuple, List
from Grid import Grid
from sys import maxsize as MAX_INT
import math
import time
from array import *
from itertools import chain


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
            evaluated = sorted(evaluated, key=lambda x: x[0], reverse=True)
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
            evaluated = sorted(evaluated, key=lambda x: x[0], reverse=False)
            return evaluated


  
    def utility(self, grid: Grid) -> int:
        """
        This method evaluates “how good” our game grid is by calculating:
        ## how many tiles are zero
        ## 
        """
        #clone the current grid to avoid modifying after using .move() on it
        gridCopy = grid.clone()
        
        #establish weights for each heuristics
        w1 = 100000 #value of topleft corner tile
        w2 = 10 #max tile value
        w3 = 0 #sum of all tiles
        w4 = 200 #sum of first column
        w5 = 10 #how many tiles are zeros
        w6 = 100000 #max tile is at corner

        weigths = [w1, w2, w3, w4, w5, w6]

        #define heuristics used
        #value of top left corner
        topleft_corner = int(grid.map[0][0])
        #max tile value
        tileval = tuple(chain.from_iterable(grid.map))
        #sum value of all tiles which are non-zero
        sum = int(math.fsum(tileval))
        max_tile = max(list(tileval))
        #sum of tiles in first column
        max_sum_col1 = grid.map[0][0] + grid.map[1][0] + grid.map[2][0] + grid.map[3][0]
        #how many tiles are zero
        count_0 = len([x for x in list(tileval) if x == 0])
        #max tile is at corner, start with '0'
        max_tile_topleft_corner = 0
        if int(grid.map[0][0]) == int(max_tile):
            max_tile_topleft_corner = 1
        #second max tile is near the corner
        second_max_tile_topleft_corner = 0
        list(tileval).remove(int(max_tile))
        second_max_tile = max(tileval)
        if int(grid.map[1][0]) == int(max_tile):
            max_tile_topleft_corner += 1
        #second max tile is near corner (at first column, second row)
        if int(grid.map[0][1]) == int(second_max_tile):
            max_tile_topleft_corner += 1
        if int(grid.map[1][1]) == int(second_max_tile):
            max_tile_topleft_corner += 1
        #bonus if tiles near corner are exact max_tile too so they merge
        #if int(grid.map[1][0]) and int(grid.map[0][1]) and int(grid.map[1][1]) == int(max_tile):
        #    max_tile_topleft_corner += 2

        heuristics = [topleft_corner, max_tile, sum, max_sum_col1, count_0, max_tile_topleft_corner]

        return int(math.fsum([a * b for a, b in zip(weigths, heuristics)]))
        #return int(w1 * sum + w2* topleft_corner + w3 * max_tile + w4 * max_sum_col1 + w5 * count_0 + w6 * max_tile_topleft_corner)

    
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


    def getMove(self, grid: Grid, depth: int = 20) -> int:
         timeLimit = 0.2
         prevTime = time.process_time()
         while time.process_time() - prevTime < timeLimit:
            (child, utility, bestmove) = self.maximise(grid, MIN_INT, MAX_INT, depth)
            print("utility: ", utility, sep=' ')
            print("bestmove: ", bestmove, sep=' ')
            return bestmove

