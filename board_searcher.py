from board_evaluator import BoardEvaluator


class BoardSearcher(object):
	"""Board searcher for best next move."""

	def __init__ (self):
		self.evaluator = BoardEvaluator()
		self.board = [ [ 0 for n in range(15) ] for i in range(15) ]
		self.gameover = 0
		self.overvalue = 0
		self.maxdepth = 3	# set the max depth to 3 so that the running time
							# for each move is not too long
							# depth: 1 - <1 sec, 2 - a few sec, 3 - up to 4 min


	def genMoves(self, turn):
		"""Generate all legal moves for the current board.

		store the score and position of each move in a list in format of (score, i, j)
		"""
		moves = []
		board = self.board
		POSES = self.evaluator.POS
		for i in range(15):
			for j in range(15):
				if board[i][j] == 0:
					score = POSES[i][j]
					moves.append((score, i, j))
	
		moves.sort(reverse=True)	# sort moves in reverse order, i.e., with decreasing scores
		return moves
	

	def __search(self, turn, depth, alpha = -0x7fffffff, beta = 0x7fffffff):
		"""Recursive search, return the best score.
		
		Minimax algorithm with alpha-beta pruning.
		0x7fffffff == (2^31)-1, indicating a large value
		"""

		# base case: depth is 0
		# evaluate the board and return
		if depth <= 0:
			score = self.evaluator.evaluate(self.board, turn)
			return score

		# if game over, return immediately
		score = self.evaluator.evaluate(self.board, turn)
		if abs(score) >= 9999 and depth < self.maxdepth: 
			return score

		# generate new moves
		moves = self.genMoves(turn)
		bestmove = None

		# for all current moves
		# len(moves) == num of empty intersections on current board
		# worst case O(m^n) or O( m!/(m-n)! ), m = num of empty spots, 
		# 			n = depth(num of further steps this program predicts)
		for score, row, col in moves:

			# label current move to board
			self.board[row][col] = turn
			
			# calculate next turn
			if turn == 1:
				nturn = 2
			elif turn == 2:
				nturn = 1
			
			# DFS, return score and position of move
			score = - self.__search(nturn, depth - 1, -beta, -alpha)

			# clear current move on board
			self.board[row][col] = 0

			# calculate the move with best score
			# alpha beta pruning: removes nodes that are evaluated by the minimax algorithm
			# 				in the search tree, eliminates branches that cannot posibbly
			#				influence the final decision.
			if score > alpha:
				alpha = score
				bestmove = (row, col)
				if alpha >= beta:
					break
		
		# if depth is max depth, record the best move
		if depth == self.maxdepth and bestmove:
			self.bestmove = bestmove

		# return current best score and its correponding move
		return alpha

	# specific search
	# args: turn: 1(black)/2(white), depth
	def search(self, turn, depth=3):
		self.maxdepth = depth
		self.bestmove = None
		score = self.__search(turn, depth)
		if abs(score) > 8000:
			self.maxdepth = depth
			score = self.__search(turn, 1)
		row, col = self.bestmove
		return score, row, col