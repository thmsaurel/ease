#!/usr/bin/python
###############################################################################
#
# File Name         : eecrun.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 12:57:33 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandRun(ECommand):
    """
    Launch the selected module, scenario
    Usage into cli interface : run
    """

    def execute(self, **kwargs):  # {{{
        """
        Run the selected Module

        @param module: the module to launch
        @return: the main dictionary
        """
        if not self._hasModule(**kwargs):
            return kwargs
        if self.ifOptions(**kwargs):
            try:
                kwargs['module'].run(**kwargs)
            except KeyError as e:
                kwargs['msg'] = '%s in %s' % (
                        e, kwargs['module'].__module__
                        )
                self.fail(**kwargs)
            except OSError as e:
                kwargs['msg'] = 'You must be root to use this module'
                self.fail(**kwargs)
            except Exception as e:
                kwargs['msg'] = '%s in %s' % (
                        e, kwargs['module'].__module__
                        )
                self.fail(**kwargs)
        return kwargs
    # }}}

    def ifOptions(self, **kwargs):  # {{{
        """
        Verify if all mandatory options are set

        @param module: the module to launch
        @return: True if all mandatory options are set, else False
        """
        if not kwargs['module'].options:
            kwargs['msg'] = 'you must add a options dictionary in your' + \
                    ' dictionary. See Docs for more information.'
            self.error(**kwargs)
            return False
        result = True
        for o in kwargs['module'].options.keys():
            if kwargs['module'].options[o][1] and \
                    not kwargs['module'].options[o][0]:
                kwargs['msg'] = 'you must set the %s option' % o
                self.warning(**kwargs)
                result = False
        return result
    # }}}
