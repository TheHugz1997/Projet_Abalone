FUTURE_DEPTH = 2  # Change the memory size of the lists
BOARD_WIDHT = 9
BOARD_HEIGHT = 9
COLORS = ['B', 'W']
directions = {
	'NE': (-1,  0),
	'SW': ( 1,  0),
	'NW': (-1, -1),
	'SE': ( 1,  1),
	 'E': ( 0,  1),
	 'W': ( 0, -1)
}

class CheckFuture:
    def get_future_board(self, marbles, direction, color, board):
        """
            Return the future board state
            Parameters:
                marbles (list): All the marbles to move
                direction (string): Direction to go
            Returns:
                The future board
        """
        future_board = []
        dl, dc = directions[direction]
        future_board = board

        for marble in marbles:
            l, c = marble[0], marble[1]
            future_board[l][c] = 'E'
            future_board[l + dl][c + dc] = COLORS[color]
        for i in range(len(future_board)):
            print(future_board[i])
        return future_board

"""
if __name__ == '__main__':
    checkfuture = CheckFuture()
    board1 = [
        ["W", "W", "W", "W", "W", "X", "X", "X", "X"],
        ["W", "W", "W", "W", "W", "W", "X", "X", "X"],
        ["E", "E", "W", "W", "W", "E", "E", "X", "X"],
        ["E", "E", "E", "E", "E", "E", "E", "E", "X"],
        ["E", "E", "E", "E", "E", "E", "E", "E", "E"],
        ["X", "E", "E", "E", "E", "E", "E", "E", "E"],
        ["X", "X", "E", "E", "B", "B", "B", "E", "E"],
        ["X", "X", "X", "B", "B", "B", "B", "B", "B"],
        ["X", "X", "X", "X", "B", "B", "B", "B", "B"]
    ]
    marbles = [[2, 3], [1, 2]]
    direction = "SE"
    color = 1
    print(checkfuture.get_future_board(marbles, direction, color, board1))
    """
