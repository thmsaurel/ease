#!/usr/bin/python
###############################################################################
#
# File Name         : eecexit.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:13:45 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand
import sys


class ECommandExit(ECommand):
    """
    Quit ease
    Usage into cli interface: (exit|quit)
    """

    def execute(self, **kwargs):  # {{{
        """
        Exit the program
        """
        self.info(msg='Bye !', **kwargs)
        sys.exit(0)
    # }}}
