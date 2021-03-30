import socket
import logging

SERVER_HOST = '127.0.0.1'
HOST_PORT = 3000
DEFAULT_PORT = 4704


class ClientTCP:
    def __init__(self, port=None):
        self.__s = socket.socket()
        self.__port = port if port is not None else DEFAULT_PORT

    def connect_server(self):
        try:
            self.__s.connect((SERVER_HOST, HOST_PORT))
        except socket.error as error:
            logging.critical(f"Socket error {error}")
            logging.critical(f"Cannot connect to the server !")
            return

        logging.info(f"Connected to the server. Host : {SERVER_HOST}, Port : {HOST_PORT}")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = ClientTCP()
    client.connect_server()
