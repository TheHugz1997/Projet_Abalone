import logging
from copy import deepcopy
from abalone_utility import *


board_weight = [
	[1, 1, 1, 1, 1, None, None, None, None],
	[1, 2, 2, 2, 2, 1, None, None, None],
	[1, 2, 3, 3, 3, 2, 1, None, None],
	[1, 2, 3, 4, 4, 3, 2, 1, None],
	[1, 2, 3, 4, 5, 4, 3, 2, 1],
	[None, 1, 2, 3, 4, 4, 3, 2, 1],
	[None, None, 1, 2, 3, 3, 3, 2, 1],
	[None, None, None, 1, 2, 2, 2, 2, 1],
	[None, None, None, None, 1, 1, 1, 1, 1]
]


class StrategyConfiguration:
	def __init__(self, priority=0, marbles=[], direction=None):
		self.__priority = priority
		self.__marbles = marbles
		self.__direction = direction

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

	def __eq__(self, other):
		return (self.__marbles == other.marbles) and (self.__direction == other.direction)

class Strategy:
	def __init__(self, color, board):
		# self._lives = lives
		self._current = color
		self._color = COLORS[color]
		self._board = board
		self.__best_choice = None
		self.__ennemy_marble = self.marble_counter()
		self.__strategy_cfg = StrategyConfiguration()

	def is_free(self, l, c):
		"""
			Check if the place choose is empyt
			Parameters:
				l (int): The current board line
				c (int): The current board column
			Returns:
				bool: True if the place is empty, False otherwise
		"""
		try:
			return self._board[l][c] == 'E'
		except IndexError:
			return False

	def is_my_marble(self, l, c):
		"""
			Check if it's one of our marble
			Parameters:
				l (int): The current board line
				c (int): The current board column
			Returns:
				bool: True if it's one of my marble, False otherwise
		"""
		try:
			return self._board[l][c] == self._color
		except IndexError:
			return False

	def is_opposite_marble(self, l, c):
		"""
			Check if it's an opposite marble board
			Parameters:
				l (int): The current board line
				c (int): The current board column
			Returns:
				bool: True if the marble is one of the opposite, False otherwise
		"""
		try:
			return self._board[l][c] == COLORS[self._current - 1]
		except IndexError:
			return False

	def is_on_board(self, l, c):
		"""
			Check if we are on the board
			Parameters:
				l (int): The current board line
				c (int): The current board column
			Returns:
				bool: True if the marble is on the board, False otherwise
		"""
		try:
			if not -1 < l < BOARD_WIDHT:
				return False
			if not -1 < c < BOARD_HEIGHT:
				return False
			return not self._board[l][c] == 'X'
		except IndexError:
			return False

	def is_move_away_edge(self, l, c, direction):
		"""
			Check if the marble is going away from the edge of the board
			Parameters:
				l (int): The current board line
				c (int): The current board column
				direction (string): Direction key to go
			Returns:
				bool: True if it's going away, False otherwise
		"""
		dl_back, dc_back = directions[opposite[direction]]
		
		return not self.is_on_board(l + dl_back, c + dc_back)

	def marble_counter(self):
		number_enemy_marbles = 0
		# Get the index of each line and the lines of the board
		for index_line, line in enumerate(self._board):
				# Get the index of each column and the composition of each line
				for index_column, marble in enumerate(line):
					if marble == COLORS[self._current - 1]:
						number_enemy_marbles += 1
		return number_enemy_marbles

	def future_marble_out(self, l, c):
		"""
			Check if one of our marble can be ejected in the future move
			Parameters:
				l (int): The current board line
				c (int): The current board column
			Returns:
				bool: True if it can be ejected, False otherwise
		"""
		len_opposite_marble = 0

		for ennemy_directions in directions:
			dl, dc = directions[ennemy_directions]
			dl_opp, dc_opp = directions[opposite[ennemy_directions]]
			# Check if there is an ennemy marble near our future marble's position and if our future marble's position is near the edge
			if self.is_opposite_marble(l + dl, c + dc) and not self.is_on_board(l + dl_opp, c + dc_opp):
				while self.is_opposite_marble(l + dl, c + dc):
					l += dl
					c += dc
					len_opposite_marble +=1
					if len_opposite_marble > 1:
						return True
		return False

	def can_be_ejected(self, l, c):
		"""
			Check if one of our marble can be ejected
			Parameters:
				l (int): The current board line
				c (int): The current board column
			Returns:
				bool: True if it can be ejected, False otherwise
		"""
		for direction, coordinates in directions.items():
			dl, dc = coordinates
			dl_back, dc_back = directions[opposite[direction]]

			if self.is_on_board(l + dl_back, c + dc_back) or self.is_my_marble(l + dl_back, c + dc_back):
				continue

			len_marble, len_opposite_marble = len(self.get_marbles_chain(l, c, opposite[direction])), 0

			while self.is_opposite_marble(l + (dl * len_marble), c + (dc * len_marble)) and len_opposite_marble < MAX_CHAIN_LENGHT:
				len_opposite_marble += 1
				l += dl
				c += dc

			if len_marble < len_opposite_marble:
				return True
		
		return False

	def can_push(self, direction, l, c, marble_chain):
		"""
			Check if we can push opposite marbles
			Parameters:
				direction (string): The direction key where we want to push
				l (int): The current board line
				c (int): The current board column
				marble_chain (list): List with our marble chain
			Returns:
				int: The priority when we can push. None when we can't push
		"""
		dl, dc = directions[direction]

		len_marble = len(marble_chain)
		len_opposite_marble = 0

		# Get the marble opposite chain
		while self.is_opposite_marble(l + dl, c + dc):
			l += dl
			c += dc
			len_opposite_marble += 1
			if len_opposite_marble >= MAX_CHAIN_LENGHT:
				return None

		# Check if there's no marble of mine behind of the opposite chain
		if len_marble > len_opposite_marble and len_opposite_marble > 0:
			if not self.is_on_board(l + dl, c + dc):
				if self.__ennemy_marble == 9:
					return 1000
				return 100
			elif self.is_free(l + dl, c + dc):
				return 100 - (self.get_board_priority(l + dl, c + dc) * 10)

		return None

	def get_marbles_chain(self, l, c, direction):
		"""
			Return the marble chain that can form the marble choosed
			Parameters:
				l (int): The current board line
				c (int): The current board column
				direction (string): The direction key where we want to push
			Returns:
				list: Return a list with all the marbles. The higher len of the list is 3 marble
		"""
		back_direction = opposite[direction]
		dl, dc = directions[back_direction]
		marbles_chain = []

		while self.is_my_marble(l, c) and self.is_on_board(l, c):
			if len(marbles_chain) < MAX_CHAIN_LENGHT:
				marbles_chain.append([l, c])
			else:
				return marbles_chain
			l += dl
			c += dc
		
		return marbles_chain

	def get_board_priority(self, l, c):
		"""
			Get the board place priority
			Parameters:
				l (int): The current board line
				c (int): The current board column
			Returns:
				int: The priority of the current place on the board
		"""
		try:
			return board_weight[l][c]
		except IndexError:
			return NO_PRIORITY

	def get_future_board(self, marbles, direction):
		"""
			Return the future board state
			Parameters:
				marbles (list): All the marbles to move
				direction (string): Direction to go
			Returns:
				The future board
		"""
		dl, dc = directions[direction]
		board = deepcopy(self._board)

		if marbles is not None:
			for marble in marbles:
				l, c = marble[0], marble[1]
				if not self.is_on_board(l + dl, c + dc):
					break
				board[l][c] = 'E'
				board[l + dl][c + dc] = self._color
		
		return board

	def check_marbles_priority(self, l, c, direction):
		"""
			Get the best marbles with priority
			Parameters:
				l (int): Line index
				c (int): Column index
				direction (string): The direction where the marbles go
			Returns:
				marbles, prioroty
		"""
		dl, dc = directions[direction]
		priority = 0

		if not self.is_my_marble(l, c):
			return [], None

		if self.is_on_board(l + dl, c + dc) and not self.is_my_marble(l + dl, c + dc):
			# Check if we can push an opposite marble
			marbles = self.get_marbles_chain(l, c, direction)
			if len(marbles) > 0:
				priority += self.get_board_priority(l + dl, c + dc) * len(marbles)

				for marble in marbles:
					if self.future_marble_out(marble[0] + dl, marble[1] + dc):
						priority -= 150
					if self.can_be_ejected(*marble):
						priority += 150
					if self.is_move_away_edge(*marble, direction):
						priority += 20

				if self.is_opposite_marble(l + dl, c + dc):
					push_priority = self.can_push(direction, l, c, marbles)
					if push_priority is not None:
						priority += push_priority
					else:
						priority = None
			return list(marbles), priority
		return [], None

	def get_strategy(self):
		"""
			Get the current marbles to move
			Returns:
				StrategyConfiguration: The current move to do
		"""
		# Get the index of each line and the lines of the board
		for index_line, line in enumerate(self._board):
			# Get the index of each column and the composition of each line
			for index_column, marble in enumerate(line):
				# Get the AI's first marble depend of the color
				if marble == self._color:
					# Get the current priority, marble to move and the direction to go
					for priority, marbles, direction in self.get_marbles(marble, index_line, index_column):
						if priority is not None:
							if priority > self.__strategy_cfg.priority:
								if self.previous_pos(marble, priority, marbles, direction):
									self.__strategy_cfg.priority = priority
									self.__strategy_cfg.marbles = marbles
									self.__strategy_cfg.direction = direction
		self.fill_previous(self._color, self.__strategy_cfg.priority, self.__strategy_cfg.marbles, self.__strategy_cfg.direction)
		print("here's previous : {}".format(PREVIOUS))
		print(self.get_future_board(self.__strategy_cfg.marbles, self.__strategy_cfg.direction))
		return self.__strategy_cfg
