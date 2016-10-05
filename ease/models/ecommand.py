#!/usr/bin/python
###############################################################################
#
# File Name         : ecommand.py
# Created By        : Thomas Aurel
# Creation Date     : June 17th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 10:30:57 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import imp

from core.eexplorer import EExplorer
from core.eobject import EObject


class ECommand(EObject):
    """
    The default ECommand Class
    """
    commands = {
            'back': 'Return to initial context',
            'environment': 'Define environment value',
            'exit': 'Quit ease',
            'help': 'Show this help',
            'run': 'Launch the selected module',
            'set': 'Set an option value for a selected module',
            'setglobal': 'Set an option value for all modules',
            'show': 'Show information about the tool or the current module',
            'use': 'Select a module for your next attack',
            }

    def __init__(self, **kwargs):  # {{{
        EObject.__init__(self, **kwargs)
    # }}}

# #############################################################################
#   Unify Objects Methods
# #############################################################################

    def execute(self, **kwargs):  # {{{
        """
        The default Execute Function for all ECommand object

        @param kwargs: the given dictionary
        @return: the given dictionary with modify values
        """
        kwargs['msg'] = 'implement "execute" for %s command' % (
                self.__class__.__name__)
        self.error(**kwargs)
        return kwargs
    # }}}

# #############################################################################
#   Usefull Function for ECommand class
# #############################################################################

    def getModule(self, **kwargs):  # {{{
        """
        Load and the search Module object

        @param payload: the EConfiguration object
        @param option: a list with all options for the command
        @return: the wanted Module object if it exists, else None
        """
        if not self._hasConfig(**kwargs) or not self._hasPayload(**kwargs):
            return None
        path = self.__getModulePath(**kwargs)
        if path:
            return imp.load_source(kwargs['payload'][0], path).Module(**kwargs)
        return None
    # }}}

    def __getModulePath(self, **kwargs):
        """
        """
        mp = kwargs['config'].get(key='modules_path')
        m = EExplorer.getPath('/'.join([mp, kwargs['payload'][0]]) + '.py')
        if EExplorer.existFile(m):
            return m
        pp = kwargs['config'].get(key='plugins_path') + "modules/"
        p = EExplorer.getPath('/'.join([pp, kwargs['payload'][0]]) + '.py')
        if EExplorer.existFile(p):
            return p
        kwargs['msg'] = 'the file "%s" or "%s" doesn\'t exist' % (m, p)
        self.error(**kwargs)
        return None

    def getClassname(self, **kwargs):  # {{{
        """
        The default getClassname function use to returned the name of the
        EObject class name
        If this method is called, the eobject subclass doesn't have a override
        of this function

        @return: None
        """
        return "ECommand"
    # }}}
