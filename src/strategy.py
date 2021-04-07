import logging

NO_PRIORITY = None
BOARD_PRIORITY_1 = 5
BOARD_PRIORITY_2 = 20
BOARD_PRIORITY_3 = 30
BOARD_PRIORITY_4 = 40
BOARD_PRIORITY_5 = 50

BOARD_WIDHT = 9
BOARD_HEIGHT = 9
MAX_CHAIN_LENGHT = 3
COLORS = ['B', 'W']

directions = {
	'NE': (-1,  0),
	'SW': ( 1,  0),
	'NW': (-1, -1),
	'SE': ( 1,  1),
	 'E': ( 0,  1),
	 'W': ( 0, -1)
}

opposite = {
	'NE': 'SW',
	'SW': 'NE',
	'NW': 'SE',
	'SE': 'NW',
	'E': 'W',
	'W': 'E'
}

board_weight = [
	[5, 5, 5, 5, 5, None, None, None, None],
	[5, 20, 20, 20, 20, 5, None, None, None],
	[5, 20, 30, 30, 30, 20, 5, None, None],
	[5, 20, 30, 40, 40, 30, 20, 5, None],
	[5, 20, 30, 40, 50, 40, 30, 20, 5],
	[None, 5, 20, 30, 40, 40, 30, 20, 5],
	[None, None, 5, 20, 30, 30, 30, 20, 5],
	[None, None, None, 5, 20, 20, 20, 20, 5],
	[None, None, None, None, 5, 5, 5, 5, 5]
]


class StrategyConfiguration:
	def __init__(self):
		self.__marbles = []
		self.__direction = None
		self.__priority = -1000

	@property
	def marbles(self):
		return self.__marbles

	@marbles.setter
	def marbles(self, marbles):
		self.__marbles = marbles

	@property
	def direction(self):
		return self.__direction

	@direction.setter
	def direction(self, direction):
		self.__direction = direction

	@property
	def priority(self):
		return self.__priority

	@priority.setter
	def priority(self, priority):
		self.__priority = priority


class Strategy:
	def __init__(self, lives, color, board):
		self._lives = lives
		self._color = COLORS[color]
		self._board = board
		self.__best_choice = None
		self.__strategy_cfg = StrategyConfiguration()

	def is_free(self, l, c):
		try:
			return self._board[l][c] == 'E'
		except IndexError:
			return False

	def is_on_board(self, l, c):
		try:
			if not 0 <= l < BOARD_WIDHT:
				return False
			if not 0 <= l < BOARD_HEIGHT:
				return False
			return not self._board[l][c] == 'X'
		except IndexError:
			return False

	def get_marbles_chain(self, color, l, c, direction):
		back_direction = opposite[direction]
		dl, dc = directions[back_direction]
		marbles_chain = []

		if not self.is_on_board(l, c):
			return marbles_chain
		while len(marbles_chain) < MAX_CHAIN_LENGHT:
			if color == self._color and self.is_on_board(l + dl, c + dc):
				marbles_chain.append([l, c])
				l += dl
				c += dc
			else:
				return marbles_chain
		
		return marbles_chain

	def get_board_priority(self, l, c):
		try:
			return board_weight[l][c]
		except IndexError:
			return NO_PRIORITY

	def get_marbles(self, direction, l, c):
		priority = self.get_board_priority(l, c)
		dl, dc = directions[direction]

		try:
			if self._board[l + dl][ c + dc] == 'E':
				marble_chain = self.get_marbles_chain(self._color, l, c, direction)
				for marble in marble_chain:
					priority += self.get_board_priority(marble[0], marble[1])
				return priority, marble_chain
			else:
				return None, None
		except IndexError:
			return None, None

	def get_strategy(self):
		for index_line, line in enumerate(self._board):
			for index_column, marble in enumerate(line):
				if marble == self._color:
					for direction in directions.keys():
						priority, marbles = self.get_marbles(direction, index_line, index_column)
						if priority is not None:
							if priority > self.__strategy_cfg.priority:
								self.__strategy_cfg.priority = priority
								self.__strategy_cfg.marble = marbles
								self.__strategy_cfg.direction = direction
		return self.__strategy_cfg
