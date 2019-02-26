import tkinter as tk
import math
from game_board import GameBoard
from board_searcher import BoardSearcher


class BoardCanvas(tk.Canvas):
	"""Apply the tkinter Canvas Widget to plot the game board and stones."""
	
	def __init__(self, master=None, height=0, width=0):
		
		tk.Canvas.__init__(self, master, height=height, width=width)
		self.draw_gameBoard()
		self.gameBoard = GameBoard()
		self.boardSearcher = BoardSearcher()
		self.boardSearcher.board = self.gameBoard.board()
		self.turn = 2
		self.undo = False
		self.depth = 2
		self.prev_exist = False
		self.prev_row = 0
		self.prev_col = 0


	def draw_gameBoard(self):
		"""Plot the game board."""

		# 15 horizontal lines
		for i in range(15):
			start_pixel_x = (i + 1) * 30
			start_pixel_y = (0 + 1) * 30
			end_pixel_x = (i + 1) * 30
			end_pixel_y = (14 + 1) * 30
			self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

		# 15 vertical lines
		for j in range(15):
			start_pixel_x = (0 + 1) * 30
			start_pixel_y = (j + 1) * 30
			end_pixel_x = (14 + 1) * 30
			end_pixel_y = (j + 1) * 30
			self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

		# place a "star" to particular intersections 
		self.draw_star(3,3)
		self.draw_star(11,3)
		self.draw_star(7,7)
		self.draw_star(3,11)
		self.draw_star(11,11)


	def draw_star(self, row, col):
		"""Draw a "star" on a given intersection
		
		Args:
			row, col (i.e. coord of an intersection)
		"""
		start_pixel_x = (row + 1) * 30 - 2
		start_pixel_y = (col + 1) * 30 - 2
		end_pixel_x = (row + 1) * 30 + 2
		end_pixel_y = (col + 1) * 30 + 2
		
		self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill = 'black')


	def draw_stone(self, row, col):
		"""Draw a stone (with a circle on it to denote latest move) on a given intersection.
		
		Specify the color of the stone depending on the turn.
		
		Args:
			row, col (i.e. coord of an intersection)
		"""

		inner_start_x = (row + 1) * 30 - 4
		inner_start_y = (col + 1) * 30 - 4
		inner_end_x = (row + 1) * 30 + 4
		inner_end_y = (col + 1) * 30 + 4

		outer_start_x = (row + 1) * 30 - 6
		outer_start_y = (col + 1) * 30 - 6
		outer_end_x = (row + 1) * 30 + 6
		outer_end_y = (col + 1) * 30 + 6

		start_pixel_x = (row + 1) * 30 - 10
		start_pixel_y = (col + 1) * 30 - 10
		end_pixel_x = (row + 1) * 30 + 10
		end_pixel_y = (col + 1) * 30 + 10
		
		if self.turn == 1:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
			self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='white')
			self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='black')
		elif self.turn == 2:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
			self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='black')
			self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='white')


	def draw_prev_stone(self, row, col):
		"""Draw the previous stone with single color.
		
		Specify the color of the stone depending on the turn.
		
		Args:
			row, col (i.e. coord of an intersection)
		"""
		
		start_pixel_x = (row + 1) * 30 - 10
		start_pixel_y = (col + 1) * 30 - 10
		end_pixel_x = (row + 1) * 30 + 10
		end_pixel_y = (col + 1) * 30 + 10
		
		if self.turn == 1:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
		elif self.turn == 2:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')


	def gameLoop(self, event):
		"""The main loop of the game. 
		Note: The game is played on a tkinter window. However, there is some quite useful information 
			printed onto the terminal such as the simple visualizaiton of the board after each turn,
			messages indicating which step the user reaches at, and the game over message. The user
			does not need to look at what shows up on the terminal. 
		
		self.gameBoard.board()[row][col] == 1(black stone) / 2(white stone)
		self.gameBoard.check() == 1(black wins) / 2(white wins)
		
		Args:
			event (the position the user clicks on using a mouse)
		"""

		while True:
			# User's turn. Place a black stone. 
			print('Your turn now...\n')
			self.turn = 1
			invalid_pos = True
			# since a user might not click exactly on an intersection, place the stone onto
			# the intersection closest to where the user clicks
			for i in range(15):
				for j in range(15):
					pixel_x = (i + 1) * 30
					pixel_y = (j + 1) * 30
					square_x = math.pow((event.x - pixel_x), 2)
					square_y = math.pow((event.y - pixel_y), 2)
					distance =  math.sqrt(square_x + square_y)

					# since there is noly one intersection such that the distance between it 
					# and where the user clicks is less than 15, it is not necessary to find 
					# the actual least distance
					if (distance < 15) and (self.gameBoard.board()[i][j] == 0):
						invalid_pos = False
						row, col = i, j
						self.draw_stone(i,j)
						if self.prev_exist == False:
							self.prev_exist = True
						else:
							self.draw_prev_stone(self.prev_row, self.prev_col)
						self.prev_row, self.prev_col = i, j
						# unbind to ensure the user cannot click anywhere until the program
						# has placed a white stone already
						self.unbind('<Button-1>')
						break	# break the inner for loop
				else:
					continue	# executed if the inner for loop ended normally(no break)
				break			# executed if 'continue' skipped(break)
								# break the outer for loop
			
			# break the inner while loop
			if invalid_pos:
				print('Invalid position.\n')
				break
			else:
				break

		# Place a black stone after determining the position
		self.gameBoard.board()[row][col] = 1

		# If the user wins the game, end the game and unbind.
		if self.gameBoard.check() == 1:
			print('BLACK WINS !!')
			self.create_text(240, 500, text = 'BLACK WINS !!')
			self.unbind('<Button-1>')
			return 0
		
		# Change the turn to the program now
		self.turn = 2
		print('Program is thinking now...')
		
		# Determine the position the program will place a white stone on.
		# Place a white stone after determining the position.
		score, row, col = self.boardSearcher.search(self.turn, self.depth)
		coord = '%s%s'%(chr(ord('A') + row), chr(ord('A') + col))
		print('Program has moved to {}\n'.format(coord))
		self.gameBoard.board()[row][col] = 2
		self.draw_stone(row,col)
		if self.prev_exist == False:
			self.prev_exist = True
		else:
			self.draw_prev_stone(self.prev_row, self.prev_col)
		self.prev_row, self.prev_col = row, col
		self.gameBoard.show()
		print('\n')

		# bind after the program makes its move so that the user can continue to play
		self.bind('<Button-1>', self.gameLoop)

		# If the program wins the game, end the game and unbind.
		if self.gameBoard.check() == 2:
			print('WHITE WINS.')
			self.create_text(240, 500, text = 'WHITE WINS')
			self.unbind('<Button-1>')
			return 0
			

class BoardFrame(tk.Frame):
	"""The Frame Widget is mainly used as a geometry master for other widgets, or to
	provide padding between other widgets.
	"""
	
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.create_widgets()


	def create_widgets(self):
		self.boardCanvas = BoardCanvas(height = 550, width = 480)
		self.boardCanvas.bind('<Button-1>', self.boardCanvas.gameLoop)
		self.boardCanvas.pack()
