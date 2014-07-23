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

from .comms import PyRFTConnection, PyRFTConnectionInvalidState
from .config import PyRFTConfig

class PyRFTServerInvalidState(PyRFTConnectionInvalidState):
	pass


class __threaded_tcp_server(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass




class PyRFTServerConfig(PyRFTConfig):
	"""
	"""

	# Maximum Number of Command Connections
	MAX_CONNECTIONS = 'maximumConnections'
	MAX_CONNECTIONS_DEFAULT = 10

	# Maximum Available Bandwidth for All Clients
	MAX_AVAILABLE_BANDWIDTH = 'maximumAvailableBandwidth'
	MAX_AVAILABLE_BANDWIDTH_DEFAULT = PyRFTConfig.UNLIMITED
	
	def __init__(self):
		super().__init__()
		self.__setattr__(PyRFTServerConfig.MAX_CONNECTIONS, PyRFTServerConfig.MAX_CONNECTIONS_DEFAULT)
		self.__setattr__(PyRFTServerConfig.MAX_AVAILABLE_BANDWIDTH, PyRFTServerConfig.MAX_AVAILABLE_BANDWIDTH_DEFAULT)
	
	def negotiate(self, other):
		settle = super().negotiate(other)
		return settle


class PyRFTServer(PyRFTConnection):
	"""
	PyRFT Server Interface

	Wrapper around the server instance to enable easy management.

	Server binds to the specified host/port. Each client connection is
	handled in its own thread.
	"""

	def __init__(self, host, port, config=PyRFTServerConfig):
		"""
		Initializer
		"""
		super().__init__(host, port)
		self.__is_running = False
		self.__config = config
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

		Throws PyRFTServerInvalidState if the server is already running.
		"""
		if not self.isRunning:
			self.__server['object'] = __threaded_tcp_server((host, port), PyRFTServerHandler)
			self.__server['thread'] = threading.Thread(target=server.serve_forever)
			self.__server['thread'].daemon = True
			self.__server['thread'].start()
			self.__is_running = True
		else:
			raise PyRFTServerInvalidState('Server is ALREADY running.')

	def stop(self):
		"""
		Stop the server and release the resources.

		Throws PyRFTServerInvalidState if the server is not running.
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
			raise PyRFTServerInvalidState('Server is NOT running.')


class PyRFTServerHandler(socketserver.StreamRequestHandler):
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

