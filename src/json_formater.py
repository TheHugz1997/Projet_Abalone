import json


SUBSCRIBE_REQUEST = 'subscribe'


def json_subscribe(matricules, port, name):
    subscribe = {}

    subscribe['request'] = SUBSCRIBE_REQUEST
    subscribe['port'] = port
    subscribe['name'] = name
    subscribe['matricules'] = matricules

    return json.dumps(subscribe, indent=4, separators=(',', ':'))
