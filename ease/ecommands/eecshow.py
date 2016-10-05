#!/usr/bin/python
###############################################################################
#
# File Name         : eecshow.py
# Created By        : Thomas Aurel
# Creation Date     : July 20th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 02:14:39 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from models.ecommand import ECommand


class ECommandShow(ECommand):
    """
    Show all information about the tool or the current module
    Usage into cli interface : show OPTION

    Possible OPTION value:
    + info:         Show all information available for a module
    + options:      Show all options available for a module
    + module:       Show all modules and scenarios available
    """
    # + environment:  Show environment settings

    def execute(self, **kwargs):  # {{{
        """
        Show all information regarding the payload value

        @param payload: the option to show
        @return: the main dictionary
        """
        if not self._hasPayload(**kwargs):
            self.error(msg='you must select an option first', **kwargs)
            return kwargs
        if kwargs['payload'][0] not in [
                'module', 'modules',
                'info', 'infos',
                'option', 'options'
                ]:
            kwargs['msg'] = 'the option "%s" doesn\'t exist for SHOW command' \
                    % kwargs['payload'][0]
            self.error(**kwargs)
            return kwargs
        t, h = self.getShowTable(**kwargs)
        if t and h:
            self.table(msg={'t': t, 'h': h}, **kwargs)
        return kwargs
    # }}}

    def getShowTable(self, **kwargs):  # {{{
        """
        Get the table to show

        @param payload: a string contains the information to show
        @param module: a Module object
        @return: t, h the content list and the header list
        """
        t = []
        h = []
        d = None
        if kwargs['payload'][0] in ['info', 'infos', 'option', 'options']:
            if not self._hasModule(**kwargs):
                kwargs['msg'] = 'you must select a module in first place'
                self.error(**kwargs)
                return None, None
            if kwargs['payload'][0] in ['option', 'options']:
                h = ['option', 'current', 'required', 'description']
                d = kwargs['module'].options
            else:
                h = ['info', 'description']
                d = kwargs['module'].infos
        if kwargs['payload'][0] in ['module', 'modules']:
            if not self._hasModules(**kwargs):
                return None, None
            h = ['Command', 'Name', 'Description']
            d = kwargs['modules']
        if not d:
            return None, None
        for k in d:
            l = []
            l.append(k)
            if kwargs['payload'][0] in ['info', 'infos', 'option', 'options']:
                l.append(d[k][0])
                if kwargs['payload'][0] in ['option', 'options']:
                    l.append(d[k][1])
                    l.append(d[k][2])
            if kwargs['payload'][0] in ['module', 'modules']:
                m = self.getModule(payload=[k], config=kwargs['config'])
                if self._isKeyDict(
                        _l=['Name', 'Description'],
                        _d=m.infos,
                        **kwargs):
                    l.append(m.infos['Name'])
                    l.append(m.infos['Description'])
            t.append(l)
        return t, h
    # }}}
