#!/usr/bin/python
###############################################################################
#
# File Name         : eecuse.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 02:10:23 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandUse(ECommand):
    """
    Select a module for your next attack
    Usage into cli interface : use EXPLOIT
    """

    def execute(self, **kwargs):  # {{{
        """
        Select the module to use

        @param payload: the exploit name to select
        @param modules: a list of available modules
        @param environment: the EEnvironment object (optional)
        @return: the main dictionary with the selected module
        """
        if not self._hasPayload(**kwargs):
            self.error(msg='You must select a module', **kwargs)
            return kwargs
        if not self._hasModules(**kwargs):
            self.error(msg='You must add modules path')
            return kwargs
        if kwargs['payload'][0] not in kwargs['modules']:
            kwargs['msg'] = 'Unknown module %s' % kwargs['payload'][0]
            self.error(**kwargs)
            return kwargs
        kwargs['module'] = self.getModule(**kwargs)
        if self._hasEnvironment(**kwargs):
            kwargs['module'] = self.__setglobals(**kwargs)
        return kwargs
    # }}}

    def __setglobals(self, **kwargs):  # {{{
        """
        Assign all setglobals elements into the current module

        @param module: the current module
        @param environment: the EEnvironment object
        @return: the current module with the setglobals options
        """
        if kwargs['environment'].globaloptions:
            for k in kwargs['environment'].globaloptions.keys():
                if k in kwargs['module'].options:
                    kwargs['module'].options[k][0] = \
                            kwargs['environment'].globaloptions[k]
        return kwargs['module']
    # }}}
