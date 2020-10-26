from random import randint
from BaseAI import BaseAI
from typing import Tuple, List
from Grid import Grid
from sys import maxsize as MAX_INT

class PlayerAI(BaseAI):
    
    #def __init__(self, map):
    #    self.clone(map)

    #def __eq__(self, other) -> bool:
    #    for i in range(4):
    #        for j in range(4):
    #            if self.map[i][j] != other.map[i][j]:
    #                return False
    #    return True


    def getChildren(self, grid, who: str) -> List:
        if who == "max":
            return grid.getAvailableMoves()
        elif who == "min":
            return grid.getAvailableCells()


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

    #define Max player to be PlayerAI

    def maximise(self, state: Grid(), a: int, b: int, d: int):  #-> Tuple[grid, int]:

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

        # at the begining we set maxUtility to the min it can be, ie. < 0
        # and maxChild to None
        (maxChild, maxUtility) = (None, -1)

        ## check if the current state is a terminal node or the max depth allowed has been reached
        #if state.isGameOver() or d == 0:
        #    maxChild = None
        #    maxUtility = state.utility()
        #    return (maxChild, maxUtility)

        #d -= 1

        # get children of current state
        children = self.getChildren(state,"max")
        # iterate on children to find child with minimum  utility value
        for child in children:
            grid = state
            grid.move(child)
            child.utility()      
            (_, utility) = self.minimise(grid, a, b, d)
            if utility > maxUtility:
                (maxChild, maxUtility) = (grid, utility)
            if maxUtility >= b:
                break
            if maxUtility > a:
                a = maxUtility

        return (maxChild, maxUtility)

    def minimise(self, state: Grid(), a: int, b: int, d: int):  #-> Tuple[grid, int]:

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
        # we set it up to 'MAX_INT' from getBestMove() function
        # and minChild to None
        (minChild, minUtility) = (None, MAX_INT)

        # check if the current state is a terminal node or the max depth allowed has been reached
        #if self.isGameOver() or d == 0:
        #    minChild = None
        #    minUtility = state.utility()
        #    return (minChild, minUtility)

        #d -= 1

        # get children of current state
        children = self.getChildren(state, "min")
        # iterate on children to find child with minimum utility value
        for child in children:
            grid = state
            grid.move(child)
            child.utility()      
            (_, utility) = self.maximise(grid, a, b, d)
            if utility > minUtility:
                (minChild, minUtility) = (grid, utility)
            if minUtility <= a:
                break
            if minUtility < b:
                b = minUtility

        return (minChild, minUtility)

    def pepa(self):
        return True

    def getMove(self, grid: Grid(), depth: int = 5):
        grid = Grid()
        (child, _) = self.maximise(grid, -1, MAX_INT, depth)
        moves = range(0,4)
        return moves[randint(0, len(moves) - 1)] if moves else None
#        return self.pepa()


    #def getMove(self, grid):
    #    #cells = grid.getAvailableCells() #for MIN
    #    #moves = grid.getAvailableMoves() #for MAX

    #    #moves = grid.getChildren("max") #for MAX

    #    return moves[randint(0, len(moves) - 1)] if moves else None

