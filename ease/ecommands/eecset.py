#!/usr/bin/python
###############################################################################
#
# File Name         : eecset.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:14:13 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandSet(ECommand):
    """
    Set an option value for a selected module
    Usage into cli interface : set OPTION VALUE
    """

    def execute(self, **kwargs):  # {{{
        """
        Set an option value of the selected module

        @param module: the module to modify
        @param payload: the list which contains the option and this value
        @return: the main dictionary with the modify module
        """
        if not self._hasModule(**kwargs):
            self.error(msg='you must select a module in first step', **kwargs)
            return kwargs
        if not self._hasPayload(**kwargs):
            self.error(msg='you must select an option first', **kwargs)
            return kwargs
        if not self._isKeyDict(
                _l=kwargs['payload'][0],
                _d=kwargs['module'].options,
                **kwargs
                ):
            kwargs['msg'] = \
                    'the option "%s" doesn\'t exist for this module' % \
                    kwargs['payload'][0]
            self.error(**kwargs)
            return kwargs
        if len(kwargs['payload']) <= 1:
            kwargs['msg'] = 'you must gave a value for the selected option'
            self.error(**kwargs)
            return kwargs
        kwargs['module'].options[kwargs['payload'][0]][0] = \
            ' '.join(kwargs['payload'][1:])
        return kwargs
    # }}}
