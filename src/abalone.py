import sys
import logging
from json_formater import json_subscribe
from client_tcp import ClientTCP


ABALONE_NAME = "Hugo&Alex"
MATRICULES = ["195347", "195004"]


class Abalone:
    def __init__(self):
        self.__name = ABALONE_NAME
        self.__client = ClientTCP()

        self.__client.connect_server()

    def subscribe_server(self):
        subscribe_data = json_subscribe(ABALONE_NAME, self.__client.port, self.__name)
        self.__client.send_data_server(subscribe_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    abalone = Abalone()
    abalone.subscribe_server()
