#!/usr/bin/python
##############################################################################
#
# File Name         : environment.py
# Created By        : Thomas Aurel
# Creation Date     : April 19th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 04:46:52 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from core.eobject import EObject


class EEnvironment(EObject):
    """
    The EEnvironment Class
    """

    def __init__(self, **kwargs):  # {{{
        """
        The default constructor for EEnvironment

        @param config: the EConfiguration object
        """
        EObject.__init__(self, **kwargs)
        self.globaloptions = {}
        if not self._hasConfig(**kwargs):
            self.mode = 0
        elif not kwargs['config']._hasKey(
                section='user', key='default_mode', **kwargs):
            self.mode = 0
        else:
            self.debug = kwargs['config'].get(
                    section='user', key='default_mode', **kwargs)
    # }}}

    def getClassname(self, **kwargs):  # {{{
        """
        The default getClassname function use to returned the name of the
        EObject class name
        If this method is called, the eobject subclass doesn't have a override
        of this function

        @return: None
        """
        return "EEnvironment"
    # }}}

    def addGlobal(self, **kwargs):  # {{{
        """
        Add setGlobal value inside the environment (call by setGlobalCommand)
        """
        self.globaloptions[kwargs['payload'][0]] = \
            ' '.join(kwargs['payload'][1:])
    # }}}

    def getMode(self, **kwargs):  # {{{
        """
        return a conversion between debug value and a string

        @retturn: a converted value into string
        """
        if not self.debug:
            return 'CLASSIC'
        return 'DEBUG'
    # }}}
