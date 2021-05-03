import logging
from strategy import Strategy, StrategyConfiguration
from check_future import CheckFuture

COLORS = ['B', 'W']

class Game:
    def __init__(self, lives, color, board):
        self.__lives = lives
        self.__color = color
        self.__board = board
        self.__checkfuture = CheckFuture()
        self.__enemy_priority = 0
        self.__The_all_strategy = {}
        StrategyConfiguration.priority = 0
        StrategyConfiguration.marbles = []
        StrategyConfiguration.direction = None
        print("here's color {}".format(color))

    def get_movement(self):
        """
			Get the two best moves from get_strategy and compare each of them to the enemy's move
			Returns:
				marbles, direction
		"""
        #calling strategy first time
        strategy = Strategy(self.__lives, self.__color, self.__board)
        #calling get_strategy and get a tuple
        my_strategy1, my_strategy2 = strategy.get_strategy()
        print("HERE ARE MY_STRAT1 AND MY_STRAT2 : {} ====== {}".format(my_strategy1, my_strategy2))
        print(StrategyConfiguration.priority)
        print(StrategyConfiguration.marbles)
        print(StrategyConfiguration.direction)
        #get the future boards corresponding to the two strategies
        future_board1 = self.building_future_board(my_strategy1[1], my_strategy1[2], self.__color, self.__board)
        future_board2 = self.building_future_board(my_strategy2[1], my_strategy2[2], self.__color, self.__board)
        #get the enemy's two biggest priorities
        Enemy_strategy1 = self.getting_the_enemy_strategy(future_board1)
        print(Enemy_strategy1)
        Enemy_strategy2 = self.getting_the_enemy_strategy(future_board2)
        if self.comparison(my_strategy1[0], my_strategy2[0], Enemy_strategy1, Enemy_strategy2):
            print("hello")
            return my_strategy1[1], my_strategy1[2]
        else:
            print("hi")
            return my_strategy2[1], my_strategy2[2]

    def building_future_board(self, marbles, direction, color, board):
        """
            Calling check future to build a future board
            Parameters: 
                marbles, direction, color(int), board(actual)
            Returns:
                future board
        """
        #building the new board with one of the two best strategy
        future_board = self.__checkfuture.get_future_board(marbles, direction, self.__color,  self.__board)
        return future_board
    
    def getting_the_enemy_strategy(self, board):
        """
            Get the best enemy's strategy for one of our movement
            Parameters: 
                board(future)
            Returns:
                list: [priority, marbles, direction]
        """
        StrategyConfiguration.priority = 0
        StrategyConfiguration.marbles = []
        StrategyConfiguration.direction = None
        print("brrr")
        E_color = self.enemy_color(self.__color)
        E_strategy = Strategy(self.__lives, E_color, board)
        enemy_strategy,_ = E_strategy.get_strategy(indicator=1)
        print("enemy strat : {}".format(enemy_strategy))
        return enemy_strategy[0]


    def enemy_color(self, color):
        """
            Get the enemy's color
            Parameters: 
                color(int)
            Returns:
                enemy_color(int)
        """
        if color == 0:
            enemy_color = 1
        else:
            enemy_color = 0
        return enemy_color

    def comparison(self, stratone, strattwo, enemyone, enemytwo):
        """
            Check which strategy is the greatest
            Parameters:
                2 priority(int), 2 enemy's priority(int)
            Returns:
                Bool: True if the first priority-the enemy's corresponding priority, False otherwise
        """
        return (stratone-enemyone) >= (strattwo - enemytwo)
    
    """
        The_all_strategy[self._color] = my_strategy
        print("HERE'S YOUR DIRECTION : {}".format(The_all_strategy[self._color].direction))
        enemy_strategy = self.get_the_enemy_movement(future_board)
        my_final_strategy = self.final_strategy(self._board, enemy_strategy.priority)
        print("HERE IS THE FINAL STRATEGY BRU : {}".format((my_final_strategy.priority, my_final_strategy.marbles, my_final_strategy.direction)))
        return The_all_strategy[self.__color].marbles, The_all_strategy[self.__color].direction

    def get_the_enemy_movement(self, future_board):
        StrategyConfiguration.priority = 0
        StrategyConfiguration.marbles = []
        StrategyConfiguration.direction = None
        E_color = self.enemy_color(self._color)
        strategy2 = Strategy(self._lives, E_color, future_board)
        enemy_strategy = strategy2.get_strategy()
        print("HERE'S THE ENEMY'S DIRECTION : {}".format(enemy_strategy.direction))
        return enemy_strategy
    
    def final_strategy(self, board, new_priority):
        StrategyConfiguration.priority = 0
        StrategyConfiguration.marbles = []
        StrategyConfiguration.direction = None
        initialisation = Strategy(self._lives, self._color, self._board)
        my_final_strategy = initialisation.get_strategy(new_priority//2)
        return my_final_strategy

    def comparison(self, my_priority, the_enemy_priority):
        if my_priority =< the_enemy_priority:
            return 
    """

