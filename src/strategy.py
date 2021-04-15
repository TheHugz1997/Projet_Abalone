import logging

NO_PRIORITY = None
BOARD_PRIORITY_1 = 5
BOARD_PRIORITY_2 = 20
BOARD_PRIORITY_3 = 30
BOARD_PRIORITY_4 = 40
BOARD_PRIORITY_5 = 50
PUSH_PRIORITY = 70

BOARD_WIDHT = 9
BOARD_HEIGHT = 9
MAX_CHAIN_LENGHT = 3
COLORS = ['B', 'W']
PREVIOUS = {}

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
	def __init__(self):
		self.__marbles = []
		self.__direction = None
		self.__priority = 0

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
		self._current = color
		self._color = COLORS[color]
		self._board = board
		self.__best_choice = None
		self.__strategy_cfg = StrategyConfiguration()
		global PREVIOUS

	def is_free(self, l, c):
		try:
			return self._board[l][c] == 'E'
		except IndexError:
			return False

	def is_my_marble(self, l, c):
		try:
			return self._board[l][c] == self._color
		except IndexError:
			return False

	def is_opposite_marble(self, l, c):
		try:
			return self._board[l][c] == COLORS[self._current - 1]
		except IndexError:
			return False

	def is_on_board(self, l, c):
		try:
			if not -1 < l < BOARD_WIDHT:
				return False
			if not -1 < c < BOARD_HEIGHT:
				return False
			return not self._board[l][c] == 'X'
		except IndexError:
			return False
	
	def future_marble_out(self, direction, l, c):
		marbel_future_pos = self._board[l][c]
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
		for direction, coordinates in directions.items():
			dl, dc = coordinates
			dl_back, dc_back = directions[opposite[direction]]

			if self.is_on_board(l + dl_back, c + dc_back):
				continue

			len_marble, len_opposite_marble = len(self.get_marbles_chain(l, c, opposite[direction])), 0

			if len_opposite_marble < MAX_CHAIN_LENGHT:
				while self.is_opposite_marble(l + (dl * len_marble), c + (dc * len_marble)) and len_opposite_marble < MAX_CHAIN_LENGHT:
					len_opposite_marble += 1
					l += dl
					c += dc

			if len_marble < len_opposite_marble:
				return True
		
		return False

	def previous_pos(self, identification, priority, marbles, direction):
		# Called when priority is not none and check if the next move is not the same as it was two moves earlier
		if PREVIOUS == {}:
			return True
		else:
			try:
				if "penultimate" in PREVIOUS[identification].keys():
					if [priority, marbles, direction] == PREVIOUS[identification]["penultimate"]:
						print("same move")
						return False
					else:
						return True
				else:
					return True
			except KeyError:
				return True
	
	def fill_previous(self, identification, priority, marbles, direction):
		# Called when the move is accepted and not the same as earlier
		# Builds the dico previous
		if PREVIOUS == {}:
			PREVIOUS[identification] = {}
			PREVIOUS[identification]["last"] = [priority, marbles, direction]
		elif identification in PREVIOUS.keys():
			if "last" in PREVIOUS[identification].keys():
				PREVIOUS[identification]["penultimate"] = PREVIOUS[identification]["last"]
				PREVIOUS[identification]["last"] = [priority, marbles, direction]
			else:
				PREVIOUS[identification]["last"] = [priority, marbles, direction]
		else:
			PREVIOUS[identification] = {}
			PREVIOUS[identification]["last"] = [priority, marbles, direction]

	def can_push(self, direction, l, c, marble_chain):
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
				return 100
			elif self.is_free(l + dl, c + dc):
				return 100 - (self.get_board_priority(l + dl, c + dc) * 10)
			else:
				return None
		return None

	def get_marbles_chain(self, l, c, direction):
		back_direction = opposite[direction]
		dl, dc = directions[back_direction]
		marbles_chain = []

		while self.is_my_marble(l, c):
			if len(marbles_chain) < MAX_CHAIN_LENGHT:
				marbles_chain.append([l, c])
			else:
				return marbles_chain
			l += dl
			c += dc
		
		return marbles_chain

	def get_board_priority(self, l, c):
		try:
			return board_weight[l][c]
		except IndexError:
			return NO_PRIORITY


	def get_marbles(self, marble, l, c):
		for direction, coordinates in directions.items():
			dl, dc = coordinates
			priority = 0
			# Check if the next coordinate is on the board and is not one of our marble
			if self.is_on_board(l + dl, c + dc) and not self.is_my_marble(l + dl, c + dc):
				# Takes marbles as much as possible that can follow the same direction
				marble_chain = self.get_marbles_chain(l, c, direction)

				if len(marble_chain) != 0:
					# Check if we can push an opposite marble
					priority += self.get_board_priority(l + dl, c + dc) * len(marble_chain)

					for marble_to_move in marble_chain:
						if self.future_marble_out(direction, *marble_to_move):
							priority -= 100
						if self.can_be_ejected(*marble_to_move):
							priority += 300

					if self.is_opposite_marble(l + dl, c + dc):
						push_priority = self.can_push(direction, l, c, marble_chain)
						if push_priority is not None:
							priority += push_priority
						else:
							priority = None
					yield priority, marble_chain, direction
		yield None, None, None

	def get_strategy(self):
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
		return self.__strategy_cfg
