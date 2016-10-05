#!/usr/bin/python
###############################################################################
#
# File Name         : elmodule.py
# Created By        : Thomas Aurel
# Creation Date     : June 27th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 02:04:21 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import os

from path import Path

from core.eexplorer import EExplorer
from models.eloader import ELoader


# from ecommands.eecuse import ECommandUse


class ELoaderModule(ELoader):
    """

    """

    def __init__(self, **kwargs):
        ELoader.__init__(self, **kwargs)

    def crawler(self, **kwargs):  # {{{
        """
        Function use to return all default Module class

        @param config: EConfig object, the program configuration object
        @param _k: the key to use
        @return: a list of Module file if the config file exist, else []
        """
        if not self.verify(**kwargs):
            print 'don\'t verify'
            return []
        modules = []
        if not self._isKeyDict(_l=['_pm'], **kwargs):
            path = EExplorer.getPath(kwargs['config'].get(key=kwargs['_k']))
        else:
            path = kwargs['config'].get(
                    key=kwargs['_k'], section=kwargs['_pm'])
        for e in self.cleanConf(_p=path, **kwargs):
            p = Path(e).expandvars()
            if not self._isKeyDict(_l=['_pm'], **kwargs):
                self._getPluginFiles(_p=p, **kwargs)
            for f in EExplorer.getPythonFiles(p):
                modules.append(os.path.splitext(f)[0])
        return modules
    # }}}

    # def load(self, **kwargs):
    #     """

    #     """
    #     if not self._hasModules(**kwargs):
    #         return None
    #     for m in kwargs['modules']:
    #         e = ECommandUse()
    #         e.execute(
    #                 payload=[m],
    #                 **kwargs)

    def verify(self, **kwargs):  # {{{
        """
        Verify if all used variable are present in the main dictionary

        @return: True if everything is ok, else False
        """
        if not ELoader.verify(self, **kwargs):
            return False
        if not kwargs['config']._hasKey(key='modules_path', **kwargs):
            return False
        k = kwargs['config'].get(key='modules_path', **kwargs)
        return EExplorer.existFolder(k)
    # }}}
