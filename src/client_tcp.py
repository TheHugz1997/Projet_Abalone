import socket
import logging

SERVER_HOST = '127.0.0.1'
HOST_PORT = 3000
DEFAULT_PORT = 4704


class ClientTCP:
    def __init__(self, port=DEFAULT_PORT):
        self.__s = socket.socket()
        self.__port = port

    def connect_server(self):
        try:
            # Bind the socket to the port choosed
            self.__s.bind(('0.0.0.0', self.__port))

            # Connection to the server
            self.__s.connect((SERVER_HOST, HOST_PORT))
        except socket.error as error:
            logging.critical(f"Socket error {error}")
            logging.critical(f"Cannot connect to the server !")
            return

        logging.info(f"Connected to the server. Host : {SERVER_HOST}, Port : {HOST_PORT}")
        logging.info(f"Socket port : {self.__s.getsockname()}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = ClientTCP()
    client.connect_server()
