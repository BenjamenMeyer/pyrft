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


import socket

from .comms import PyRFTConnection, PyRFTConnectionInvalidState
from .config import PyRFTConfig


class PyRFTClientInvalidState(PyRFTConnectionInvalidState):
	pass


class PyRFTClientConfig(PyRFTConfig):
	"""
	"""
	
	def __init__(self):
		super().__init__()
	
	def negotiate(self, other):
		settle = super().negotiate(other)
		return settle


class PyRFTClient(PyRFTConnection):
	"""
	PyRFT Client Interface

	Wrapper around the client instance to enable easy management.

	Client connects to the specified host/port.
	"""

	def __init__(self, host, port, config=PyRFTClientConfig):
		"""
		Initializer
		"""
		super().__init__(host, port)
		self.__config = config
		self.__is_active = False
		self.__client = {}
		self.__client['socket'] = None
	
	@property
	def isActive(self):
		"""
		Determine the client status

		Returns True if the client is connected to a server.
		Returns False if the client is disconnected.
		"""
		return (self.__is_active is True)
	
	def connect(self, host=None, port=None):
		"""
		Connect to the specified server

		Throws PyRFTClientInvalidState if already connected
		"""
		if not self.isActive:

			if host is not None:
				self.host = host

			if port is not None:
				self.port = port

			self.__client['socket'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.__client['socket'].connect((self.host, self.port))

		else:
			raise PyRFTClientInvalidState('Already connected.')
	
	def disconnect(self):
		"""
		Disconnects from the server

		Throws PyRFTClientConnection if not connected
		"""
		if self.isActive:
			self.__client['socket'].close()
			del self.__client['socket']
			self.__client['socket'] = None

		else:
			raise PyRFTClientConnection('Not connected.')
