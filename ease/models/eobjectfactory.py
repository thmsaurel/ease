#!/usr/bin/python
###############################################################################
#
# File Name         : eobjectfactory.py
# Created By        : Thomas Aurel
# Creation Date     : June 23th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 04:45:01 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from core.eobject import EObject


class EObjectFactory(EObject):
    """
    The default EObjectFactory Class

    Used to return a dictionnary of one EObject subclass
    """

    def __init__(self, **kwargs):
        EObject.__init__(self, **kwargs)

    def getDefaultVariable(self, **kwargs):  # {{{
        """
        Return a dict with the default variables for ease

        @param kwargs: the previous dictionnary
        @return: a new dictionnary clean for useless variable
        """
        d = {}
        if self._hasConfig(**kwargs):
            d['config'] = kwargs['config']
        if self._hasInterface(**kwargs):
            d['interface'] = kwargs['interface']
        if self._hasModule(**kwargs):
            d['module'] = kwargs['module']
        if self._hasModules(**kwargs):
            d['modules'] = kwargs['modules']
        if self._hasEnvironment(**kwargs):
            d['environment'] = kwargs['environment']
        return d
    # }}}
