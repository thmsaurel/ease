#!/usr/bin/python
###############################################################################
#
# File Name         : memorycartoraphy.py
# Created By        : Thomas Aurel
# Creation Date     : April 21th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:22:05 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import threading
import time

from scapy.contrib.modbus import (ModbusPDU01ReadCoilsRequest,
                                  ModbusPDU02ReadDiscreteInputsRequest,
                                  ModbusPDU03ReadHoldingRegistersRequest,
                                  ModbusPDU04ReadInputRegistersRequest)

from emodules.eemmodbus import EModuleModbus


class Module(EModuleModbus):
    """
    """
    infos = {
            'Name': 'PLC Memory Cartography',
            'Author': ['thms'],
            'Description': 'Create a PLC Memory Cartography'
            }

    options = {
            'HOST': ['', True, 'The target address'],
            'PORT': [502, True, 'The target port'],
            'THREADS': [1, False, 'Number of parallel threads running'],
            'PERIOD': [
                0, False, 'Number of waiting second between requests'],
            }

    threadTarget = {
            'Thread_RC': [
                ModbusPDU01ReadCoilsRequest,
                'ModbusPDU01ReadCoilsResponse',
                'Coils'],
            'Thread_RDI': [
                ModbusPDU02ReadDiscreteInputsRequest,
                'ModbusPDU02ReadDicreteInputsResponse',
                'Discrete Inputs'],
            'Thread_RHR': [
                ModbusPDU03ReadHoldingRegistersRequest,
                'ModbusPDU03ReadHoldingRegistersResponse',
                'Holding Registers'],
            'Thread_RIR': [
                ModbusPDU04ReadInputRegistersRequest,
                'ModbusPDU04ReadInputRegistersResponse',
                'Inputs Registers'],
                }

    def __init__(self, **kwargs):
        EModuleModbus.__init__(self, **kwargs)

    def run(self, **kwargs):
        t = time.time()
        EModuleModbus.run(self, **kwargs)
        kwargs['msg'] = 'Cartography Realised in %s seconds' % str(
                time.time() - t)
        self.success(**kwargs)

    def do(self, **kwargs):  # {{{
        threads = []
        for k in self.threadTarget.keys():
            thread = threading.Thread(
                    name=k,
                    target=self.do_read,
                    kwargs=kwargs)
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()
    # }}}

    def do_read(self, **kwargs):  # {{{
        try:
            kwargs = EModuleModbus.do(self, **kwargs)
        except:
            return
        result = []
        thread = threading.currentThread()
        for i in range(0x0000, 0x010000):
            kwargs['request'] = self.modbusRequest()/self.threadTarget[
                    thread.name][0](startAddr=i)
            rp = self.sendmessagesocket(**kwargs)
            if rp.payload.__class__.__name__ == \
                    self.threadTarget[thread.name][1]:
                result.append(i)
            if self.options['PERIOD'][0] > 0:
                time.sleep(self.options['PERIOD'][0])
        kwargs['socket'].close()
        if len(result) != 0:
            kwargs['result'] = result
            kwargs['target'] = self.threadTarget[thread.name][2]
            self.print_result(**kwargs)
    # }}}

    def print_result(self, **kwargs):  # {{{
        if 'result' not in kwargs and 'target' not in kwargs:
            self.error(msg='result and/or target are not define', **kwargs)
            raise
        start = None
        j = None
        for i in kwargs['result']:
            if start is None:
                start = i
            elif i != j+1:
                kwargs['msg'] = 'The PLC (%s) is readable from %s to %s %s' % (
                        kwargs['ip'], str(start), str(j), kwargs['target'])
                self.info(**kwargs)
                start = i
            j = i
        kwargs['msg'] = 'The PLC (%s) is writable from %d to %d %s' % (
                kwargs['ip'], start, j, kwargs['target'])
        self.info(**kwargs)
    # }}}
