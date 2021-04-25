from copy import deepcopy
from strategy import StrategyConfiguration

MEMORY_SIZE = 10  # Change the memory size of the lists


class CheckLoop:
	def __init__(self):
		self.__pointer = 0
		self.__move_mem = [None] * MEMORY_SIZE
		self.__board_mem = [None] * MEMORY_SIZE	

	def append(self, move, board):
		"""
			Append a move and a board in the memory
			Parameters :
				move (StrategyConfiguration): Move to add on the memory
				board (list): Board to add on the memory
		"""
		if MEMORY_SIZE == 0:
			return

		if self.__pointer < MEMORY_SIZE:
			self.__move_mem[self.__pointer] = move
			self.__board_mem[self.__pointer] = deepcopy(board)
			self.__pointer += 1
		else:
			self._shift_mem()
			self.__move_mem[MEMORY_SIZE - 1] = move
			self.__board_mem[MEMORY_SIZE - 1] = deepcopy(board)

	def _shift_mem(self):
		"""
			Shift the list if the memory is full
		"""
		if MEMORY_SIZE == 0:
			return

		for i in range(1, MEMORY_SIZE):
			self.__move_mem[i - 1] = self.__move_mem[i]
			self.__board_mem[i - 1] = self.__board_mem[i]
		self.__move_mem[MEMORY_SIZE - 1] = None
		self.__board_mem[MEMORY_SIZE - 1] = None
	
	def is_looping(self, move, board):
		"""
			Check if the game is looking
			Parameters:
				move (StrategyConfiguration): Move to check
				board (list): Board to check
			Returns:
				Return True if it's looping, False otherwise
		"""
		if self.__pointer == 0:
			return False
		
		for i in range(0, self.__pointer):
			if (self.__board_mem[i] == board and self.__move_mem[i] == move):
				return True

		return False

if __name__ == '__main__':
	strategy_1 = StrategyConfiguration([1, 2], 'SW', 150)
	strategy_2 = StrategyConfiguration([2, 3], 'SE', 100)
	strategy_3 = StrategyConfiguration([3, 6], 'SE', 120)

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

	board2 = [
		["W", "W", "W", "W", "W", "X", "X", "X", "X"],
		["W", "W", "W", "W", "W", "W", "X", "X", "X"],
		["E", "E", "W", "W", "W", "E", "E", "X", "X"],
		["E", "E", "E", "E", "E", "E", "E", "E", "X"],
		["E", "E", "E", "E", "E", "E", "E", "E", "E"],
		["X", "E", "E", "E", "E", "E", "E", "E", "E"],
		["X", "X", "E", "E", "B", "B", "B", "E", "E"],
		["X", "X", "X", "B", "E", "B", "B", "B", "B"],
		["X", "X", "X", "X", "E", "B", "B", "B", "B"]
	]

	board3 = [
		["W", "W", "W", "W", "W", "X", "X", "X", "X"],
		["W", "W", "W", "W", "W", "W", "X", "X", "X"],
		["E", "E", "W", "W", "W", "E", "E", "X", "X"],
		["E", "E", "E", "E", "E", "E", "E", "E", "X"],
		["E", "E", "E", "E", "E", "E", "E", "E", "E"],
		["X", "E", "E", "W", "E", "E", "E", "E", "E"],
		["X", "X", "E", "W", "B", "B", "B", "E", "E"],
		["X", "X", "X", "B", "E", "B", "B", "B", "B"],
		["X", "X", "X", "X", "E", "B", "B", "B", "B"]
	]

	checkloop = CheckLoop()

	checkloop.append(strategy_1, board1)
	checkloop.append(strategy_2, board2)
	checkloop.append(strategy_3, board3)

	print(checkloop.is_looping(strategy_1, board1))
	print(checkloop.is_looping(strategy_2, board2))
	print(checkloop.is_looping(strategy_3, board3))

