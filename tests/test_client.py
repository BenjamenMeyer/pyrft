"""
"""

def test_client_config():
    """
    """
    from pyrft.client import PyRFTClientConfig
    from pyrft.config import PyRFTConfig

    base_config = PyRFTConfig()
    client_config = PyRFTClientConfig()

    assert isinstance(client_config, PyRFTClientConfig)
    assert isinstance(client_config, PyRFTConfig)

    assert isinstance(base_config, PyRFTConfig)

    assert client_config.maximumConnections == base_config.maximumConnections
    assert client_config.maximumDataConnections == base_config.maximumDataConnections
    assert client_config.maximumBandwidthUsage == base_config.maximuMBandwidthUsage
    assert client_config.maximuBandwidthPerTransfer == base_config.maximumBandwidthPerTransfer

def test_negotiation():

    from pyrft.client import PyRFTClientConfig
    from pyrft.config import PyRFTConfig

    config_left = PyRFTConfig()
    config_right = PyRFTConfig()

    config_left.maximumConnections = 1500
    config_left.maximumDataConnections = 5
    config_left.maximumBandwidthUsage = 20
    config_left.maximumBandwidthPerTransfer = 30

    config_right.maximumConnections = 1200
    config_right.maximumDataConnections = 2
    config_right.maximumBandwidthUsage = 40
    config_right.maximumBandwidthPerTransfer = 50

    config_test = PyRFTClientConfig()
    config_test.maximumConnections = 5000
    config_test.maximumDataConnections = 10
    config_test.maximumBandwidthUsage = -1
    config_test.maximumBandwidthPerTransfer = -1

    settlement_left = config_test.negotiate(config_left)

    assert settlement_left.maximumConnections == config_left.maximumConnections
    assert settlement_left.maximumDataConnections == config_left.maximumDataConnections
    assert settlement_left.maximumBandwidthUsage == config_left.maximumBandwidthUsage
    assert settlement_left.maximumBandwidthPerTransfer == config_left.maximumBandwidthPerTransfer

    settlement_right = config_test.negotiate(config_right)

    assert settlement_right.maximumConnections == config_right.maximumConnections
    assert settlement_right.maximumDataConnections == config_right.maximumDataConnections
    assert settlement_right.maximumBandwidthUsage == config_right.maximumBandwidthUsage
    assert settlement_right.maximumBandwidthPerTransfer == config_right.maximumBandwidthPerTransfer

