import socket
import logging

SERVER_HOST = '127.0.0.1'  # Server IP address
HOST_PORT = 3000  # Port listened by the server
DEFAULT_PORT = 4704  # Default port to use


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

    def send_data_server(self, data):
        packet_sent = 0

        data = data.encode('utf8')
        logging.debug(f"Sending packets...\nPackets : {data}")

        while packet_sent < len(data):
            packet_sent += self.__s.send(data[packet_sent:])

        logging.debug(f"Send completed !")

    @property
    def port(self):
        return self.__port


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    client = ClientTCP()
    client.connect_server()
    client.send_data_server("Hello world")
