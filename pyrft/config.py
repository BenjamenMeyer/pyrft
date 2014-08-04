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


class PyRFTConfig(object):
    """
    """
    UNLIMITED = -1

    # Maximum Connections (Server-Side)
    MAX_CONNECTIONS = 'maximumConnections'
    MAX_CONNECTIONS_DEFAULT = 2000

    # Maximum Number of Data Transfer Connections
    MAX_DATA_CONNECTIONS = 'maximumDataConnections'
    MAX_DATA_CONNECTIONS_DEFAULT = 10

    # Maximum Bandwidth to use for all on-going file transfers (default: -1, aka unlimited)
    MAX_BANDWIDTH_USAGE = 'maximumBandwidthUsage'
    MAX_BANDWIDTH_USAGE_DEFAULT = UNLIMITED

    # Maximum Bandwidth to use for any given file transfer
    MAX_BANDWIDTH_USAGE_PER_TRANSFER = 'maximumBandwidthPerTransfer'
    MAX_BANDWIDTH_USAGE_PER_TRANSFER_DEFAULT = UNLIMITED

    def __init__(self):
        self.__setattr__(PyRFTConfig.MAX_CONNECTIONS, PyRFTConfig.MAX_CONNECTIONS_DEFAULT)
        self.__setattr__(PyRFTConfig.MAX_DATA_CONNECTIONS, PyRFTConfig.MAX_DATA_CONNECTIONS_DEFAULT)
        self.__setattr__(PyRFTConfig.MAX_BANDWIDTH_USAGE, PyRFTConfig.MAX_BANDWIDTH_USAGE_DEFAULT)
        self.__setattr__(PyRFTConfig.MAX_BANDWIDTH_USAGE_PER_TRANSFER, PyRFTConfig.MAX_BANDWIDTH_USAGE_PER_TRANSFER_DEFAULT)

    def enforce(self):
        self.maximumBandwidthPerTransfer = max(self.maximumBandwidthPerTransfer, self.maximuBandwidthUsage)

    @staticmethod
    def negotiate_unlimited(left, right):
        if left == -1:
            return right
        elif right == -1:
            return left
        else:
            return min(left, right)

    def negotiate(self, other):

        settle = PyRFTConfig()

        # Max # of Data Transfer Connections
        settle.maximumDataConnections = PyRFTConfig.negotiate_unlimited(self.maximumDataConnections, other.maximumDataConnections)

        #
        settle.maximumConnections = min(self.maximumConnections, other.maximumConnections)
        settle.maximumBandwidthUsage = PyRFTConfig.negotiate_unlimited(self.maximumBandwidthUsage, other.maximumBandwidthUsage)
        settle.maximumBandwidthPerTransfer = PyRFTConfig.negotiate_unlimited(self.maximumBandwidthPerTransfer, other.maximumBandwidthPerTransfer)

        return settle
