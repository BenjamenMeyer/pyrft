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
import uuid
import logging
from collections import deque

from .comms import PyRFTConnection, PyRFTConnectionInvalidState
from .config import PyRFTConfig


class PyRFTServerInvalidState(PyRFTConnectionInvalidState):
    pass


class PyRFTServerAssociationError(Exception):
    pass


class _threaded_tcp_server(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.__client_connections = {}
        self.__client_associations = {}
        self.__client_lock = threading.RLock()
        self.log = logging.getLogger(__name__)

    def register_connection(self, connection_id, connection_type, handler):
        """
        Register a connection
        """
        with self.__client_lock:
            self.__client_connections[connection_id] = {'type': connection_type, 'handler': handler}

            if connection_type == PyRFTServerHandler.CONNECTION_TYPE_CONTROLLER:
                self.__client_associations[connecdtion_id] = {}

    def deregister_connection(self, connection_id):
        """
        Remove the connection registration
        """
        with self.__client_lock:
            if connection_id in self.__client_connections:
                if self.__client_connections[connection_id]['type'] == PyRFTServerHandler.CONNECTION_TYPE_WORKER:
                    self.deassociate_connection(connection_id)

                del self.__client_connections[connection_id]

    def associate_connection(self, connection_id, controller_id):
        """
        Associate a worker connection with the controller connection
        """
        with self.__client_lock:
            if connection_id not in self.__client_connections:
                raise PyRFTServerAssociationError('Specified Connection ID not registered')

            if self.__client_connections['type'] != PyRFTServerHandler.CONNECTION_TYPE_WORKER:
                raise PyRFTServerAssociationError('Only workers can be associated with controllers')

            if controller_id not in self.__client_associations:
                raise PyRFTServerAssociationError('Specified Controller not present')

            # ensure there are no existing associations
            for alternate_controller_id, controller_associations in self.__client_associations.items():
                if connection_id in controller_associations:
                    raise PyRFTServerAssociationError('Connection is already associated')

            self.__client_associations[controller_id].append(connection_id)
            self.notify_controller(connection_id, {'type': 'association', 'action': 'add', 'id': connection_id})

    def deassociation_connection(self, connection_id):
        """
        Remove the worker connection association
        """
        with self.__client_lock:
            for controller_id, controller_associations in self.__client_associations.items():
                if connection_id in controller_associations:
                    self.notify_controller(connection_id, {'type': 'association', 'action': 'remove', 'id': connection_id})
                    del controller_associations[connection_id]

    def notify_associates(self, connection_id, message):
        """
        Pass a message on to all workers
        """
        with self.__client_lock:
            if connection_id in self.__client_associations:
                for associated_connection in self.__client_associations[connection_id]:
                    associated_connection['handler'].send_internal_message(message)

    def notify_controller(self, connection_id, message):
        """
        Pass a message to the controller
        """
        with self.__client_lock:
            if connection_id in self.__client_connections:
                for controller_id, controller_associations in self.__client_associations.items():
                    if connection_id in controller_associations:
                        if controller_id in self.__client_connections:
                            self.__client_connections[controller_id]['handler'].send_internal_message(message)
                        else:
                            raise PyRFTServerAssociationError('Unable to locate controller specifiec connections ({0:})'.format(connection_id))
                        break


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
        self.log = logging.getLogger(__name__)

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
        self.log = logging.getLogger(__name__)

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
            self.__server['object'] = _threaded_tcp_server((self.host, self.port), PyRFTServerHandler)
            self.__server['thread'] = threading.Thread(target=self.__server['object'].serve_forever)
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
    CONNECTION_TYPE_UNKNOWN = 'UNKNOWN'
    CONNECTION_TYPE_CONTROLLER = 'CONTROLLER'
    CONNECTION_TYPE_WORKER = 'WORKER'
    CONNECTION_TYPE_ADMINISTATOR = 'ADMINISTRATOR'

    def __init_me(self):
        """
        """
        self.__lock = threading.RLock()
        self.__session_id = uuid.uuid4()
        self.__session_type = PyRFTServerHandler.CONNECTION_TYPE_UNKNOWN
        self.__session_message_queue = deque()
        self.log = logging.getLogger(__name__)

    def handle(self):
        """
        """
        self.__init_me()
        self.log.debug('Received connection from {0:}'.format(self.client_address))

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
        try:
            # Once we figure out if we are a controller or worker we can do the following:
            # self.server.register_connection(self.session_id, self.session_type, self)

            while True:
                if self.has_internal_message:
                    internal_message = self.get_internal_message()
                    self.handle_internal_message(internal_message)

        finally:
            self.server.deregister_connection(self.__session_id)

    def handle_internal_message(self, message):
        """
        """
        message_handled = False

        if message['type'] == 'association':
            if message['action'] == 'add':
                self.log.info('Request Handler ({0:|) has worker connection {1:}'.format(self.__session_id, message['id']))

            elif message['action'] == 'remove':
                self.log.info('Request Handler ({0:|) lost worker connection {1:}'.format(self.__session_id, message['id']))

        if not message_handled:
            self.log.error('Internal Message for Request Handler ({0:}) was not handled: {1:}'.format(self.__session_id, message))

    @property
    def has_internal_message(self):
        """
        Is there an internal, inter-thread message waiting for the handler?
        """
        with self.__lock:
            return (len(self.__session_message_queue) > 0)

    def get_internal_message(self):
        """
        Pop an internal, inter-thread message from the handler's queue
        """
        with self.__lock:
            if self.has_internal_message:
                return self.__session_message_queue.popleft()

    def send_internal_message(self, message):
        """
        Push an internal, inter-thread message to the handler's queue
        """
        with self.__lock:
            self.__session_message_queue.append(message)
