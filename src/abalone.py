import sys
import logging
from threading import Thread
from json_formater import json_decode, json_subscribe, json_ping_answer
from client_tcp import ClientTCP


ABALONE_NAME = "Hugo&Alex"
MATRICULES = ["195347", "195004"]


class Abalone:
    def __init__(self):
        self.__name = ABALONE_NAME
        self.__client = ClientTCP()

        # self.__client.connect_server()
        self.__client.connect_server_ping()

        self.__request_handler = \
        {
            'ping': self.__confirm,
        }

    def run(self):
        while True:
            client, addr, message_json = self.__client.get_request()

            logging.info(f"Request received : {message_json}")
            message = json_decode(message_json)

            if 'request' in message:
                self.__request_handler[message['request']](client, message)
            elif 'response' in message:
                self.__subscribe_response_extract(message)

    def subscribe_server(self):
        """
            Subscribe the server Championship
        """
        subscribe_data = json_subscribe(MATRICULES, self.__client.port, self.__name)
        response = json_decode(self.__client.send_to_server(subscribe_data))

        try:
            print()
            if response["response"].upper() == "OK":
                logging.info("Registered to th server")
            else:
                logging.critical(f"Error while subscribing : {response['error']}")
        except Exception as e:
            logging.critical(f"Error on subscribing to the server : {e}")
            exit()

    def __confirm(self, *arg, **kwarqgs):
        msg = json_ping_answer()
        self.__client.send_to_server(msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    abalone = Abalone()
    abalone.subscribe_server()

    try:
        abalone.run()
    except InterruptedError:
        exit()
