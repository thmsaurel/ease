#!/usr/bin/python
###############################################################################
#
# File Name         : eecsetglobal.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 12:57:38 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandSetGlobal(ECommand):
    """
    Set an option value for all modules
    Usage into cli interface : setg[lobal] OPTION VALUE
    """

    def execute(self, **kwargs):  # {{{
        """
        Set a option for all modules (stored inside the EEnvironment object)

        @param payload: the list which contains the option and his value
        @param environment: the EEnvironment object
        @return: the main dictionary with the modify
        """
        if not self._hasEnvironment(**kwargs):
            kwargs['msg'] = 'you must set a EEnvironment object first'
            self.error(**kwargs)
            return kwargs
        if not self._hasPayload(**kwargs):
            self.error(msg='you must select an option first', **kwargs)
            return kwargs
        if len(kwargs['payload']) <= 1:
            kwargs['msg'] = 'you must gave a value for the selected option'
            self.error(**kwargs)
            return kwargs
        kwargs['environment'].addGlobal(**kwargs)
        if self._hasModule(**kwargs):
            if self._isKeyDict(
                    _l=kwargs['payload'][0], _d=kwargs['module'].options):
                kwargs['module'].options[kwargs['payload'][0]][0] = \
                        ' '.join(kwargs['payload'][1:])
        return kwargs
    # }}}
