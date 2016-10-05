#!/usr/bin/python
###############################################################################
#
# File Name         : eecenvironment.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : August  9th, 2016 at 10:20:46 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandEnvironment(ECommand):
    """
    Define environment value
    Usage into cli interface: env[ironment] [COMMAND [VALUE]]
    """

    def execute(self, **kwargs):  # {{{
        """
        Set or show elements from the EEnvironment object

        @param environment: the EEnvironment object
        @param payload: the list with the modification (optional)
        @return: the main directory with the modified values
        """
        if not self._hasEnvironment(**kwargs):
            kwargs['msg'] = 'you must set a EEnvironment object first'
            self.error(**kwargs)
            return kwargs
        if not self._hasPayload(**kwargs):
            kwargs['msg'] = 'This is Environment Variables'
            self.info(**kwargs)
            kwargs['msg'] = 'MODE: %s' % (
                    kwargs['environment'].getMode(**kwargs)
                    )
            self.info(**kwargs)
            if kwargs['environment'].globaloptions:
                t = []
                h = ['OPTION', 'VALUE']
                for k in kwargs['environment'].globaloptions:
                    t.append([k, kwargs['environment'].globaloptions[k]])
                kwargs['msg'] = {'t': t, 'h': h}
                self.table(**kwargs)
            return kwargs
        # modify element from EEnvironment
        return kwargs
    # }}}
