BOARD_WIDHT = 9
BOARD_HEIGHT = 9
MAX_CHAIN_LENGHT = 3
COLORS = ['B', 'W']

directions = {
	'NE': (-1, 0),
	'SW': (1, 0),
	'NW': (-1, -1),
	'SE': (1, 1),
	'E': (0, 1),
	'W': (0, -1)
}

opposite = {
	'NE': 'SW',
	'SW': 'NE',
	'NW': 'SE',
	'SE': 'NW',
	'E': 'W',
	'W': 'E'
}
