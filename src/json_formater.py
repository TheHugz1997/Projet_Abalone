import json
from random import shuffle


SUBSCRIBE_REQUEST = 'subscribe'
MOVE_REQUEST = 'move'
MOVE_MESSAGES = [
	'I will beat you',
	'You will never beat me',
	'Behind you',
	'MANC-RMA finale champions gros',
	'A 10 is sufficient',
	'Don\'t look the code'
	]


def json_decode(string):
	return json.loads(string)

def json_subscribe(matricules, port, name):
	subscribe = {}

	subscribe['request'] = SUBSCRIBE_REQUEST
	subscribe['port'] = port
	subscribe['name'] = name
	subscribe['matricules'] = matricules

	return json.dumps(subscribe, indent=4, separators=(',', ':'))

def json_ping_answer():
	ping_ans = {"response": "pong"}

	return json.dumps(ping_ans, indent=4, separators=(',', ':'))

def json_play_response(marbles, direction):
	shuffle(MOVE_MESSAGES)
	response, move_played = dict(), dict()

	move_played['marbles'] = marbles
	move_played['direction'] = direction

	response['response'] = MOVE_REQUEST
	response['move'] = move_played
	response['message'] = MOVE_MESSAGES[0]

	return json.dumps(response, indent=4, separators=(',', ':'))

def json_give_up():
	response = {'response': 'giveup'}

	return json.dumps(response, indent=4, separators=(',', ':'))


