#!/usr/bin/python
###############################################################################
#
# File Name         : eecback.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 12:56:55 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandBack(ECommand):
    """
    Return to initial context
    Usage into cli interface: back
    """

    def execute(self, **kwargs):  # {{{
        """
        Remove the module from the main dictionary

        @param kwargs: the main dictionary
        @return: the main dictionary whithout the module element
        """
        if self._hasModule(**kwargs):
            del kwargs['module']
        return kwargs
    # }}}
