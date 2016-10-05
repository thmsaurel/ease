#!/usr/bin/python
###############################################################################
#
# File Name         : econfiguration.py
# Created By        : Thomas Aurel
# Creation Date     : May 25th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 11:22:36 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from configparser import SafeConfigParser

from core.eexplorer import EExplorer
from core.eobject import EObject


class EConfiguration(EObject):
    """
    The Default Configuration Object
    """

    def __init__(self, **kwargs):
        EObject.__init__(self, **kwargs)
        self.parser = SafeConfigParser()

    def getClassname(self, **kwargs):  # {{{
        """
        Use to verify if the value is an EObject

        @return: classname ('EConfiguration')
        """
        return self.__class__.__name__
    # }}}

    def getParser(self, **kwargs):  # {{{
        """
        Return the parser of the configuration object

        @return: the parser of the configuration object
        """
        return self.parser
    # }}}

# #############################################################################
#   Get Functions (Configuration file, Section & Key)
# #############################################################################

    def getConfigurationFile(self, **kwargs):  # {{{
        """
        Read the input config file

        @param fconf: the conf ini file to read (default 'config.ini')
        @return: the parser object if the file exists, else None
        """
        p = self.getParser()
        if not self._isKeyDict(_l='fconf', **kwargs):
            kwargs['fconf'] = 'config.ini'
        if not EExplorer.existFile(kwargs['fconf']):
            self.error(msg='the config file doesn\'t exist', **kwargs)
            return None
        p.read(kwargs['fconf'])
        return p
    # }}}

    def getSection(self, **kwargs):  # {{{
        """
        Return the entire Section

        @param section: the wanted section
        @return: a dict of the section if the section exists, else None
        """
        if not self._hasSection(**kwargs):
            print kwargs['section']
            self.error(msg='this section does\'t exists', **kwargs)
            return None
        d = {}
        p = self.getParser()
        for k, v in p.items(kwargs['section']):
            d[k] = v
        return d
    # }}}

    def get(self, **kwargs):  # {{{
        """
        Return the wanted key of the given section

        @param key: the value to looking for
        @param section: the section where is the value (default 'default')
        @return: the key value if the key exists, else None
        """
        p = self.getParser()
        if not self._isKeyDict(_l='section', **kwargs):
            kwargs['section'] = 'default'
        if not self._hasSection(**kwargs):
            self.error(msg='this section does\'t exists', **kwargs)
            return None
        if not self._hasKey(**kwargs):
            return None
        return p.get(kwargs['section'], kwargs['key'])
    # }}}

# #############################################################################
#   Verification functions
# #############################################################################

    def _hasSection(self, **kwargs):  # {{{
        """
        Verify if the given section exist inside the configuration file

        @param section: the section to looking for
        @return: True if the section exist, else False
        """
        p = self.getParser(**kwargs)
        if not self._isKeyDict(_l=['section'], **kwargs):
            return False
        return p.has_section(kwargs['section'])
    # }}}

    def _hasKey(self, **kwargs):  # {{{
        """
        Verify if the given section has the given key

        @param section: the section where looking for the key value (default
        'default')
        @param key: the key to looking for
        @return: True if the key exist, else False
        """
        p = self.getParser(**kwargs)
        if not self._isKeyDict(_l=['section'], **kwargs):
            kwargs['section'] = 'default'
        if not self._isKeyDict(_l=['key'], **kwargs):
            return False
        return p.has_option(kwargs['section'], kwargs['key'])
        # }}}
