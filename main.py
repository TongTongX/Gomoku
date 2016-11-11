#!/usr/bin/env python
#-*- coding: utf-8 -*-

import Tkinter
import boardGUI
import gobang


if __name__ == "__main__":
	window = Tkinter.Tk()
	window.wm_title("GOMOKU GAME")
	gui_board = boardGUI.Board_Frame(window)
	gui_board.pack()
	window.mainloop()
