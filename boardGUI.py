#!/usr/bin/env python
#-*- coding: utf-8 -*-

import Tkinter
import math
import gobang

'''
	Apply the Tkinter Canvas Widget to plot the game board and stones.
'''
class Board_Canvas(Tkinter.Canvas):
	def __init__(self, master = None, height = 0, width = 0):
		Tkinter.Canvas.__init__(self, master, height = height, width = width)
		
		# initializations
		self.draw_gameBoard()
		self.b = gobang.gameBoard()
		self.s = gobang.searcher()
		self.s.board = self.b.board()
		self.turn = 2
		self.undo = False
		self.depth = 2
	

	'''
		Dlot the game board
	'''
	def draw_gameBoard(self):
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


	'''
		Draw a "star" on a given intersection
		Args: row, col (i.e.coord of an intersection)
	'''
	def draw_star(self, row, col):
		start_pixel_x = (row + 1) * 30 - 2
		start_pixel_y = (col + 1) * 30 - 2
		end_pixel_x = (row + 1) * 30 + 2
		end_pixel_y = (col + 1) * 30 + 2
		
		self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill = 'black')


	'''
		Draw a stone on a given intersection. Specify the color of the stone depending on the turn.
		Args: row, col (i.e.coord of an intersection) 
	'''
	def draw_stone(self, row, col):
		start_pixel_x = (row + 1) * 30 - 10
		start_pixel_y = (col + 1) * 30 - 10
		end_pixel_x = (row + 1) * 30 + 10
		end_pixel_y = (col + 1) * 30 + 10
		
		if self.turn == 1:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
		elif self.turn == 2:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')


	'''
		The main loop of the game. 
		Note: The game is played on a Tkinter window. However, there is some quite useful information 
			printed onto the terminal such as the simple visualizaiton of the board after each turn,
			messages indicating which step the user reaches at, and the game over message. The user
			does not need to look at what shows up on the terminal. 
		Args: event (the position the user clicks on using a mouse)
		self.b.board()[row][col] == 1(black stone) / 2(white stone)
		self.b.check() == 1(black wins) / 2(white wins)
	''' 
	def gameLoop(self, event):
		while True:
			# User's turn. Place a black stone. 
			print 'Your turn now...\n'
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
					if (distance < 15) and (self.b.board()[i][j] == 0):
						invalid_pos = False
						row, col = i, j
						self.draw_stone(i,j)
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
				print 'Invalid position.\n'
				break
			else:
				break

		# Place a black stone after determining the position
		self.b.board()[row][col] = 1

		# If the user wins the game, end the game and unbind.
		if self.b.check() == 1:
			print 'BLACK WINS !!'
			self.create_text(240, 500, text = 'BLACK WINS !!')
			self.unbind('<Button-1>')
			return 0
		
		# Change the turn to the program now
		self.turn = 2
		print 'Program is thinking now...'
		
		# Determine the position the program will place a white stone on.
		# Place a white stone after determining the position.
		score, row, col = self.s.search(self.turn, self.depth)
		coord = '%s%s'%(chr(ord('A') + row), chr(ord('A') + col))
		print 'Program has moved to %s \n' % coord
		self.b.board()[row][col] = 2
		self.draw_stone(row,col)
		self.b.show()
		print '\n'

		# bind after the program makes its move so that the user can continue to play
		self.bind('<Button-1>', self.gameLoop)

		# If the program wins the game, end the game and unbind.
		if self.b.check() == 2:
			print 'WHITE WINS.'
			self.create_text(240, 500, text = 'WHITE WINS')
			self.unbind('<Button-1>')
			return 0
			

'''
	The Frame Widget is mainly used as a geometry master for other widgets, or to provide padding
	between other widgets. 
'''	
class Board_Frame(Tkinter.Frame):
	def __init__(self, master = None):
		Tkinter.Frame.__init__(self, master)
		self.create_widgets()

	def create_widgets(self):
		self.board_canvas = Board_Canvas(height = 550, width = 480)
		self.board_canvas.bind('<Button-1>', self.board_canvas.gameLoop)
		self.board_canvas.pack()
