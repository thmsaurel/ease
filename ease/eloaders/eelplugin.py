#!/usr/bin/python
###############################################################################
#
# File Name         : elplugin.py
# Created By        : Thomas Aurel
# Creation Date     : June 27th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 02:54:01 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################

import os
import shutil

from path import Path

from core.eexplorer import EExplorer
from models.eloader import ELoader


# import site
# import sys
# from importlib import import_module


class ELoaderPlugin(ELoader):
    """

    """

    def __init__(self, **kwargs):
        ELoader.__init__(self, **kwargs)

    def crawler(self, **kwargs):  # {{{
        """
        Function use to return all plugins class

        @param config: EConfig object, the program configuration object
        @return: a list of Module file if the config file exist, else []
        """
        # TODO: add a warning for each unexisting folders (if verify is ok)
        if not self.verify(**kwargs):
            return []
        ppath = kwargs['config'].get(key='plugins_path', **kwargs)[:-1]
        if not ppath:
            return []
        g = ppath + '.' + kwargs['_pm']
        try:
            __import__(g)
            for e in self.cleanConf(_p=kwargs['_pp'], **kwargs):
                p = Path(e).expandvars()
                if not EExplorer.existFolder(p):
                    kwargs['msg'] = 'This repostory "%s" does\'t exist' % p
                    self.warning(**kwargs)
                else:
                    self._getPluginFiles(_p=p, **kwargs)
                    self.__addPlugin(_p=p, _g=g, **kwargs)
        except Exception as e:
            kwargs['msg'] = 'Problem while compiling and loading plugin ' + \
                    'folder : %s ' % g
            self.error(**kwargs)
            kwargs['msg'] = 'Try to put \'__init__.py\' file into each ' + \
                ' repository'
            self.error(**kwargs)
            kwargs['msg'] = 'Error : %s' % e
            self.error(**kwargs)
            # print e
        # }}}

    def verify(self, **kwargs):  # {{{
        """
        Verify if all used variable are present in the main dictionary

        @return: True if everything is ok, else False
        """
        if not ELoader.verify(self, **kwargs):
            return False
        if not self._isKeyDict(_l=['_pp', '_pm'], **kwargs):
            return False
        if not kwargs['_pp'] or not kwargs['_pm']:
            return False
        cc = self.cleanConf(_p=kwargs['_pp'], **kwargs)
        if not cc:
            return False
        l = []
        for e in cc:
            p = Path(e)
            if not EExplorer.existFolder(p.expandvars()):
                l.append(p)
        if len(l) == len(cc):
            return False
        # remove all files from the plugin emplacment
        return self.cleanPluginElements(**kwargs)
    # }}}

    def cleanPluginElements(self, **kwargs):
        ppath = kwargs['config'].get(key='plugins_path', **kwargs)
        for f in EExplorer.getALLPythonFiles(ppath + kwargs['_pm']):
            os.remove(ppath + kwargs['_pm'] + '/' + f)
        for r in EExplorer.getRepository(ppath + kwargs['_pm']):
            os.removedirs(ppath + kwargs['_pm'] + '/' + r)
        return True

    def addPluginsModules(self, **kwargs):
        """

        """
        if not self.verify(**kwargs):
            return
        ppath = kwargs['config'].get(key='plugins_path', **kwargs)
        if not ppath:
            return
        for e in self.cleanConf(_p=kwargs['_pp'], **kwargs):
            p = Path(e).expandvars()
            if EExplorer.existFolder(p):
                for r in EExplorer.getRepository(p):
                    shutil.copytree(p + r, ppath + kwargs['_pm'] + '/' + r)

    def __addPlugin(self, **kwargs):  # {{{
        """
        Add a plugin inside the modules import

        @param _p: one element of plugins_path list
        @param _g: the group name where to import the new module
        """
        if not self._isKeyDict(_l=['_p', '_g'], **kwargs):
            return
        for f in EExplorer.getPythonFiles(kwargs['_p']):
            try:
                __import__(kwargs['_g'] + '.' + os.path.splitext(f)[0])
                # m = __import__(kwargs['_g'] + '.' + os.path.splitext(f)[0])
                # try:
                #     # for k in m.__dict__:
                #     #     print k, m.__dict__[k]
                # except Exception as e:
                #     print e
            except Exception as e:
                kwargs['msg'] = 'Problem compiling and loading plugin: %s' % f
                self.warning(**kwargs)
                kwargs['msg'] = 'Please DEBUG the plugin to fix the problem'
                self.warning(**kwargs)
                kwargs['msg'] = 'Error : %s' % e
                self.warning(**kwargs)
                os.remove(str(kwargs['_g'] + '.').replace('.', '/') + f)
    # }}}
