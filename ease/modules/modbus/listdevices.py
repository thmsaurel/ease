#!/usr/bin/python
###############################################################################
#
# File Name         : listdevices.py
# Created By        : Thomas Aurel
# Creation Date     : May 11th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:21:46 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import socket

from models.emodule import EModule
from emodules.eemmodbus import EModuleModbus


class Module(EModuleModbus):
    """
    """
    infos = {
            'Name': 'List Modbus Device',
            'Author': ['thms'],
            'Description': 'List all Device wich talk Modbus'
            }

    options = {
            'HOST': ['', True, 'The target address'],
            'PORT': [502, True, 'The target port'],
            'THREADS': [1, False, 'Number of parallel threads running'],
            }

    succeded = False

    def __init__(self, **kwargs):
        EModuleModbus.__init__(self, **kwargs)

    def run(self, **kwargs):
        EModuleModbus.run(self, **kwargs)
        if not self.succeded:
            kwargs['msg'] = 'No Modbus Device on %s' % self.options['HOST'][0]
            self.fail(**kwargs)

    def do(self, **kwargs):
        kwargs = EModule.do(self, **kwargs)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((kwargs['host'], self.options['PORT'][0]))
            kwargs['msg'] = '%s - modbus device' % kwargs['ip'],
            self.success(**kwargs)
            self.succeded = True
        except:
            pass
        return kwargs
