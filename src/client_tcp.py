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
		self.__port = port if port is not None else DEFAULT_PORT
		self.__s_ping = socket.socket()

	def connect_server_ping(self):
		"""
			Configure a socket to listen the server requests
		"""
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
		"""
			Answer a message to the client
			Parameters:
				client (TCP client): The client to answer the message
				msg_receive (string): The message to send to the client
		"""
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
		"""
			Extract the message received by the client
			Parameters:
				client (TCP client): The client to repond
			Returns:
				string: Message received
		"""
		is_received = False
		result = b''

		while is_received == False:
			data = client.recv(1024)
			result += data
			is_received = data == b''

		return result.decode('utf8')

	def send_to_server(self, msg):
		"""
			Send message to the server
			Parameters:
				msg (string): Message to send
		"""
		s_send = socket.socket()
		s_send.connect(SERVER_ADDRESS)
		self.__send(s_send, msg)
		response = self.__receive(s_send)
		s_send.close()

		return response

	def send_answer(self, client, msg):
		"""
			Answer to the server request
			Parameters:
				client (TCP client): The client to repond
				msg_receive (string): The message received by the client
		"""
		self.__send(client, msg)

	def get_request(self):
		"""
			Get the request received by the server
			Returns:
				TCP client, tuple, string: The client who sent the message, the address of the client, the message
		"""
		client, addr = self.__s_ping.accept()
		msg = client.recv(1024).decode('utf8')

		return client, addr, msg

	@property
	def port(self):
		"""
			Accessor to get the TCP port used
			Returns:
				int: The port used
		"""
		return self.__port


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)

	client = ClientTCP()
	client.connect_server()