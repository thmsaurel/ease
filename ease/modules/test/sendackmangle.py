#!/usr/bin/python
###############################################################################
#
# File Name         : sendackmangle.py
# Created By        : Thomas Aurel
# Creation Date     : June 16th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:20:15 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from emodules.eemtest import EModuleTest


class Module(EModuleTest):
    """
    """

    infos = {
            'Name': '',
            'Author': ['thms'],
            'Description': ''
            }

    options = {
            'HOST': ['', True, 'The target address'],
            'PORT': ['', True, 'The target port'],
            'THREADS': [1, False, 'Number of parallel threads running'],
            'SRCPORT': [None, False, 'The source port'],
            'SRCIP': [None, False, 'The source ip'],
            'PAYLOAD': ['', True, 'The malicious payload used by the attack']
            }

    def __init__(self, **kwargs):
        EModuleTest.__init__(self, **kwargs)

    def run(self, **kwargs):
        EModuleTest.run(self, **kwargs)

    def do(self, **kwargs):
        EModuleTest.do(self, **kwargs)

    def verify(self, **kwargs):
        EModuleTest.verify(self, **kwargs)
