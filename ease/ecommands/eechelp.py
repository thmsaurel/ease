#!/usr/bin/python
###############################################################################
#
# File Name         : eechelp.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : August  9th, 2016 at 10:27:55 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandHelp(ECommand):
    """
    Show an help message
    Usage into cli interface: help [COMMAND]
    """

    def execute(self, **kwargs):  # {{{
        """
        Show a global or specific help message

        @param payload: the argument list
        @param config: the EConfiguration file (optional)
        @return: the main dictionary
        """
        if self._hasPayload(**kwargs):
            if not kwargs['payload'][0]:
                kwargs['msg'] = 'Unknown command: can\'t show help message'
                self.error(**kwargs)
                return kwargs
        if self._hasConfig(**kwargs):
            kwargs['msg'] = 'This is the help for ease (version %s)' % (
                    kwargs['config'].get(key='version'))
            self.help(**kwargs)
        kwargs['interface'].helpmsg(**kwargs)
        return kwargs
    # }}}
