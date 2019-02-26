'''
	Define an BoardEvaluator class.
	Note: I wrote more than 100 lines if-elif-else statements to discuss every single
		possible scenarios that could occur. This portion of code looks ugly but it is
		quite necessary for the evaluation process.
'''
class BoardEvaluator(object):

	def __init__ (self):
		# self.POS is for adding weight to each intersetion
		# add weight of 7 to the center, 6 to the outer square, then
		# 5, 4, 3, 2, 1, at last 0 to the outermost square.
		self.POS = []
		for i in range(15):
			row = []
			for j in range(15):
				row.append( 7 - max(abs(i - 7), abs(j - 7)) )
			# row = [ (7 - max(abs(i - 7), abs(j - 7))) for j in range(15) ]
			self.POS.append(tuple(row))
		
		

		# different types of situations below
		self.cTwo = 1		# chong'er	2 stones in a row, 1 move to make a chongsan
		self.cThree = 2		# chongsan	3 stones in a row, 1 move to make a chongsi
		self.cFour = 3		# chongsi	4 stones in a row, 1 move(1 possible position) to make a 5
		self.two = 4		# huo'er	2 stones in a row, 1 move to make a huosan
		self.three = 5		# huosan	3 stones in a row, 1 move to make a huosi
		self.four = 6		# huosi		4 stones in a row, 1 move(2 possible positions) to make a 5
		self.five = 7		# huowu		5 stones in a row
		self.analyzed = 8		# has benn analyzed
		self.unanalyzed = 0			# has not been analyzed
		self.result = [ 0 for i in range(30) ]		# save current reslut of analyzation in a line
		self.line = [ 0 for i in range(30) ]		# current data in a line
		self.record = []			# result of analysis of whole board 
									# format of each item in list is record[row][col][dir]
		for i in range(15):
			self.record.append([])
			self.record[i] = []
			for j in range(15):
				self.record[i].append([ 0, 0, 0, 0])
		self.count = []				# count of each situation: count[black/white][situation]
		for i in range(3):
			data = [ 0 for i in range(10) ]
			self.count.append(data)
		self.reset()

	
	# reset data
	def reset(self):
		unanalyzed = self.unanalyzed
		count = self.count
		for i in range(15):
			line = self.record[i]
			for j in range(15):
				line[j][0] = unanalyzed
				line[j][1] = unanalyzed
				line[j][2] = unanalyzed
				line[j][3] = unanalyzed
		for i in range(10):
			count[0][i] = 0
			count[1][i] = 0
			count[2][i] = 0
		return 0

	
	# analyze & evaluate board 
	# return score based on analysis result
	def evaluate (self, board, turn):
		score = self.__evaluate(board, turn)
		count = self.count
		if score < -9000:
			if turn == 1:
				stone = 2
			elif turn == 2:
				stone = 1
			# print('evaluate: stone = ', stone)
			for i in range(10):
				if count[stone][i] > 0:
					score -= i
		elif score > 9000:
			if turn == 1:
				stone = 2
			elif turn == 2:
				stone = 1
			# print('evaluate: stone = ', stone)
			for i in range(10):
				if count[turn][i] > 0:
					score += i
		return score
	
	
	# analyze & evaluate board 
	# in 4 directinos: horizontal, vertical, diagonal(left-hand or right-hand)
	# return score difference between players based on analysis result
	def __evaluate (self, board, turn):
		record = self.record
		count = self.count
		unanalyzed = self.unanalyzed
		analyzed = self.analyzed
		self.reset()
		# analysis in 4 directions
		for i in range(15):
			boardrow = board[i]
			recordrow = record[i]
			for j in range(15):
				if boardrow[j] != 0:
					# has not analyzed horizontally
					if recordrow[j][0] == unanalyzed:
						self.__analysis_horizon(board, i, j)
					# has not analyzed vertically
					if recordrow[j][1] == unanalyzed:
						self.__analysis_vertical(board, i, j)
					# has not analyzed left-hand diagonally 
					if recordrow[j][2] == unanalyzed:
						self.__analysis_left(board, i, j)
					# has not analyzed right-hand diagonally
					if recordrow[j][3] == unanalyzed:
						self.__analysis_right(board, i, j)

		five = self.five
		four = self.four
		three =  self.three
		two = self.two
		cFour = self.cFour
		cThree = self.cThree
		cTwo = self.cTwo
		
		check = {}

		# for either white or black, calculated the number of occurences of different
		# situations (i.e., five, four, cFour, three, cThree, two, cTwo)
		for c in (five, four, cFour, three, cThree, two, cTwo):
			check[c] = 1
		# for each stone on the board
		for i in range(15):
			for j in range(15):
				stone = board[i][j]
				if stone != 0:
					# for 4 directions
					for k in range(4):
						ch = record[i][j][k]
						if ch in check:
							count[stone][ch] += 1
		
		# return score if there is a five
		black = 1
		white = 2
		# current turn is white
		if turn == white:
			if count[black][five]:
				return -9999
			elif count[white][five]:
				return 9999
		# current turn is black
		else:
			if count[white][five]:
				return -9999
			elif count[black][five]:
				return 9999
		
		# if there exist 2 chongsi, it's equivalent to 1 huosi
		if count[white][cFour] >= 2:
			count[white][four] += 1
		if count[black][cFour] >= 2:
			count[black][four] += 1

		# return score for specific situations
		wvalue = 0
		bvalue = 0
		win = 0
		# current turn is white
		if turn == white:
			if count[white][four] > 0:			# white huosi
				return 9990
			if count[white][cFour] > 0:			# white chongsi
				return 9980
			if count[black][four] > 0:			# black huosi
				return -9970
			if count[black][cFour] and count[black][three]:			# black chongsi & huosan
				return -9960
			if count[white][three] and count[black][cFour] == 0:	# white huosan & no black chongsi
				return 9950
			if	(count[black][three] > 1 and	# black >1 huosan &
				count[white][cFour] == 0 and	# no white chongsi &
				count[white][three] == 0 and	# no white huosan &
				count[white][cThree] == 0):		# no white chongsan
					return -9940
			
			if count[white][three] > 1:			# white >1 huosan
				wvalue += 2000
			elif count[white][three]:			# white 1 huosan
				wvalue += 200
			if count[black][three] > 1:			# black >1 huosan
				bvalue += 500
			elif count[black][three]:			# black 1 huosan
				bvalue += 100
			
			if count[white][cThree]:					# white chongsan
				wvalue += count[white][cThree] * 10
			if count[black][cThree]:					# black chongsan
				bvalue += count[black][cThree] * 10
			if count[white][two]:						# white huo'er
				wvalue += count[white][two] * 4
			if count[black][two]:						# black huo'er
				bvalue += count[black][two] * 4
			if count[white][cTwo]:						# white chong'er
				wvalue += count[white][cTwo]
			if count[black][cTwo]:						# black chong'er
				bvalue += count[black][cTwo]
		
		# current turn is black
		else:
			if count[black][four] > 0:			# black huosi
				return 9990
			if count[black][cFour] > 0:			# black chongsi
				return 9980
			if count[white][four] > 0:			# white huosi
				return -9970
			if count[white][cFour] and count[white][three]:			# white chongsi & huosan
				return -9960
			if count[black][three] and count[white][cFour] == 0:	# black huosan & no white chongsi
				return 9950
			if	(count[white][three] > 1 and	# white >1 huosan &
				count[black][cFour] == 0 and	# no black chongsi &
				count[black][three] == 0 and	# no black huosan &
				count[black][cThree] == 0):		# no black chongsan
					return -9940
			
			if count[black][three] > 1:			# black >1 huosan
				bvalue += 2000
			elif count[black][three]:			# black 1 huosan
				bvalue += 200
			if count[white][three] > 1:			# white >1 huosan
				wvalue += 500
			elif count[white][three]:			# white 1 huosan
				wvalue += 100
			
			if count[black][cThree]:					# black chongsan
				bvalue += count[black][cThree] * 10
			if count[white][cThree]:					# white chongsan
				wvalue += count[white][cThree] * 10
			if count[black][two]:						# black huo'er
				bvalue += count[black][two] * 4
			if count[white][two]:						# white huo'er
				wvalue += count[white][two] * 4
			if count[black][cTwo]:						# black chong'er
				bvalue += count[black][cTwo]
			if count[white][cTwo]:						# white chong'er
				wvalue += count[white][cTwo]
		
		
		# include weight for each intersection
		# add weight of 7 to the center, 6 to the outer square, then
		# 5, 4, 3, 2, 1, at last 0 to the outermost square.
		wc = 0
		bc = 0
		# for each intersection with a stone, add weight
		for i in range(15):
			for j in range(15):
				stone = board[i][j]
				if stone != 0:
					if stone == white:
						wc += self.POS[i][j]
					else:
						bc += self.POS[i][j]
		# add total weight to total score
		wvalue += wc
		bvalue += bc
		
		# return score differnece between players
		if turn == white:
			return wvalue - bvalue

		return bvalue - wvalue
	
	
	# anaylze horizontally
	def __analysis_horizon (self, board, i, j):
		line = self.line
		result = self.result
		record = self.record
		unanalyzed = self.unanalyzed
		# add each intersection in a row to line
		for x in range(15):
			line[x] = board[i][x]
		self.analysis_line(line, result, 15, j)
		for x in range(15):
			if result[x] != unanalyzed:
				record[i][x][0] = result[x]
		return record[i][j][0]
	
	
	# analyze vertically
	def __analysis_vertical (self, board, i, j):
		line = self.line
		result = self.result
		record = self.record
		unanalyzed = self.unanalyzed
		for x in range(15):
			line[x] = board[x][j]
		self.analysis_line(line, result, 15, i)
		for x in range(15):
			if result[x] != unanalyzed:
				record[x][j][1] = result[x]
		return record[i][j][1]
	
	
	# analyze left-hand diagonally
	def __analysis_left (self, board, i, j):
		line = self.line
		result = self.result
		record = self.record
		unanalyzed = self.unanalyzed
		if i < j:
			x, y = j - i, 0
		else:
			x, y = 0, i - j
		k = 0
		while k < 15:
			if x + k > 14 or y + k > 14:
				break
			line[k] = board[y + k][x + k]
			k += 1
		self.analysis_line(line, result, k, j - x)
		for s in range(k):
			if result[s] != unanalyzed:
				record[y + s][x + s][2] = result[s]
		return record[i][j][2]

	
	# analyzed right-hand diagonally
	def __analysis_right (self, board, i, j):
		line = self.line
		result = self.result
		record = self.record
		unanalyzed = self.unanalyzed
		if 14 - i < j:
			x, y, realnum = j - 14 + i, 14, 14 - i
		else:
			x, y, realnum = 0, i + j, j
		k = 0
		while k < 15:
			if x + k > 14 or y - k < 0:
				break
			line[k] = board[y - k][x + k]
			k += 1
		self.analysis_line(line, result, k, j - x)
		for s in range(k):
			if result[s] != unanalyzed:
				record[y - s][x + s][3] = result[s]
		return record[i][j][3]
	
	
	# analyze a line, find out different situations (i.e., five, four, three, etc)
	def analysis_line (self, line, record, num, pos):
		unanalyzed = self.unanalyzed
		analyzed = self.analyzed
		three = self.three
		cThree = self.cThree
		four = self.four
		cFour = self.cFour
		
		while len(line) < 30:
			line.append(15)
		while len(record) < 30:
			record.append(unanalyzed)
		
		for i in range(num, 30):
			line[i] = 15
		for i in range(num):
			record[i] = unanalyzed
		
		if num < 5:
			for i in range(num): 
				record[i] = analyzed
			return 0
		stone = line[pos]
		inverse = (0, 2, 1)[stone]
		num -= 1
		xl = pos
		xr = pos
		# left border
		while xl > 0:
			if line[xl - 1] != stone:
				break
			xl -= 1
		# right border
		while xr < num:
			if line[xr + 1] != stone:
				break
			xr += 1
		left_range = xl
		right_range = xr
		# left border (not opponent's stone intersection)
		while left_range > 0:
			if line[left_range - 1] == inverse:
				break
			left_range -= 1
		# right border (not opponent's stone intersection)
		while right_range < num:
			if line[right_range + 1] == inverse:
				break
			right_range += 1
		
		# if the linear range is less than 5, return directly
		if right_range - left_range < 4:
			for k in range(left_range, right_range + 1):
				record[k] = analyzed
			return 0
		
		# set analyzed
		for k in range(xl, xr + 1):
			record[k] = analyzed
		
		srange = xr - xl

		# if 5 in a row
		if srange >= 4:	
			record[pos] = self.five
			return self.five
		
		# if 4 in a row
		if srange == 3:	
			leftfour = False
			# if space on the left
			if xl > 0:
				if line[xl - 1] == 0:
					# huo'si
					leftfour = True
			if xr < num:
				if line[xr + 1] == 0:
					if leftfour:
						# huo'si
						record[pos] = self.four
					else:
						# chognsi
						record[pos] = self.cFour
				else:
					if leftfour:
						# chongsi
						record[pos] = self.cFour
			else:
				if leftfour:
					# chongsi
					record[pos] = self.cFour
			return record[pos]
		
		# if 3 in a row
		if srange == 2:
			left3 = False
			# if space on the left
			if xl > 0:
				# if space on the left
				if line[xl - 1] == 0:
					if xl > 1 and line[xl - 2] == stone:
						record[xl] = cFour
						record[xl - 2] = analyzed
					else:
						left3 = True
				elif xr == num or line[xr + 1] != 0:
					return 0
			if xr < num:
				# if space on the right
				if line[xr + 1] == 0:
					if xr < num - 1 and line[xr + 2] == stone:
						# 11101 or 22202 is equivalent to chongsi
						record[xr] = cFour
						record[xr + 2] = analyzed
					elif left3:
						record[xr] = three
					else:
						record[xr] = cThree
				elif record[xl] == cFour:
					return record[xl]
				elif left3:
					record[pos] = cThree
			else:
				if record[xl] == cFour:
					return record[xl]
				if left3:
					record[pos] = cThree
			return record[pos]
		
		# if 2 in a row
		if srange == 1:
			left2 = False
			if xl > 2:
				# if space on the left
				if line[xl - 1] == 0:
					if line[xl - 2] == stone:
						if line[xl - 3] == stone:
							record[xl - 3] = analyzed
							record[xl - 2] = analyzed
							record[xl] = cFour
						elif line[xl - 3] == 0:
							record[xl - 2] = analyzed
							record[xl] = cThree
					else:
						left2 = True
			if xr < num:
				# if space on the right
				if line[xr + 1] == 0:
					if xr < num - 2 and line[xr + 2] == stone:
						if line[xr + 3] == stone:
							record[xr + 3] = analyzed
							record[xr + 2] = analyzed
							record[xr] = cFour
						elif line[xr + 3] == 0:
							record[xr + 2] = analyzed
							record[xr] = left2 and three or cThree
					else:
						if record[xl] == cFour:
							return record[xl]
						if record[xl] == cThree:
							record[xl] = three
							return record[xl]
						if left2:
							record[pos] = self.two
						else:
							record[pos] = self.cTwo
				else:
					if record[xl] == cFour:
						return record[xl]
					if left2:
						record[pos] = self.cTwo
			return record[pos]
		return 0