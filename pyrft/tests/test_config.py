"""
"""

def test_config():
    """
    """
    from pyrft.config import PyRFTConfig

    assert PyRFTConfig.UNLIMITED == -1

    config = PyRFTConfig()

    assert config.maximumConnections == PyRFTConfig.MAX_CONNECTIONS_DEFAULT
    assert config.maximumDataConnections == PyRFTConfig.MAX_DATA_CONNECTIONS_DEFAULT
    assert config.maximumBandwidthUsage == PyRFTConfig.MAX_BANDWIDTH_USAGE_DEFAULT
    assert config.maximumBandwidthPerTransfer == PyRFTConfig.MAX_BANDWIDTH_USAGE_PER_TRANSFER_DEFAULT

def test_negotiate_unlimited():

    from pyrft.config import PyRFTConfig

    assert PyRFTConfig.negotiate_unlimited(-1, 'right') == 'right'
    assert PyRFTConfig.negotiate_unlimited('left', -1) == 'left'

    assert PyRFTConfig.negotiate_unlimited(0, 5) == 0
    assert PyRFTConfig.negotiate_unlimited(5, 0) == 0

def test_negotiation():

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

    config_test = PyRFTConfig()
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

