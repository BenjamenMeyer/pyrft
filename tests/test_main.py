"""
"""

def test_server():
    from pyrft import create_server
    from pyrft.server import PyRFTServer

    server = create_server(host='127.0.0.2', port=9010)

    assert isinstance(server, PyRFTServer)

    assert server.isRunning

    server.stop()

    assert not server.isRunning

    del server


def test_server_client():
    from pyrft import create_server, create_client
    from pyrft.client import PyRFTTransferClient
    from pyrft.server import PyRFTServerHandler
    server = create_server(host='127.0.0.3', port=9020)

    assert server.isRunning

    client = create_client(host='127.0.0.3', port=9020)

    assert isinstance(client, PyRFTTransferClient)

    assert (client.connectionType == PyRFTServerHandler.CONNECTION_TYPE_CONTROLLER)

    assert client.isActive

    client.disconnect()

    assert not client.isActive

    del client
    del server


def test_server_data_client():
    from pyrft import create_server, create_client
    from pyrft.client import PyRFTTransferDataClient
    from pyrft.server import PyRFTServerHandler
    server = create_server(host='127.0.0.3', port=9020)

    assert server.isRunning

    client = PyRFTTransferDataClient(host='127.0.0.3', port=9020)

    assert not client.isActive

    assert (client.connectionType == PyRFTServerHandler.CONNECTION_TYPE_WORKER)

    client.connect()

    assert client.isActive

    client.disconnect()

    assert not client.isActive

    del client
    del server


def test_server_admin():
    from pyrft import create_server, create_admin_client
    from pyrft.client import PyRFTAdminClient
    from pyrft.server import PyRFTServerHandler
    server = create_server(host='127.0.0.4', port=9030)

    assert server.isRunning

    client = create_admin_client(host='127.0.0.4', port=9030)

    assert isinstance(client, PyRFTAdminClient)

    assert (client.connectionType == PyRFTServerHandler.CONNECTION_TYPE_ADMINISTATOR)

    assert client.isActive

    client.disconnect()

    assert not client.isActive

    del client
    del server
