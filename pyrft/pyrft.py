"""
PyRFT - Python-based Reliable File Transfer
Copyright 2014 Clockwerks Software, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import socketserver
import threading


class PyRFT_TCPServer_Handler(socketserver.StreamRequestHandler):
	"""
	"""

	def handle(self):
		"""

		"""
		pass

	def write_message(self, message):
		"""
		"""
		pass

	def read_message(self):
		"""
		"""
		pass

	def client_loop(self):
		"""
		"""
		pass

class __threaded_tcp_server(socketserver.ThreadingMixIn, socketserver.TCpServer):
	pass


class PyRFT_Server_InvalidState(Exception):
	pass


class PyRFTConnection(object):
	"""
	Basic Connection Object for Client and Server

	For derived clients, this contains the server information to connect to.
	For derived servers, this contains the server information to bind to.
	"""

	def __init__(self, host, port):
		"""
		Initializer for the connection
		"""
		self.__host = host
		self.__port = port

	@property
	def host(self):
		"""
		Host Address for the connection
		"""
		return self.__host

	@host.setter
	def host(self, host_address):
		if not self.isRunning:
			self.__host = host_address
		else:
			raise PyRFT_Server_InvalidState('Server is running.')

	@property
	def port(self):
		"""
		Port for the connection
		"""
		return self.__port

	@port.setter
	def port(self, port_number):
		if not self.isRunning:
			self.__port = port_number
		else:
			raise PyRFT_Server_InvalidState('Server is running.')

class PyRFT_Server(PyRFTConnection):
	"""
	PyRFT Server Interface

	Wrapper around the server instance to enable easy management.

	Server binds to the specified host/port. Each client connection is
	handled in its own thread.
	"""

	def __init__(self, host='localhost', port='9000'):
		"""
		Initializer
		"""
		super().__init__(host, port)
		self.__is_running = False
		self.__server = {}
		self.__server['thread'] = None
		self.__server['object'] = None

	@property
	def isRunning(self):
		"""
		Determine the server status

		Returns True if the server is actively listening
		Returns False if the server is not doing anything
		"""
		return (self.__is_running is True)

	def start(self):
		"""
		Start the server actively listening on the address specified by host:port

		Throws PyRFT_Server_InvalidState if the server is already running.
		"""
		if not self.isRunning:
			self.__server['object'] = __threaded_tcp_server(host, port), PyRFT_TCPServer_Handler)
			self.__server['thread'] = threading.Thread(target=server.serve_forever)
			self.__server['thread'].daemon = True
			self.__server['thread'].start()
			self.__is_running = True
		else:
			raise PyRFT_Server_InvalidState('Server is ALREADY running.')

	def stop(self):
		"""
		Stop the server and release the resources.

		Throws PyRFT_Server_InvalidState if the server is not running.
		"""
		if self.isRunning:
			# shutdown returns when the server has fully shutdown.So it's safe to delete it.
			self.__server['object'].shutdown()
			del self.__server['thread']
			del self.__server['object']
			self.__is_running = False
			self.__server['thread'] = None
			self.__server['object'] = None
		else:
			raise PyRFT_Server_InvalidState('Server is NOT running.')


def pyrft_server(host='localhost', port='9000'):
	"""
	Create a PyRFT Server and start it
	"""
	server = PyRFT_Server(host=host, port=port)
	server.start()
	return server

