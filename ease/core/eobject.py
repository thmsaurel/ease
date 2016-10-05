#!/usr/bin/python
###############################################################################
#
# File Name         : eobject.py
# Created By        : Thomas Aurel
# Creation Date     : May 24th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 05:13:02 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################


class EObject(object):
    """
    The default object class of the program

    It contains function which are used by multiple class
    """

    def __init__(self, **kwargs):
        pass

# #############################################################################
#   Unify Objects Methods
# #############################################################################

    def getClassname(self, **kwargs):  # {{{
        """
        The default getClassname function use to returned the name of the
        EObject class name
        If this method is called, the eobject subclass doesn't have a override
        of this function

        @return: None
        """
        kwargs['msg'] = 'implement getClassname function for %s' % (
                self.__class__.__name__
                )
        self.error(**kwargs)
        return None
    # }}}

# #############################################################################
#   Print messages (using a EInterface class)
# #############################################################################

    def error(self, **kwargs):  # {{{
        """
        Default function to show an error message
        Call the printMsg function to process to all verification

        @param msg: the message to show
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='error', **kwargs)
    # }}}

    def debug(self, **kwargs):
        """
        Default function to show a default message
        Call the printMsg function to process to all verification

        @param msg: the message to show
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='debug', **kwargs)

    def info(self, **kwargs):  # {{{
        """
        Default function to show an info message
        Call the printMsg function to process to all verification

        @param msg: the message to show
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='info', **kwargs)
    # }}}

    def warning(self, **kwargs):  # {{{
        """
        Default function to show a warning message
        Call the printMsg function to process to all verification

        @param msg: the message to show
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='warning', **kwargs)
    # }}}

    def success(self, **kwargs):  # {{{
        """
        Default function to show a success message
        Call the printMsg function to process to all verification

        @param msg: the message to show
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='success', **kwargs)
    # }}}

    def fail(self, **kwargs):  # {{{
        """
        Default function to show a fail message
        Call the printMsg function to process to all verification

        @param msg: the message to show
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='fail', **kwargs)
    # }}}

    def help(self, **kwargs):  # {{{
        """
        Default function to show a help message
        Call the printMsg function to process to all verification

        @param msg: the message to show
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='help', **kwargs)
    # }}}

    def table(self, **kwargs):  # {{{
        """
        Default function to show an table message
        Call the printMsg function to process to all verification

        @param msg: a dictionary compose of two list:
                * h: the table header
                * t: the table element store inside a list
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='table', **kwargs)
    # }}}

    def hexdump(self, **kwargs):  # {{{
        """
        Default function to show a hexdump message
        Call the printMsg function to process to all verification

        @param request: the request to show
        @param response: the response to show (optional)
        @param interface: EInterface object, where to print the given message
        """
        self.printMsg(type='hexdump', **kwargs)
    # }}}

# #############################################################################
#   Print messages main method
# #############################################################################

    def printMsg(self, **kwargs):  # {{{
        """
        The default message printer
        Verify if all necessary elements are present inside the dictionary

        @param type: string, the message type you want to use
        @param interface: EInterface where to show the message
        @param msg: the message to show (except for 'hexdump')
        @param request: the message to show for a hexdump type
        """
        if not self._hasInterface(**kwargs):
            print self.__class__.__name__
            print '[-] ERROR:    you have to create a EInterface instance' + \
                ' first.'
            return
        if not self._isKeyDict(_l=['type'], **kwargs):
            kwargs['interface'].error(msg="the message type is undefined")
            return
        k = 'msg' if kwargs['type'] not in ['hexdump'] else 'request'
        if not self._isKeyDict(_l=['type', k], **kwargs):
            kwargs['interface'].error(msg="the message to show is undefined")
            return
        if kwargs['type'] in ['debug']:
            kwargs['interface'].debug(**kwargs)
            return
        if kwargs['type'] in ['error']:
            kwargs['interface'].error(**kwargs)
            return
        if kwargs['type'] in ['fail']:
            kwargs['interface'].fail(**kwargs)
            return
        if kwargs['type'] in ['help']:
            kwargs['interface'].help(**kwargs)
            return
        if kwargs['type'] in ['info']:
            kwargs['interface'].info(**kwargs)
            return
        if kwargs['type'] in ['success']:
            kwargs['interface'].success(**kwargs)
            return
        if kwargs['type'] in ['warning']:
            kwargs['interface'].warning(**kwargs)
            return
        if kwargs['type'] in ['hexdump']:
            kwargs['interface'].hexdump(**kwargs)
            return
        if kwargs['type'] in ['table']:
            if not isinstance(kwargs['msg'], dict):
                kwargs['msg'] = 'the table message is not a dictionary'
                kwargs['interface'].error(**kwargs)
                return
            kwargs['interface'].table(**kwargs['msg'])
            return
        kwargs['interface'].error(msg='Unknown message type')
    # }}}

# #############################################################################
#   Verify if the kwargs has the current value and do some additional
#   verifications (like unitary test)
# #############################################################################

    def _hasConfig(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'config' key, if this 'config'
        key has a EObject instance for value and if this EObject instance is a
        EConfiguration instance

        @param kwargs: dictionary which contains all elements
        @return: True if a 'config' key is a EConfiguration object, else False
        """
        if not self._isKeyDict(_l='config', **kwargs):
            return False
        if not self._isEObject(_o=kwargs['config']):
            return False
        return self._isClass(_o=kwargs['config'], _cn='EConfiguration')
    # }}}

    def _hasEnvironment(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'environment' key, if this
        'environment' key has a EObject instance for value and if this EObject
        instance is a EEnvironment instance

        @param kwargs: dictionary which contains all elements
        @return: True if a 'environment' key is a EInterface object, else False
        """
        if not self._isKeyDict(_l='environment', **kwargs):
            return False
        if not self._isEObject(_o=kwargs['environment']):
            return False
        return self._isClass(_o=kwargs['environment'], _cn='EEnvironment')
    # }}}

    def _hasInterface(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'interface' key, if this
        'interface' key has a EObject instance for value and if this EObject
        instance is a EInterface instance

        @param kwargs: dictionary which contains all elements
        @return: True if a 'interface' key is a EInterface object, else False
        """
        if not self._isKeyDict(_l='interface', **kwargs):
            return False
        if not self._isEObject(_o=kwargs['interface']):
            return False
        return self._isClass(_o=kwargs['interface'], _cn='EInterface')
    # }}}

    def _hasModule(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'module' key, if this 'module'
        key has a EObject instance for value and if this EObject instance is a
        EModule instance

        @param kwargs: dictionary which contains all elements
        @return: True if a 'module' key is a EModule objet, else False
        """
        if not self._isKeyDict(_l='module', **kwargs):
            return False
        if not self._isEObject(_o=kwargs['module']):
            return False
        return self._isClass(_o=kwargs['module'], _cn='EModule')
    # }}}

    def _hasModules(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'modules' key and if this
        'modules' key has a list value.

        @param kwargs: dictionary which contains all elements
        @return. True if a 'modules' key is a list object, else False
        """
        if not self._isKeyDict(_l='modules', **kwargs):
            return False
        return isinstance(kwargs['modules'], list)
    # }}}

    def _hasPayload(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'payload' keyand if this 'payload'
        key is a list object

        @param kwargs: the dictionary wich contains all elements
        @return: True if a 'payload' key is a list, else False
        """
        if not self._isKeyDict(_l='payload', **kwargs):
            return False
        return isinstance(kwargs['payload'], list)
    # }}}

# #############################################################################
#   Verification Methods
# #############################################################################

    def _isClass(self, **kwargs):  # {{{
        """
        Verify if the given object is a instance of the given class name

        @param _o: the given object
        @param _cn: the given class name
        @return: True if _o class name is the given class name, else False
        """
        if not self._isKeyDict(_l=['_cn', '_o'], **kwargs):
            kwargs['msg'] = "you must define the '_o' and '_cn' keys, stupid!"
            self.error(**kwargs)
            return False
        return kwargs['_o'].getClassname() == kwargs['_cn']
    # }}}

    def _isEObject(self, **kwargs):  # {{{
        """
        Verify if the key value is a EObject instance

        @param _o: the object to test
        @return: True if the given object if a EObject instance, else False
        """
        if not self._isKeyDict(_l='_o', **kwargs):
            kwargs['msg'] = "you must define the '_o' key, stupid!"
            self.error(**kwargs)
            return False
        return isinstance(kwargs['_o'], EObject)
    # }}}

    def _isKeyDict(self, **kwargs):  # {{{
        """
        Verify if the given entry is a key of the given dictionary. In case of
        the given entry is a list, it will check if all list element are keys
        of the dictionary.

        @param _l: the potential key(s)
        @param _d: the given directory (default "kwargs")
        @return: return True if all element inside _l are _d's keys
        """
        if '_l' not in kwargs:
            kwargs['msg'] = "you must define the '_l' key, stupid!"
            self.error(**kwargs)
            return False
        if '_d' not in kwargs:
            kwargs['_d'] = kwargs
        if not isinstance(kwargs['_d'], dict):
            return False
        if not isinstance(kwargs['_l'], list):
            return kwargs['_l'] in kwargs['_d']
        for n in kwargs['_l']:
            if not self._isKeyDict(_l=n, _d=kwargs['_d']):
                break
        else:
            return True
        return False
    # }}}

# #############################################################################
#   Miscs Methods
# #############################################################################

    def _cleanList(self, **kwargs):  # {{{
        """
        Clean a list from all empty element from a config file list

        @param _lt: the list to clean
        @return: the clean list if success, else None
        """
        if not self._isKeyDict(_l=['_lt'], **kwargs):
            self.error(msg='define \'_lt\', stupid!')
            return None
        return ' '.join(kwargs['_lt']).split()
    # }}}
