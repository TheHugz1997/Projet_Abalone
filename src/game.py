import logging
from strategy import Strategy, StrategyConfiguration


class Game(Strategy):
    def __init__(self, lives, color, board):
        Strategy.__init__(self, lives, color, board)

    def get_movement(self):
        strategy = self.get_strategy()
        print(strategy.marble)
        return strategy.marble, strategy.direction
