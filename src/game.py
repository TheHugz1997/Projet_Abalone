import logging
import time
import random
from threading import Thread
from strategy import Strategy, StrategyConfiguration
from abalone_utility import *
from check_loop import CheckLoop


GAME_TIMEOUT = 2.5  # Seconds


def timeit(func):
	"""
		Decorator use to print the function time
	"""
	def wrapper(*arg, **kwargs):
		start = time.time()
		res = func(*arg)
		logging.debug(f'Time of the function : {time.time() - start}')
		return res
	return wrapper

class Game():
	"""
		Get all the move and lauch the negamax algorithm
		Parameters:
			live (int): Bad moves that we can do
			player (int): The current player (0: Black, 1: White)
			board (list): The board state
	"""

	__check_loop = CheckLoop()
	def __init__(self, lives, player, board):
		self.__lives = lives
		self.__board = board
		self.__player = player
		self.__running = False
		self.__return = [None, None, None]

	def cache_negamax(self, player, board):
		"""
			Thread function where the negamax is running
			Parameters:
				player (int): Current player
				board (list): The current board
		"""
		def depth_negamax(player, board, depth=2, priority=None, marbles=None, direction=None, alpha=float('-inf'), beta=float('inf')):
			if depth == 0:
				if priority is not None:
					return -priority, marbles, direction
				return None, None, None

			strategy = Strategy(player, board)
			best_value, best_marbles, best_direction = float("-inf"), None, None

			for index_line, line in enumerate(board):
				# Get the index of each column and the composition of each line
				for index_column, marble in enumerate(line):
					for c_direction in directions:
						if not self.__running:
							break
						# Get the current priority, marble to move and the direction to go
						marble_chain, c_priority = strategy.check_marbles_priority(index_line,
																	index_column, c_direction)
						if c_priority is None or marble_chain is None:
							continue

						# Get the board after move
						future_board = strategy.get_future_board(marble_chain, c_direction)

						value, marbles, direction = depth_negamax(0 if player else 1, future_board, depth-1, -c_priority, marble_chain, c_direction, -beta, -alpha)
						value = c_priority - value
						if Game.__check_loop.is_looping(marble_chain, board):
							value /= 10

						if value is not None:
							if value > best_value:
								best_value = value
								best_marbles = marble_chain
								best_direction = c_direction
						alpha = max(alpha, best_value)
						if alpha >= beta:
							break
			return -best_value, best_marbles, best_direction

		self.__return = depth_negamax(player, self.__board)
		Game.__check_loop.append(self.__return[1], self.__board)

	@timeit
	def get_movement(self):
		"""
			Get the current movement to do
			Returns
				marbles, direction
		"""
		self.__running = True

		# Create and start the game thread
		game_thread = Thread(target=self.cache_negamax, args=(self.__player, self.__board))
		game_thread.start()

		# Start the timer
		time_start = time.time()
		while (((time.time() - time_start) < GAME_TIMEOUT) and game_thread.is_alive()):
			True
		self.__running = False

		# Wait the thread
		game_thread.join()

		str_cfg = StrategyConfiguration(*self.__return)

		logging.info("priority : {}, marbles : {}, direction : {}".format(*self.__return))
		return str_cfg.marbles, str_cfg.direction
