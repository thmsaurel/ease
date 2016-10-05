#!/usr/bin/python
###############################################################################
#
# File Name         : controller.py
# Created By        : Thomas Aurel
# Creation Date     : May 24th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 04:45:16 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
# import random

from path import Path

from core.econfiguration import EConfiguration
from core.eenvironment import EEnvironment
from core.eexplorer import EExplorer
from core.eobject import EObject
from ecommands.eecuse import ECommandUse
from eloaders.eelmodule import ELoaderModule
from eloaders.eelplugin import ELoaderPlugin
from eobjectfactories.eeofcommand import EOFCommand
from ihm.einterface import EInterface


class EController(EObject):
    """
    The Default Controller Class
    """

# #############################################################################
#   Init Function
# #############################################################################

    def __init__(self, **kwargs):  # {{{
        # EObject __init__
        EObject.__init__(self, **kwargs)

        # Configuration declaration
        self.config = EConfiguration(**kwargs)
        self.config = self.getConfiguration(**kwargs)
        kwargs['config'] = self.config

        # Interface declaration
        self.ihm = EInterface(**kwargs)
        kwargs['interface'] = self.ihm

        # get the default user configuration
        self.config = self.getConfiguration(**kwargs)

        # Define environment
        self.environment = EEnvironment(**kwargs)

        # Charge Modules and Load Scapy for the first time
        self.modules = self.getModules(**kwargs)
        self.info(msg='Load all plugins and check imports', **kwargs)

        # get the plugins
        self.modules += self.getPlugins(**kwargs)
        self.debug(msg="modules + plugins: " + str(self.modules), **kwargs)
        # }}}

# #############################################################################
#   Execute (Main Function)
# #############################################################################

    def execute(self, **kwargs):  # {{{
        """
        The EController main function

        @param kwargs: the main directory
        """
        dwargs = self.verify(**kwargs)
        if self.isECommand(**dwargs):
            dwargs = kwargs['_o'].execute(**dwargs)
            # try:
            #     kwargs = kwargs['_o'].execute(**kwargs)
            # except Exception as e:
            #     kwargs['msg'] = 'error while execute %s: %s' % (
            #             kwargs['_o'].__class__.__name__, e)
            #     self.error(**kwargs)
        dargs = self.selectCommand(**dwargs)
        self.execute(**dargs)
    # }}}

# #############################################################################
#   Additional Init Functions
# #############################################################################

    def getConfiguration(self, **kwargs):  # {{{
        """
        The fonction use to get the configuration class
        If no configuration are given, use the default file 'config.ini'.
        If an user configuration file exists, add the configuration variables
        into the object

        @return: the EConfiguration instance
        """
        config = self.config
        if self._isKeyDict(_l='config', **kwargs):
            k = config.get(key='config_file', **kwargs)
            p = Path(k)
            if not EExplorer.existFile(p.expandvars()):
                kwargs['msg'] = 'You can used an user configuration file ' + \
                    'at %s' % p.expandvars()
                self.warning(**kwargs)
                return config
            kwargs['fconf'] = p.expandvars()
        config.getConfigurationFile(**kwargs)
        return config
    # }}}

    def getModules(self, **kwargs):  # {{{
        """
        Get the modules (path given by the EConfiguration object)

        @param config: the EConfiguration object
        @return: A list with all the availables modules
        """
        mloader = ELoaderModule(**kwargs)
        modules = mloader.crawler(_k='modules_path', **kwargs)
        for m in modules:
            e = ECommandUse()
            e.execute(
                    payload=[m],
                    modules=modules,
                    **kwargs)
        return modules
    # }}}

# #############################################################################
#   Plugins
# #############################################################################

    def getPlugins(self, **kwargs):
        """
        """
        if not self._hasConfig(**kwargs):
            return None
        p = ELoaderPlugin(**kwargs)
        m = ELoaderModule(**kwargs)
        uep = kwargs['config'].get(
                key='user_emodules_path',
                section='emodules',
                **kwargs)
        upp = kwargs['config'].get(
                key='user_protocols_path',
                section='protocols',
                **kwargs)
        p.crawler(_pp=upp, _pm='protocols', **kwargs)
        p.crawler(_pp=uep, _pm='emodules', **kwargs)
        modules = []
        ump = kwargs['config'].get(
                key='user_modules_path',
                section='modules',
                **kwargs)
        if ump:
            modules = m.crawler(
                    _k='user_modules_path',
                    _pm='modules',
                    **kwargs)
            p.addPluginsModules(_pp=ump, _pm='modules', **kwargs)
        self.debug(msg="plugins: " + str(modules), **kwargs)
        return modules

# #############################################################################
#   Execute (Auxiliary Functions)
# #############################################################################

    def selectCommand(self, **kwargs):  # {{{
        """
        The input prompt and selector command function

        @param interface: the EInterface object
        @return: the main dictionary with a ECommand object
        """
        if not self._hasInterface(**kwargs):
            return kwargs
        try:
            i = raw_input(kwargs['interface'].getprompt(**kwargs))
            kwargs['_o'] = i.strip().replace('\xc2\xa0', ' ').split()
            if not isinstance(kwargs['_o'], list):
                kwargs['_o'] = []
        except KeyboardInterrupt:
            print
            kwargs['_o'] = []
        except EOFError:
            kwargs['_o'] = ['exit']
        of = EOFCommand()
        return of.getECommand(**kwargs)
    # }}}

    def isECommand(self, **kwargs):  # {{{
        """
        Verify if the _o element of the main dictionnary is a ECommand object

        @param kwargs: the main directory
        @return: True if the _o value is a ECommand object, else False
        """
        if not self._isKeyDict(_l='_o', **kwargs):
            return False
        if not self._isEObject(**kwargs):
            return False
        return self._isClass(_cn="ECommand", **kwargs)
    # }}}

    def verify(self, **kwargs):  # {{{
        """
        Verify is the main directory has a EInterface object, a EConfiguration
        object, a EEnvironment object and a list of modules

        @param kwargs: the main directory
        @return: the main directory with all needed elements
        """
        if not self._hasInterface(**kwargs):
            kwargs['interface'] = self.ihm
        if not self._hasConfig(**kwargs):
            kwargs['config'] = self.config
        if not self._hasModules(**kwargs):
            kwargs['modules'] = self.modules
        if not self._hasEnvironment(**kwargs):
            kwargs['environment'] = self.environment
        return kwargs
    # }}}
