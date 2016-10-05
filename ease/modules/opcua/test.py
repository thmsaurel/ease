#!/usr/bin/python
###############################################################################
#
# File Name         : test.py
# Created By        : Thomas Aurel
# Creation Date     : July  4th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:22:58 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from emodules.eemopcua import EModuleOpcua
from protocols.opcua import (OPCUACreateSessionRequest, OPCUAHelloRequest,
                             OPCUAOpenSecureChannelIdRequest)


class Module(EModuleOpcua):
    options = {
            'HOST': ['', True, 'The target address'],
            'PORT': [51210, False, 'The target port'],
            'THREADS': [1, False, 'Number of parallel threads running'],
            }

    infos = {
            'Name': 'Test EModuleTest',
            'Author': ['thms'],
            'Description': 'Test EModuleTest'
            }

    THREADS = []

    def run(self, **kwargs):
        """
        Use to launch all attacks instances and all option verifications
        """
        EModuleOpcua.run(self, **kwargs)

    def do(self, **kwargs):
        kwargs = EModuleOpcua.do(self, **kwargs)
        kwargs['request'] = OPCUAHelloRequest()
        kwargs['request'].endPointUrl = \
            'opc.tcp://factory3-pc:51210/UA/SampleServer'
        # kwargs['request'].show()
        rp = self.sendmessagesocket(**kwargs)
        if rp.__class__.__name__ != 'OPCUAAckResponse':
            self.error(msg="don't received a acknowledge message", **kwargs)
            return kwargs
        kwargs['request'] = OPCUAOpenSecureChannelIdRequest()
        kwargs['request'].securityPolicyUri = \
            "http://opcfoundation.org/UA/SecurityPolicy#None"
        kwargs['request'].sequenceNumber = 1
        kwargs['request'].requestId = 2
        rp = self.sendmessagesocket(**kwargs)
        if rp.__class__.__name__ != 'OPCUAOpenSecureChannelIdResponse':
            self.error(msg="don't received a open message response")
            return kwargs
        kwargs['secure_channel_id'] = rp.secureChannelId
        kwargs['request'] = OPCUACreateSessionRequest()
        rp = self.sendmessagesocket(**kwargs)
