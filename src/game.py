from strategy import Strategy, StrategyConfiguration


COLORS = ['B', 'W']


class Game(Strategy):
    def __init__(self, lives, color, board):
        self.__lives = lives
        self.__color = COLORS[color]
        self.__board = board

    def get_movement(self):
        strategy_cfg = StrategyConfiguration()
        return strategy_cfg.marbles, strategy_cfg.direction
