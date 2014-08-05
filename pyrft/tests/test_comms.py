"""
"""

def test_pyrft_connection():
	"""
	"""
	from pyrft.comms import PyRFTConnection

	test_connection = PyRFTConnection('test_host', 'test_port')

	assert test_connection.host == 'test_host'
	assert test_connection.port == 'test_port'

	test_connection.host = 'host_test'

	assert test_connection.host == 'host_test'
	assert test_connection.port == 'test_port'

	test_connection.port = 'port_test'

	assert test_connection.host == 'host_test'
	assert test_connection.port == 'port_test'
