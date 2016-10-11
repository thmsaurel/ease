#!/usr/bin/python
###############################################################################
#
# File Name         : module.py
# Created By        : Thomas Aurel
# Creation Date     : May 25th, 2016
# Version           : 0.1
# Last Change       : October 11th, 2016 at 05:12:02 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import socket
import struct
import threading

from core.eobject import EObject


class EModule(EObject):
    """
    The default EModule class
    """
    options = {
            'HOST': ['', True, 'The target address'],
            'PORT': [0, False, 'The target port'],
            'THREADS': [1, False, 'Number of parallel threads running'],
            }

    THREADS = []

    def __init__(self, **kwargs):
        EObject.__init__(self, **kwargs)

# #############################################################################
#   Main EModule Methods
# #############################################################################

    def run(self, **kwargs):  # {{{
        """
        Use to verify if the options are expected value type and launch the do
        function command in threads (number of IP in host * number of threads).

        @return: the main directory
        """
        error = self.verify(**kwargs)
        if error:
            return kwargs
        for ip in self.ips(host=self.options['HOST'][0]):
            for i in range(int(self.options['THREADS'][0])):
                kwargs['host'] = ip
                thread = threading.Thread(
                        name='thread %d' % i,
                        target=self.do,
                        kwargs=kwargs)
                self.THREADS.append(thread)
                thread.start()
        for thread in self.THREADS:
            thread.join()
    # }}}

    def do(self, **kwargs):  # {{{
        """
        Launch the initial function for the Module action

        @param host: the IP targeted
        @param port: the port targeted
        @return: the main dictionary
        """
        if not self._hasHost(**kwargs):
            kwargs['msg'] = 'host is not configure'
            self.error(**kwargs)
            raise
        kwargs['port'] = self.options['PORT'][0]
        return kwargs
    # }}}

# #############################################################################
#   Auxiliary Usefull Methods for Module
# #############################################################################

    def initsocket(self, **kwargs):  # {{{
        """
        Create a socket with the host and port

        @param host: the IP targeted
        @param port: the port targeted
        @return: the wanted socket if it's possible, else None
        @raise: a error if the connection is refused
        """
        if not self._hasHost(**kwargs):
            kwargs['msg'] = 'you must define a valid host'
            self.error(**kwargs)
            return None
        if not self._hasPort(**kwargs):
            kwargs['msg'] = 'you must define a valid port'
            self.error(**kwargs)
            return None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((kwargs['host'], kwargs['port']))
        except:
            kwargs['msg'] = 'Connection refused to %s:%s' % (
                    kwargs['host'], kwargs['port'])
            self.error(**kwargs)
            raise
        return s
    # }}}

    def ips(self, host=options['HOST'][0], **kwargs):  # {{{
        """
        Get a list of all IP available from the HOST value

        @param host: a host value (IP/MASK) (default HOST option value)
        @return: a list of IP available from the host value
        """
        if len(host.split('/')) < 2:
            return [host]
        h = host.split('/')
        return self.mask2ip(ip=h[0], mask=h[1])
    # }}}

    def mask2ip(self, **kwargs):  # {{{
        """
        Get a list IP available from a network mask

        @return: an IP available list from a network mask if success, else None
        """
        if self._isKeyDict(_l=['ip', 'mask'], **kwargs):
            kwargs['msg'] = 'Error: ip and/or mask values are missing'
            self.error(**kwargs)
            return None
        ip_m = socket.inet_ntoa(struct.pack(">L", (1 << 32) - (
            1 << 32 >> int(kwargs['mask']))))
        ip_me = ip_m.split('.')
        ip_e = kwargs['ip'].split('.')
        ips = []
        for i0 in range(256 - int(ip_me[0])):
            e0 = str(i0 + (int(ip_e[0]) - (
                int(ip_e[0]) % (256 - int(ip_me[0]))))) + '.'
            for i1 in range(256 - int(ip_me[1])):
                e1 = e0 + str(i1 + (int(ip_e[1]) - (int(ip_e[1]) % (
                    256 - int(ip_me[1]))))) + '.'
                for i2 in range(256 - int(ip_me[2])):
                    e2 = e1 + str(i2 + (int(ip_e[2]) - (int(ip_e[2]) % (
                        256 - int(ip_me[2]))))) + '.'
                    for i3 in range(256 - int(ip_me[3])):
                        e3 = e2 + str(i3 + (int(ip_e[3]) - (
                            int(ip_e[3]) % (256 - int(ip_me[3])))))
                        ips.append(e3)
        return ips
    # }}}

    def sendmessagesocket(self, **kwargs):  # {{{
        """
        Send a request message through the given socket and get an answer

        @param socket: a socket object
        @param request: the message to sent
        @return: the answer message
        @raise: an error if socket or request are not defined
        """
        if not self._hasSocket(**kwargs):
            raise KeyError('Socket is defined or is not a socket object')
        if not self._hasRequest(**kwargs):
            raise KeyError('Request is defined or is not a socket object')
        kwargs['socket'].send(str(kwargs['request']))
        # self.hexdump(**kwargs)
        kwargs['response'] = kwargs['socket'].recv(65535)
        # self.hexdump(**kwargs)
        return kwargs['response']
    # }}}

# #############################################################################
#   Verification EModule Methods
# #############################################################################

    def _hasHost(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'host' key and if this 'host' key
        value is a valid IP address

        @param kwargs: dictionary which contains all elements
        @return: True if a 'host' key is a valid IP address, else None
        """
        if not self._isKeyDict(_l=['host'], **kwargs):
            return False
        return self._isValidIp(**kwargs)
    # }}}

    def _hasPort(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'port' key and if this 'port' key
        value is a valid port address

        @param kwargs: dictionary which contains all elements
        @return: True if a 'port' key is a valid port address, else None
        """
        if not self._isKeyDict(_l=['port'], **kwargs):
            return False
        return self._isValidPort(**kwargs)
    # }}}

    def _hasRequest(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'request' key

        @param kwargs: dictionary which contains all elements
        @return: True if the dictionary has a 'request' key, else False
        """
        return self._isKeyDict(_l=['request'], **kwargs)
    # }}}

    def _hasResponse(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'response' key

        @param kwargs: dictionary which contains all elements
        @return: True if the dictionary has a 'response' key, else False
        """
        return self._isKeyDict(_l=['response'], **kwargs)
    # }}}

    def _hasSocket(self, **kwargs):  # {{{
        """
        Verify if the given dictionary has a 'socket' key and if this 'socket'
        key value is a socket instance

        @param kwargs: dictionary which contains all elements
        @return: True if a 'socket' key is a socket instance, else None
        """
        if not self._isKeyDict(_l=['socket'], **kwargs):
            return False
        return isinstance(kwargs['socket'], socket.socket)
    # }}}

# #############################################################################
#   Verify if the options dict has correct values
# #############################################################################

    def verify(self, **kwargs):  # {{{
        """
        Verify some element from module class

        @return: False if no error is raise, else True
        """
        error = False
        if 'HOST' in self.options:  # {{{
            host = self.options['HOST'][0].split('/')
            if not self._hasHost(host=host[0], **kwargs):
                kwargs['msg'] = 'you must define a valid host'
                self.error(**kwargs)
                error = True
            if len(host) == 2:
                try:
                    mask = int(host.split('/')[1])
                except:
                    kwargs['msg'] = '"%s" is not a valid mask' % host[1]
                    self.error(**kwargs)
                    error = True
                if mask > 32 or mask < 0:
                    kwargs['msg'] = '"%s" is not a valid mask' % host[1]
                    self.error(**kwargs)
                    error = True
            elif len(host) > 2:
                kwargs['msg'] = '"%s" is not a valid HOST option' % (
                        '/'.join(host))
                self.error(**kwargs)
                error = True
        # }}}
        if 'PORT' in self.options:  # {{{
            # print self._hasPort(**kwargs)
            # print not self._hasPort(port=self.options['PORT'][0], **kwargs)
            if not self._hasPort(port=self.options['PORT'][0], **kwargs):
                kwargs['msg'] = 'you must define a valid port'
                self.error(**kwargs)
                error = True
            # }}}
        if 'THREADS' in self.options:  # {{{
            try:
                thread = int(self.options['THREADS'][0])
            except:
                kwargs['msg'] = '"%s" is an invalid number of threads' % (
                        self.options['THREADS'][0])
                self.error(**kwargs)
                error = True
            if thread < 0:
                kwargs['msg'] = '"%s" is an invalid number of threads' % (
                        self.options['THREADS'][0])
                self.error(**kwargs)
                error = True
        # }}}
        return error
    # }}}

    def _isValidIp(self, **kwargs):  # {{{
        """
        Verify if the given host is a valid IP address (IPv4 and IPv6)

        @param host: the host to verify
        @return: True if host value is a valid IP address, else False
        """
        return self._isValidIpv4(**kwargs) or self._isValidIpv6(**kwargs)
    # }}}

    def _isValidIpv4(self, **kwargs):  # {{{
        """
        Verify if the given host is an IPv4 address
        found at : http://stackoverflow.com/a/4017219

        @param host: the given address
        @return: True if host value is a valid IPv4 address, else False
        """
        try:
            socket.inet_pton(socket.AF_INET, kwargs['host'])
        except AttributeError:  # no inet_pton support (not unix system)
            try:
                socket.inet_aton(kwargs['host'])
            except socket.error:
                return False
            # avoid the usage of short address
            # e.g. '127.1' == '127.0.0.1' == '\x7f\x00\x00\x01'
            return kwargs['host'].count('.') == 3
        except socket.error:
            return False
        return True
    # }}}

    def _isValidIpv6(self, **kwargs):  # {{{
        """
        Verify if the given host is an IPv6 address
        found at : http://stackoverflow.com/a/4017219

        @param host: the given address
        @return: True if host value is a valid IPv6 address, else False
        """
        try:
            socket.inet_pton(socket.AF_INET6, kwargs['host'])
        except socket.error:
            return False
        return True
    # }}}

    def _isValidPort(self, **kwargs):  # {{{
        """
        Verify if the given port is a valid port

        @param port: the port to verify
        @return: True if port value is a valid port, else False
        """
        try:
            port = int(kwargs['port'])
        except:
            return False
        return port <= 65535 and port >= 0
    # }}}

# #############################################################################
#   Miscs
# #############################################################################

    def getClassname(self, **kwargs):  # {{{
        """
        Use to verify if the value is module inside EObject

        @return: 'EModule' (The main class name)
        """
        return 'EModule'
    # }}}
