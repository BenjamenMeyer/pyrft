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


class PyRFTConnectionInvalidState(Exception):
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
        self.__host = host_address

    @property
    def port(self):
        """
        Port for the connection
        """
        return self.__port

    @port.setter
    def port(self, port_number):
        """
        Set the Port for the connection
        """
        self.__port = port_number
