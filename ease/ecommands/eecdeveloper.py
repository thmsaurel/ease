#!/usr/bin/python
###############################################################################
#
# File Name         : eecdeveloper.pyw
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 12:57:07 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand
from ecommands.eecuse import ECommandUse
import os
import sys


class ECommandClear(ECommand):  # {{{
    """
    Clear the terminal screen (use clear system command)
    """

    def execute(self, **kwargs):  # {{{
        """
        Clear the screen

        @return: the main dictionary
        """
        os.system('clear')
        return kwargs
    # }}}
# }}}


class ECommandCmd(ECommand):  # {{{
    """
    Execute the given command
    """

    def execute(self, **kwargs):  # {{{
        """
        Execute the payload command

        @param payload: the command to execute
        @return: the main dictionary
        """
        if self._hasPayload(**kwargs):
            os.system(' '.join(kwargs['payload']))
        return kwargs
    # }}}
# }}}


class ECommandDebug(ECommand):  # {{{
    """
    Launch a Python Shell
    """

    def execute(self, **kwargs):  # {{{
        """
        launch a python shell

        @return: the main dictionary
        """
        os.system('python')
        return kwargs
    # }}}
# }}}


class ECommandEdit(ECommand):  # {{{
    """
    Edit the selected module
    """

    def execute(self, **kwargs):  # {{{
        """
        edit the selected module

        @param module: the module to modify source code
        @return: the main dictionary with the modified module
        """
        if not self._hasModule(**kwargs):
            return kwargs
        m = kwargs['module']
        # print sys.modules[kwargs['module'].__module__].__file__
        mp = sys.modules[kwargs['module'].__module__].__file__[:-1]
        # print mp
        os.system('$EDITOR ' + mp)
        kwargs['paylpad'] = [kwargs['module'].__module__, ]
        e = ECommandUse()
        kwargs = e.execute(**kwargs)
        kwargs['module'].options = m.options
        return kwargs
    # }}}
# }}}
