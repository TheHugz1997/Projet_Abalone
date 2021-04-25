import logging
from strategy import Strategy, StrategyConfiguration
from abalone_utility import *
import time
import random

def timeit(func):
	def wrapper(*arg, **kwargs):
		start = time.time()
		res = func(*arg)
		print(f'Time of the function : {time.time() - start}')
		return res
	return wrapper

from collections import defaultdict
class Game():#Strategy):
	def __init__(self, lives, player, board):
		self.__board = board
		self.__player = player
		pass

	def negamax_depth(self, player, board):
		cache = defaultdict(lambda : 0)
		def cache_negamax(player, board, depth=2, priority=None, marbles=None, direction=None, alpha=float('-inf'), beta=float('inf')):
			if depth == 0:
				if priority is not None:
					return -priority, marbles, direction
				return None, None, None

			strategy = Strategy(player, board)
			best_value, best_marbles, best_direction = float('-inf'), None, None
			for index_line, line in enumerate(board):
				# Get the index of each column and the composition of each line
				for index_column, marble in enumerate(line):
					for c_direction in directions:
						# Get the current priority, marble to move and the direction to go
						marble_chain, c_priority = strategy.check_marbles_priority(index_line,
																	index_column, c_direction)

						if c_priority is None or marble_chain is None:
							continue
						future_board = strategy.get_future_board(marble_chain, c_direction)
						value, marbles, direction = cache_negamax(
							0 if player else 1, future_board, depth-1, -c_priority, marble_chain, c_direction, -beta, -alpha)
						value = c_priority - value

						if value is not None:
							if value > best_value:
								best_value = value
								best_marbles = marble_chain
								best_direction = c_direction
						alpha = max(alpha, best_value)
						if alpha >= beta:
							continue
			return -best_value, best_marbles, best_direction
		return cache_negamax(player, board)


	@timeit
	def get_movement(self):
		# strategy = self.get_strategy()
		#return strategy.marbles, strategy.direction
		priority, marbles, direction = self.negamax_depth(self.__player, self.__board)
		print("{}.{}.{}".format(priority, marbles, direction))
		return priority, marbles, direction
