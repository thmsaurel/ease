#!/usr/bin/python
###############################################################################
#
# File Name         : loader.py
# Created By        : Thomas Aurel
# Creation Date     : May 25th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 04:38:22 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import re
import shutil

from core.eexplorer import EExplorer
from core.eobject import EObject


class ELoader(EObject):
    """
    Loader Module Class

    Use to search (and load) the Module class element
    """
    def __init__(self, **kwargs):
        EObject.__init__(self, **kwargs)

    def verify(self, **kwargs):
        """
        Verify if all used variable are present in the main dictionary

        @return: True if everything is ok, else False
        """
        return self._hasConfig(**kwargs)

    def cleanConf(self, **kwargs):  # {{{
        """
        Get a clean version of a list of a configuration element

        @param _p: the configuration element
        @return: the clean list if success, else None
        """
        if not self._isKeyDict(_l='_p', **kwargs):
            return None
        return self._cleanList(
                _lt=re.split('\s*,\s*', kwargs['_p']),
                **kwargs
                )
    # }}}

    def _getPluginFiles(self, **kwargs):  # {{{
        """
        Create a copy of all plugin files into the dedicated repository

        @param _p: one element of plugins_path list
        """
        if not self._isKeyDict(_l=['_p', '_pm'], **kwargs):
            return
        ppath = kwargs['config'].get(key='plugins_path', **kwargs)
        for f in EExplorer.getPythonFiles(kwargs['_p']):
            shutil.copy(kwargs['_p'] + f, ppath + kwargs['_pm'] + '/')
    # }}}
