class GameBoard(object):
    """Game board."""

    def __init__(self):
        # board is a 15*15 array: each posision is initially set to be 0
        self.__board = [[0 for _ in range(15)] for _ in range(15)]

        # store positions of 5 stones in a line
        self.won = {}


    def reset(self):
        """Clear the board (set all position to 0)."""
        self.__board = [[0 for _ in range(15)] for _ in range(15)]


    def get(self, row, col):
        """Get the value at a coord."""
        
        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return 0
        return self.__board[row][col]


    def check(self):
        """Check if there is a winner.

        Returns:
            0-no winner, 1-black wins, 2-white wins
        """
        board = self.__board
        # check in 4 directions
        # a coordinate stands for a specific direction, imagine the direction of a coordinate
        # relative to the origin on xy-axis
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(15):
            for j in range(15):
                # if no stone is on the position, don't need to consider this position
                if board[i][j] == 0:
                    continue
                # value-value at a coord, i-row, j-col
                value = board[i][j]
                # check if there exist 5 in a line
                for d in dirs:
                    x, y = i, j
                    count = 0
                    for _ in range(5):
                        if self.get(x, y) != value:
                            break
                        x += d[0]
                        y += d[1]
                        count += 1
                    # if 5 in a line, store positions of all stones, return value
                    if count == 5:
                        self.won = {}
                        r, c = i, j
                        for _ in range(5):
                            self.won[(r, c)] = 1
                            r += d[0]
                            c += d[1]
                        return value
        return 0


    def board(self):
        """Return the board array."""
        return self.__board


    def show(self):
        """Output current board on terminal."""
        print('  A B C D E F G H I J K L M N O')
        self.check()
        for col in range(15):
            print(chr(ord('A') + col), end=" ")
            for row in range(15):
                ch = self.__board[row][col]
                if ch == 0:
                    print('.', end=" ")
                elif ch == 1:
                    print('X', end=" ")
                elif ch == 2:
                    print('O', end=" ")
            print()
