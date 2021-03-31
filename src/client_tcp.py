import socket
import logging
from threading import Thread

SERVER_HOST = '127.0.0.1'  # Server IP address
HOST_PORT = 3000  # Port listened by the server
SERVER_ADDRESS = (SERVER_HOST, HOST_PORT)
DEFAULT_PORT = 4704  # Default port to use


class ClientTCP:
    def __init__(self, port=DEFAULT_PORT):
        # Create the socket instance
        self.__port = port
        self.__s_ping = socket.socket()

    def connect_server_ping(self):
        try:
            # Bind the socket to the port choosed
            self.__s_ping.bind(('0.0.0.0', self.__port))

            # Listen the data on the port
            self.__s_ping.listen()
        except socket.error as error:
            logging.critical(f"Cannot create the lister !")
            logging.critical(f"Socket error {error}")
            return

        logging.info(f"Listen on {self.__port}")
        logging.info(f"Socket port : {self.__s_ping.getsockname()}")

    def __send(self, client, msg):
        packet_sent = 0
        msg = msg.encode('utf8')
        try:
            while packet_sent < len(msg):
                packet_sent += client.send(msg[packet_sent:])

            logging.debug("Data sent !")
        except Exception as e:
            logging.warning("Error sending data !")
            print(e)


    def __receive(self, client):
        is_received = False
        result = b''

        while is_received == False:
            data = client.recv(1024)
            result += data
            is_received = data == b''

        return result.decode('utf8')

    def send_to_server(self, msg):
        s_send = socket.socket()
        s_send.connect(SERVER_ADDRESS)
        self.__send(s_send, msg)
        response = self.__receive(s_send)
        s_send.close()

        return response

    def get_subsciption_answer(self):
        msg = ''
        while msg == '':
            msg = self.__receive(self.__s)

        return msg

    def get_request(self):
        client, addr = self.__s_ping.accept()
        msg = client.recv(1024).decode('utf8')
        # client.close()
        return client, addr, msg

    @property
    def port(self):
        return self.__port


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    client = ClientTCP()
    client.connect_server()
