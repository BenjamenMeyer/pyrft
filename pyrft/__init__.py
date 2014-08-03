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

from .server import PyRFTServer, PyRFTServerConfig
from .client import PyRFTTransferClient, PyRFTAdminClient, PyRFTClientConfig

__default_port = 9000


def create_server(host='localhost', port=__default_port,
        config=PyRFTServerConfig):
    """
    Create a PyRFT Server Instance and start listening for clients
    """
    server = PyRFTServer(host=host, port=port, config=config)
    server.start()
    return server


def create_client(host='localhost', port=__default_port,
        config=PyRFTClientConfig):
    """
    Create a PyRFT Client Instance and connect to the server
    """
    client = PyRFTTransferClient(host=host, port=port, config=config)
    client.connect()
    return client


def create_admin_client(host='localhost', port=__default_port):
    """
    Create a PyRFT Administrative Client Instance and connect to the server
    """
    import uuid
    admin_client = PyRFTAdminClient(host=host, port=port, controller_id=uuid.uuid4())
    admin_client.connect()
    return admin_client
