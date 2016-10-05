#!/usr/bin/python
###############################################################################
#
# File Name         : eobjectfactoryecommand.py
# Created By        : Thomas Aurel
# Creation Date     : June 23th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 04:45:07 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import re

from ecommands.eecback import ECommandBack
from ecommands.eecdeveloper import (ECommandClear, ECommandCmd, ECommandDebug,
                                    ECommandEdit)
from ecommands.eecenvironment import ECommandEnvironment
from ecommands.eecexit import ECommandExit
from ecommands.eechelp import ECommandHelp
from ecommands.eecrun import ECommandRun
from ecommands.eecset import ECommandSet
from ecommands.eecsetglobal import ECommandSetGlobal
from ecommands.eecshow import ECommandShow
from ecommands.eecuse import ECommandUse
from models.eobjectfactory import EObjectFactory


class EOFCommand(EObjectFactory):
    """
    The EObjectFactory Class for ECommand
    """

    def __init__(self, **kwargs):
        EObjectFactory.__init__(self, **kwargs)

    def getECommand(self, **kwargs):  # {{{
        """
        Get a ECommand value from the input user

        @param _o: the input user
        @return: a new dictionary wich is clean of all useless elements
        """
        d = self.getDefaultVariable(**kwargs)
        if len(kwargs['_o']) > 0:
            d['_o'] = self.getDefaultCommand(input=kwargs['_o'][0])
            if not d['_o']:
                d['_o'] = self.getDeveloperCommand(input=kwargs['_o'][0])
            if len(kwargs['_o']) > 1:
                d['payload'] = self.getPayload(
                        command=d['_o'], input=kwargs['_o'][1:])
        else:
            d['_o'] = kwargs['_o']
        return d
    # }}}

    def getDefaultCommand(self, **kwargs):  # {{{
        """
        Get a default ECommand object

        @param input: the first element of the user input
        @return: a ECommand object if it exist, else None
        """
        if not self._isKeyDict(_l='input', **kwargs):
            return None
        if kwargs['input'] in ['back']:
            return ECommandBack()
        if kwargs['input'] in ['env']:
            return ECommandEnvironment()
        if kwargs['input'] in ['exit', 'quit']:
            return ECommandExit()
        if kwargs['input'] in ['help']:
            return ECommandHelp()
        if kwargs['input'] in ['run']:
            return ECommandRun()
        if kwargs['input'] in ['set']:
            return ECommandSet()
        if kwargs['input'] in ['setglobal', 'setg']:
            return ECommandSetGlobal()
        if kwargs['input'] in ['show']:
            return ECommandShow()
        if kwargs['input'] in ['use']:
            return ECommandUse()
        return None
    # }}}

    def getDeveloperCommand(self, **kwargs):  # {{{
        """
        Get a developer ECommand object

        @param input: the first element of the user input
        @return: a ECommand object if it exist, else None
        """
        if not self._isKeyDict(_l='input', **kwargs):
            return None
        if kwargs['input'] in ['clear']:
            return ECommandClear()
        if kwargs['input'] in ['edit']:
            return ECommandEdit()
        if kwargs['input'] in ['debug']:
            return ECommandDebug()
        if re.match(r'^!.*$', kwargs['input']):
            return ECommandCmd()
        return None
    # }}}

    def getPayload(self, **kwargs):  # {{{
        """
        Get a payload for the command

        @param command: a ECommand object
        @param input: a list which all user input (except the first one)
        @return: a string or list (depends of ECommand) if exist, else None
        """
        if not self._isKeyDict(_l=['command', 'input'], **kwargs):
            return []
        if not kwargs['command'] or not kwargs['input']:
            return []
        if (
                isinstance(kwargs['command'], ECommandEnvironment) or
                isinstance(kwargs['command'], ECommandSet) or
                isinstance(kwargs['command'], ECommandSetGlobal) or
                isinstance(kwargs['command'], ECommandShow) or
                isinstance(kwargs['command'], ECommandUse)
                ):
            return kwargs['input']
        if isinstance(kwargs['command'], ECommandHelp):
            return [self.getECommand(_o=kwargs['input'])['_o']]
        if isinstance(kwargs['command'], ECommandCmd):
            return [' '.join(kwargs['input'])]
        return []
    # }}}
