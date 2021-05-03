from copy import deepcopy


MEMORY_SIZE = 10  # Change the memory size of the lists
POINTER = 0
MOVE_MEM = [None] * MEMORY_SIZE
BOARD_MEM = [None] * MEMORY_SIZE

class CheckLoop:
	def append_test(self, move, board):
		global POINTER
		global MOVE_MEM
		global BOARD_MEM
		"""
			Append a move and a board in the memory
			Parameters :
				move (StrategyConfiguration): Move to add on the memory
				board (list): Board to add on the memory
		"""
		if MEMORY_SIZE == 0:
			return

		if POINTER < MEMORY_SIZE:
			MOVE_MEM[POINTER] = move
			BOARD_MEM[POINTER] = deepcopy(board)
			POINTER += 1
		else:
			self._shift_mem()
			MOVE_MEM[MEMORY_SIZE - 1] = move
			BOARD_MEM[MEMORY_SIZE - 1] = deepcopy(board)

	def _shift_mem(self):
		global POINTER
		global MOVE_MEM
		global BOARD_MEM
		"""
			Shift the list if the memory is full
		"""
		if MEMORY_SIZE == 0:
			return

		for i in range(1, MEMORY_SIZE):
			MOVE_MEM[i - 1] = MOVE_MEM[i]
			BOARD_MEM[i - 1] = BOARD_MEM[i]
		MOVE_MEM[MEMORY_SIZE - 1] = None
		BOARD_MEM[MEMORY_SIZE - 1] = None
	
	def is_looping(self, move, board):
		global POINTER
		global MOVE_MEM
		global BOARD_MEM
		"""
			Check if the game is looping
			Parameters:
				move (StrategyConfiguration): Move to check
				board (list): Board to check
			Returns:
				Return True if it's looping, False otherwise
		"""
		if POINTER == 0:
			return False
		
		for i in range(0, POINTER):
			if (BOARD_MEM[i] == board and MOVE_MEM[i] == move):
				print("IT'S LOOPING BRU")
				return True

		return False
"""
if __name__ == '__main__':
	strategy_1 = StrategyConfiguration([1, 2], 'SW', 150)
	strategy_2 = StrategyConfiguration([2, 3], 'SE', 100)
	strategy_3 = StrategyConfiguration([3, 6], 'SE', 120)
	strategy_4 = StrategyConfiguration([3, 6], 'SE', 120)
	strategy_4_previous = StrategyConfiguration([2, 6], 'SE', 120)

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

	board4 = [
		["E", "W", "W", "W", "W", "X", "X", "X", "X"],
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

	checkloop.append_test(strategy_1, board1)
	checkloop.append_test(strategy_2, board2)
	checkloop.append_test(strategy_3, board3)
	checkloop.append_test(strategy_4, board4)

	print(checkloop.is_looping(strategy_1, board1))
	print(checkloop.is_looping(strategy_2, board2))
	print(checkloop.is_looping(strategy_3, board3))
	print(checkloop.is_looping(strategy_4_previous, board4))
"""

