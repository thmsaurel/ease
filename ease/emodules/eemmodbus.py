#!/usr/bin/python
###############################################################################
#
# File Name         : modbus.py
# Created By        : Thomas Aurel
# Creation Date     : May 25th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:23:31 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import random

from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse

from models.emodule import EModule


class EModuleModbus(EModule):
    """
    """
    def __init__(self, **kwargs):
        EModule.__init__(self, **kwargs)

# #############################################################################
#   Main EModule Methods
# #############################################################################

    def run(self, **kwargs):  # {{{
        """
        Use to launch all attacks instances and all option verifications
        """
        EModule.run(self, **kwargs)
    # }}}

    def do(self, **kwargs):  # {{{
        """
        An instance attack

        @return: the main dictionary
        @raise: a exception if no socket are created
        """
        kwargs = EModule.do(self, **kwargs)
        kwargs['socket'] = self.initsocket(**kwargs)
        if not self._hasSocket(**kwargs):
            self.error(msg="Can't create a socket", **kwargs)
            raise
        return kwargs
    # }}}

# #############################################################################
#   Verify if the options dict has correct values
# #############################################################################

    def verify(self, **kwargs):  # {{{
        """
        Verify some element from module class

        @return: False if no error is raise, else True
        """
        error = EModule.verify(self, **kwargs)
        if 'PERIOD' in self.options:  # {{{
            p = self.options['PERIOD'][0]
            try:
                period = int(p)
            except:
                self.error(msg='"%s" is an invalid time' % p, **kwargs)
                error = True
            if period < 0:
                self.error(msg='"%s" is an invalid time' % p, **kwargs)
                error = True
        # }}}
        return error
    # }}}

# #############################################################################
#   Auxiliary Usefull Methods for Module
# #############################################################################

    def modbusRequest(self, **kwargs):  # {{{
        """
        Get the modbus request base

        @return: the modbus request base
        """
        return ModbusADURequest(transId=random.randint(1, 65535))
    # }}}

    def sendmessagesocket(self, **kwargs):  # {{{
        """
        Get a modbus response to an umas request

        @return: the modbus response
        """
        rp = EModule.sendmessagesocket(self, **kwargs)
        return ModbusADUResponse(rp)
    # }}}
