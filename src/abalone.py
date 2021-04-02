import sys
import logging
from threading import Thread
from json_formater import json_decode, json_subscribe, json_ping_answer
from client_tcp import ClientTCP


ABALONE_NAME = "Hugo&Alex"
MATRICULES = ["195347", "195004"]


class Abalone:
    def __init__(self, port=None):
        self.__name = ABALONE_NAME
        self.__client = ClientTCP(port)

        self.__client.connect_server_ping()

        self.__request_handler = \
        {
            'ping': self.__confirm,
        }

    def run(self):
        while True:
            print(self.__client.port)
            client, addr, message_json = self.__client.get_request()
            logging.info(f"Request received : {message_json}")
            message = json_decode(message_json)

            if 'request' in message:
                request = message['request']
                if request in self.__request_handler.keys():
                    self.__request_handler[request](client, message)
                else:
                    logging.critical(f"Request \"{request}\" unknown...")
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
                logging.info("Registered to the server")
            else:
                logging.critical(f"Error while subscribing : {response['error']}")
        except Exception as e:
            logging.critical(f"Error on subscribing to the server : {e}")
            exit()

    def __confirm(self, client, msg_receive):
        msg = json_ping_answer()
        self.__client.send_answer(client, msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            abalone = Abalone(int(arg))
            abalone.subscribe_server()
            Thread(target=abalone.run, daemon=True).start()
        while True:
            pass
    else:
        port = sys.argv[1] if len(sys.argv) == 2 else None
        abalone = Abalone(port)
        abalone.subscribe_server()
        while True:
            abalone.run()
