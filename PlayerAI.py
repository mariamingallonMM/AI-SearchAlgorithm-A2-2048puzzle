from random import randint
from BaseAI import BaseAI
from typing import Tuple, List
from Grid import Grid
from sys import maxsize as MAX_INT
import math
import time


class PlayerAI(BaseAI):

    global MIN_INT, timeLimit
    MIN_INT = -MAX_INT - 1
    timeLimit = 0.2

    def getChildren(self, grid, minmax: str) -> Tuple[Grid, int]:
        """gets all children and the moving directions for max player
           gets all empty cells and attempts new tiles configurations for "2" and "4" for min player
           TODO: Why does getChildren produce the same childs? dir appears to be working correctly, check when gridcopy is assigned
        """
        children = []
        moving = []

        if minmax == "max":
            for direction in grid.getAvailableMoves():
                #clone the current grid here to avoid loosing it after .move()
                gridcopy = grid.clone()
                #move method returns True if moved and makes the change to gridcopy itself
                moved = gridcopy.move(direction)
                if moved == True:
                    children.append(gridcopy)
                    moving.append(direction)
                    print("this is a max child", gridcopy.map)
            return list(zip(children, moving))
        if minmax == "min":
            for cell in grid.getAvailableCells():
                #clone the current grid here to avoid loosing it after .move()
                gridcopy = grid.clone()
                #insert a new tile "2" in empty cell to cover this posibility
                gridcopy.insertTile(cell, 2)
                children.append(gridcopy)
            for cell in grid.getAvailableCells():
                #restart the grid object to get branches for new tile "4"
                gridcopy = grid.clone()
                #insert a new tile "4" in empty cell to cover this posibility
                move_4 = gridcopy.insertTile(cell, 4)
                children.append(gridcopy)
            return children


    def middle(self, L) -> int:
        L = sorted(L)
        n = int(len(L)/2)
        m = int((n - 1) / 2)
        return int((L[n] + L[m]) / 2)

    
    def utility(self, grid) -> int:
        """
        This method evaluates “how good” our game grid is by calculating:
        how many tiles of same value,
        how close to each other,
        highest tile,
        number of non-zero elements.
        """
        #how many tiles are non-zero
        count = 0
        #sum all the tiles which are non-zero
        sum = 0
        #list of all tile values
        tileval = []
        #count number of cells with adjacent values being same
        adjCellCount = 0
        #clone the current grid to avoid modifying after using .move() on it
        gridCopy = grid.clone()
        #establish weights for each heuristics
        weight_1 = 20
        weight_2 = 0
        weight_3 = 20
        weight_4 = 10000000

        for i in range(grid.size):
            for j in range(grid.size):
                sum += grid.map[i][j]
                tileval.append(grid.map[i][j])
                if grid.map[i][j] != 0:
                    count += 1
                    adjCellValue = gridCopy.getCellValue((i + gridCopy.move(0), j + gridCopy.move(1)))
                    #compare gridCopy after move to the previous grid
                    if adjCellValue == grid.map[i][j]:
                        adjCellCount += 1
                    
        max_tile = max(tileval)
        tilemedian = self.middle(tileval)
        print("adjacent cells count", adjCellCount)
        return int(weight_1 * (sum/count) + weight_2 * tilemedian + weight_3 * max_tile + weight_4 * adjCellCount)

    
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
            return (None, self.utility(grid), 0)
        d -= 1

        time_start = time.process_time()

        #if no children are generated, stop here
        if not self.getChildren(grid, "max"):
            return (maxChild, maxUtility, -1)

        # iterate on children to find child with minimum  utility value
        for child, dir in self.getChildren(grid, "max"):
            move = dir
            print("for each", dir)
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

    def minimise(self, grid: Grid, a: int, b: int, d: int)-> Tuple[Grid, int, int]:

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
        for child in self.getChildren(grid, "min"):
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

    
    def getMove(self, grid: Grid, depth: int = 5) -> int:
        (child, utility, bestmove) = self.maximise(grid, MIN_INT, MAX_INT, depth)
        print("utility: ", utility, sep=' ')
        print("bestmove: ", bestmove, sep=' ')
        return bestmove

### REMOVE IF NOT USED

        #def utility(self, grid) -> int:
    #    """
    #    This method evaluates “how good” our game grid is by calculating the averageTileNumber as 
    #    the sum all the elements of the matrix and divide by the number of non-zero elements.
    #    """
    #    count = 0
    #    sum = 0
    #    weight_1 = 60
    #    weight_2 = 20
    #    tilenum = []
    #    for i in range(grid.size):
    #        for j in range(grid.size):
    #            sum += grid.map[i][j]
    #            tilenum.append(grid.map[i][j])
    #            if grid.map[i][j] != 0:
    #                count += 1
    #    tilemedian = self.middle(tilenum)    
    #    return int(weight_1 * (sum/count) + weight_2 * tilemedian)

     #TODO: try to improve utility function heuristics
    # add limit for time and maybe try different d values
    #def utility(self, grid) -> int:
    #    #Try to keep largest tile on top left and others in decreasing order from left to right
    #    emptyTiles = 0
    #    list_tiles = []

    #    for i in range(grid.size):
    #        for j in range(grid.size):
    #            if grid.map[i][j] == 0:
    #                emptyTiles += 1
    #                list_tiles.append(grid.map[i][j])
      
    #    if list_tiles:
    #        maxTile = max(list_tiles)
    #    else:
    #        maxTile = 0

    #    MergeBonus = 0
    #    OrderBonus = 0
    #    Ord = 0
    #    penalty = 0
    #    #weights = [[10,8,7,6.5],
    #    #           [.5,.7,1,3],
    #    #           [-.5,-1.5,-1.8,-2],
    #    #           [-3.8,-3.7,-3.5,-3]]

    #    weights = [[65536,32768,16384,8192],
    #               [512,1024,2048,4096],
    #               [256,128,64,32],
    #               [2,4,8,16]]
    #    #corner item 
    #    #i_corner = grid.size - 1
    #    i_corner = 0

    #    if maxTile == grid.map[i_corner][i_corner] and maxTile != 0:
    #        Ord += (math.log(grid.map[i_corner][i_corner])/math.log(2))*weights[i_corner][i_corner]
    #    for i in range(grid.size):
    #        for j in range(grid.size):
    #            if grid.map[i][j] >= 8:
    #                Ord += weights[i][j]*(math.log(grid.map[i][j])/math.log(2))
    #        #if i < 4 and grid[i] == 0 :
    #            ##Ord -=weights[i]*(math.log(maxTile)/math.log(2))
    #        return int(Ord/(16-emptyTiles))

    #    orig_grid = [[0] * grid.size for i in range(grid.size)]
    #    k = 0
    #    for i in range(grid.size):
    #        for j in range(grid.size):
    #            orig_grid[i][j] = grid.map[k]
    #            k += 1
    #    sm = 0
    #    for i in range(grid.size):
    #        for j in range(grid.size):
    #            if orig_grid[i][j] != 0:
    #                val = math.log(orig_grid[i][j])/math.log(2)
    #                for k in range(grid.size -1 -j):
    #                    nextright = orig_grid[i][j+k+1]
    #                    if nextright != 0:
    #                        rightval = math.log(nextright)/math.log(2)
    #                        if rightval != val:
    #                            sm -= math.fabs(rightval - val)
    #                            break
    #                for k in range(grid.size -1 -i):
    #                    nextdown = orig_grid[i+k+1][j]
    #                    if nextdown != 0:
    #                        downval = math.log(nextdown)/math.log(2)
    #                        if downval != val:
    #                            sm -= math.fabs(downval - val)
    #                            break
    #    mn = 0
    #    up = 0
    #    down = 0
    #    left = 0
    #    right = 0
        
    #    for i in range(grid.size):
    #        j = 0
    #        k = j+1
    #        while k < grid.size:
    #            if orig_grid[i][k] == 0:
    #                k += 1
    #            else:
    #                if orig_grid[i][j] == 0:
    #                    curr = 0
    #                else:
    #                    curr = math.log(orig_grid[i][j])/math.log(2)
    #                nextval = math.log(orig_grid[i][k])/math.log(2)
    #                if curr > nextval:
    #                    up += nextval - curr
    #                elif nextval > curr:
    #                    down += curr - nextval
    #            j = k
    #            k += 1
    #    for j in range(grid.size):
    #        i = 0
    #        k = i+1
    #        while k < grid.size:
    #            if orig_grid[j][k] == 0:
    #                k += 1
    #            else:
    #                if orig_grid[j][i] == 0:
    #                    curr = 0
    #                else:
    #                    curr = math.log(orig_grid[j][i])/math.log(2)
    #                nextval = math.log(orig_grid[j][k])/math.log(2)
    #                if curr > nextval:
    #                    left += nextval - curr
    #                elif nextval > curr:
    #                    right += curr - nextval
    #            i = k
    #            k += 1
    #    nm = max(up,down) + max(left,right)
    #    return int(0.1*sm+mn+math.log(maxTile)/math.log(2)+ emptyTiles)
