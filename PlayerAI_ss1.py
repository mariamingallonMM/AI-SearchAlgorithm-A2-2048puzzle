from random import randint
from BaseAI import BaseAI
from sysconfig import sys
from Grid import Grid
from GameManager import GameManager


sys.setrecursionlimit(4000)

class PlayerAI(BaseAI):

	#variable that keeps track of the most optimal direction the PlayerAI can make
	def _init_(self):
		self.direction = -1

	#Input for heuristic: Gets the top four tiles and returns to eval function.
	def getMaxTiles(self, grid):
		maxTile = 0
		dist = 0
		maxTiles = [0, 0, 0, 0]
		for x in xrange(grid.size):
			for y in xrange(grid.size):
				dist = dist+(x-y)*grid.map[x][y]*3.0
				maxTile = grid.map[x][y]
				if maxTile > maxTiles[0]:
					maxTiles[0]=maxTile
					maxTiles.sort(cmp=None, key=None, reverse=False)
		maxTiles.append(dist)
		return maxTiles
		
	#Heuristic: Calculates the utility at leaf node based on - number of empty cells available, top 4 maxTiles values
	#and weighted distance of tiles from bottom left corner.	
	def evalfn(self,grid):
		cell = grid.getAvailableCells()
		maxTiles = self.getMaxTiles(grid)
		maxSum = sum(maxTiles)-maxTiles[4]
		
		evalScore = len(cell)*5000+maxSum*0.8+maxTiles[4]*2
		return(evalScore)
		
			
	#Allocates new tile as either number 2 (probability 0.9) or 4 (probability 0.1)
	#def getNewTileValue(self):
	#	if randint(0,99) < 100 * 0.9: 
	#		return 2 
	#	else: 
	#		return 4	

	#Minimax algorithm implementation with alpha-beta pruning
	def alphabeta(self, grid, depth, alpha, beta, maximizingPlayer):
		if depth == 0:
			e = self.evalfn(grid)
			return [e,-1]
		if maximizingPlayer:
			moves = grid.getAvailableMoves()
			if moves == []:
				return [alpha, self.direction]
			for i in moves:
				newgrid = grid.clone()
				newgrid.move(i)
				r = self.alphabeta(newgrid, depth-1, alpha, beta, False)
				if alpha < r[0]:
					self.direction = i
				if r[0] == -float('inf'):
					self.direction = i
				alpha = max(alpha, r[0])
				if beta <= alpha:
					print("I'm in break stmt")
					break
			result = [alpha, self.direction]
			return result
		else:
			cells = grid.getAvailableCells()
			if cells == []:
				return result
			i = cells[randint(0, len(cells) - 1)]
			grid.map[i[0]][i[1]] = self.getNewTileValue()
			r = self.alphabeta(grid, depth-1, alpha, beta, True)
			beta = min(beta, r[0])
			result = [beta, r[1]]
			return result
	
	
	#Returns the optimal move per the algorithm to the GameManager function.
	def getMove(self, grid: Grid):
		moves = grid.getAvailableMoves()
		print(moves)		
		result = self.alphabeta(grid, 12, -float('inf'), float('inf'), True)
		print("Expected score:",result[0])
		print("Direction",result[1])
		return result[1]				
	
