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


class  StrategyConfiguration:
    def __init__(self):
        self.__marbles = []
        self.__direction = None

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
    def direction(self, coordinates):
        for key, value in directions:
            if value == coordinates:
                return key
        return None


class Strategy:
    def __init__(self):
        self.__best_choice = None
