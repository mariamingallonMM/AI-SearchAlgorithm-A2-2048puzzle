from random import randint
from BaseAI import BaseAI
from typing import Tuple, List
from Grid import Grid
from sys import maxsize as MAX_INT

class PlayerAI(BaseAI):
    
    def utility(self) -> int:
            """
            Next, we create a utility method. This method evaluates “how good” our game grid is. There could be many possible choices for this, but here we use the following metric: 
              sum all the elements of the matrix and divide by the number of non-zero elements.

            """

            count = 0
            sum = 0
            for i in range(4):
                for j in range(4):
                    sum += self.map[i][j]
                    if self.map[i][j] != 0:
                        count += 1
            return int(sum/count)

    
    def getChildren(self, grid):
        #gets all children and the moving directions
        allmoves = [0,1,2,3]
        children = []
        moving = []
        for m in allmoves:
            gridcopy = grid
            moved = gridcopy.move(m)
            #move method returns True if moved and makes the change to gridcopy itself
            if moved == True:
                children.append(gridcopy)
                moving.append(m)
            return children
        
    #define Max player to be PlayerAI
    def maximise(self, state: Grid, a: int, b: int, d: int):  #-> Tuple[grid, int]:

        """
        The function maximise from the minimax algorithm takes the following parameters:
        state: is an object of the Grid class
        a: alpha from α-β pruning
        b: beta from α-β pruning
        d: maximum allowed depth
        returns: a tuple of the form (maxChild, maxUtility), where:
                    maxChild is the children of the current state object (in the minimax algorithm tree) 
                    that maximizes the utility, and 
                    maxUtility is the utility value of maxChild game state.
        """
        if d == 0:
            return heuristic(state)
        if not state.canMove():
            return heuristic(state)
        
        # at the beginning we set maxUtility to the min it can be, ie. < 0
        # and maxChild to None
        (maxChild, maxUtility) = (None, -1)


        # get children of current state
        children = self.getChildren(state)

        # iterate on children to find child with minimum  utility value
        for child in children:
            grid = state
            #state.move()
            #child.utility()      
            (_, utility) = self.minimise(grid, a, b, d)
            if utility > maxUtility:
                (maxChild, maxUtility) = (grid, utility)
            if maxUtility >= b:
                break
            if maxUtility > a:
                a = maxUtility
        return (maxChild, maxUtility)

    def minimise(self, state: Grid, a: int, b: int, d: int):  #-> Tuple[grid, int]:

        """
        The function minimise from the minimax algorithm takes the following parameters:

        state: is an object of the Grid class
        a: alpha from α-β pruning
        b: beta from α-β pruning
        d: maximum allowed depth

        returns: a tuple of the form (minChild, minUtility), where:
                    minChild is the children of the current state object (in the minimax algorithm tree) 
                    that minimises the utility, and 
                    minUtility is the utility value of minChild game state.
        """

        # at the begining we set minUtility to the max it can be considering the result of the maximise function
        # we set it up to 'MAX_INT'
        # and minChild to None
        (minChild, minUtility) = (None, MAX_INT)

        # get children of current state
        children = state.getAvailableCells()
        # iterate on children to find child with minimum utility value
        for child in children:
            grid = state
            #state.move()
            #child.utility()      
            (_, utility) = self.maximise(grid, a, b, d)
            if utility > minUtility:
                (minChild, minUtility) = (grid, utility)
            if minUtility <= a:
                break
            if minUtility < b:
                b = minUtility

        return (minChild, minUtility)



    #TODO: check heuristic function
    def heuristic(grid):
        #Try to keep largest tile in top left and others in decreasing order from left to right
        emptyTiles = len([i for i, x in enumerate(grid) if x == 0])
        maxTile = max(grid)
        MergeBonus = 0
        OrderBonus = 0
        Ord = 0
        penalty = 0
        ##weights = [10,8,7,6.5,.5,.7,1,3,-.5,-1.5,-1.8,-2,-3.8,-3.7,-3.5,-3]
        weights = [65536,32768,16384,8192,512,1024,2048,4096,256,128,64,32,2,4,8,16]
        if maxTile == grid[0]:
            Ord += (math.log(grid[0])/math.log(2))*weights[0]
        for i in xrange(16):
            if grid[i] >= 8:
                Ord += weights[i]*(math.log(grid[i])/math.log(2))
            ##if i < 4 and grid[i] == 0 :
                ###Ord -=weights[i]*(math.log(maxTile)/math.log(2))
        return Ord/(16-emptyTiles)

        orig_grid = [[0] * 4 for i in xrange(4)]
        k = 0
        for i in range(4):
            for j in range(4):
                orig_grid[i][j] = grid[k]
                k += 1
        sm = 0
        for i in range(4):
            for j in range(4):
                if orig_grid[i][j] != 0:
                    val = math.log(orig_grid[i][j])/math.log(2)
                    for k in range(3-j):
                        nextright = orig_grid[i][j+k+1]
                        if nextright != 0:
                            rightval = math.log(nextright)/math.log(2)
                            if rightval != val:
                                sm -= math.fabs(rightval - val)
                                break
                    for k in range(3-i):
                        nextdown = orig_grid[i+k+1][j]
                        if nextdown != 0:
                            downval = math.log(nextdown)/math.log(2)
                            if downval != val:
                                sm -= math.fabs(downval - val)
                                break
        mn = 0
        up = 0
        down = 0
        left = 0
        right = 0
        
        for i in range(4):
            j = 0
            k = j+1
            while k < 4:
                if orig_grid[i][k] == 0:
                    k += 1
                else:
                    if orig_grid[i][j] == 0:
                        curr = 0
                    else:
                        curr = math.log(orig_grid[i][j])/math.log(2)
                    nextval = math.log(orig_grid[i][k])/math.log(2)
                    if curr > nextval:
                        up += nextval - curr
                    elif nextval > curr:
                        down += curr - nextval
                j = k
                k += 1
        for j in range(4):
            i = 0
            k = i+1
            while k < 4:
                if orig_grid[j][k] == 0:
                    k += 1
                else:
                    if orig_grid[j][i] == 0:
                        curr = 0
                    else:
                        curr = math.log(orig_grid[j][i])/math.log(2)
                    nextval = math.log(orig_grid[j][k])/math.log(2)
                    if curr > nextval:
                        left += nextval - curr
                    elif nextval > curr:
                        right += curr - nextval
                i = k
                k += 1
        nm = max(up,down) + max(left,right)
        return 0.1*sm+mn+math.log(maxTile)/math.log(2)+ emptyTiles

    def getMoveTo(self, grid) -> int:
        if grid.canMove([0]):
            g = Grid()
            g.move(0)
            if g == grid:
                return 0
        if grid.canMove([1]):
            g = Grid()
            g.move(1)
            if g == grid:
                return 1
        if grid.canMove([2]):
            g = Grid()
            g.move(2)
            if g == grid:
                return 2
        return 3

    def getMove(self, grid: Grid, depth: int = 1):
        (child, _) = self.maximise(grid, -1, MAX_INT, depth)
        return self.getMoveTo(child)
        #return moves[randint(0, len(moves) - 1)] if moves else None
