import json


SUBSCRIBE_REQUEST = 'subscribe'


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
