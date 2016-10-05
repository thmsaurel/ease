#!/usr/bin/python
###############################################################################
#
# File Name         : test.py
# Created By        : Thomas Aurel
# Creation Date     : June 13th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:19:19 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import os
import random
import subprocess
import time

from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send, sr1

from models.emodule import EModule


class EModuleTest(EModule):
    options = {
            'HOST': ['', True, 'The target address'],
            'PORT': ['', True, 'The target port'],
            'THREADS': [1, False, 'Number of parallel threads running'],
            'SRCPORT': [None, False, 'The source port'],
            'SRCIP': [None, False, 'The source ip'],
            'PAYLOAD': ['', True, 'The malicious payload used by the attack']
            }

    def __init__(self, **kwargs):  # {{{
        EModule.__init__(self, **kwargs)
    # }}}

# #############################################################################
#   Main EModule Methods
# #############################################################################

    def run(self, **kwargs):  # {{{
        """
        Use to launch all attacks instances and all option verifications
        """
        t = time.time()
        self.filteriptables(**kwargs)
        EModule.run(self, **kwargs)
        self.unfilteriptables(**kwargs)
        kwargs['msg'] = 'Test realised in %s seconds' % str(time.time() - t)
    # }}}

    def do(self, **kwargs):  # {{{
        """
        An instance attack

        @return: the main dictionary
        """
        kwargs = EModule.do(self, **kwargs)
        kwargs['seq'] = random.randint(1000000, 16000000)
        kwargs['id'] = random.randint(1024, 65635)

        # begin play function
        kwargs['ack'] = self.sendSYN(**kwargs)
        if kwargs['ack'] == 0:
            kwargs['msg'] = 'failed to connect with %s' % kwargs['host']
            self.error(**kwargs)
            return kwargs
        kwargs['seq'] += 1
        kwargs['ack'] += 1
        kwargs['id'] += 1
        self.sendACK(**kwargs)
        kwargs['request'] = self.getRequest(**kwargs)
        send(kwargs['request'])
        return kwargs
    # }}}

# #############################################################################
#   Verify if the options dict has correct values
# #############################################################################

    def verify(self, **kwargs):  # {{{
        """
        Verify some element from module class

        @return: False if no error is raise, else True
        """
        error = EModule.verify(self, **kwargs)
        print os.environ
        if 'SUDO_UID' not in os.environ:  # {{{
            kwargs['msg'] = 'You don\'t have administrator permissions.'
            self.warning(**kwargs)
            kwargs['msg'] = 'It\'s possible you encounter some issues to ' + \
                'use some parts of this script'
            self.warning(**kwargs)
            kwargs['msg'] = "We recommand you to use EASE program with 'sudo'."
            self.warning(**kwargs)
        # }}}
        if 'PAYLOAD' in self.options:  # {{{
            try:
                str(self.options['PAYLOAD'][0])
            except:
                error = True
        # }}}
        return error
    # }}}

# #############################################################################
#   Auxiliary Usefull Methods for Module
# #############################################################################

# #############################################################################
#   Send SYN and ACK
# #############################################################################

    def sendSYN(self, **kwargs):  # {{{
        """
        send a SYN to the defined host

        @retun: the ack sequence if there is a response, else 0
        """
        self.info(msg='Send SYN to %s' % kwargs['host'], **kwargs)
        rq = self.ipRequest(**kwargs)/self.tcpRequest(flags="S", **kwargs)
        rp = sr1(rq, timeout=1, retry=-2)
        if not rp:
            return 0
        return rp[TCP].seq
    # }}}

    def sendACK(self, **kwargs):  # {{{
        """
        send a ACK to the defined host
        """
        self.info(msg='Send ACK to %s' % kwargs['host'], **kwargs)
        rq = self.ipRequest(**kwargs)/self.tcpRequest(flags="A", **kwargs)
        send(str(rq), verbose=0)
    # }}}

# #############################################################################
#   IP and TCP Requests
# #############################################################################

    def ipRequest(self, **kwargs):  # {{{
        """
        Get an IP base request

        @param host: the targeted host
        @param proto: the targeted protocol
        @param id: the id request
        @return: a IP base request
        @raise: a error if host is not defined
        """
        dictip = {}
        if not self._hasHost(**kwargs):
            raise
        i = random.randint(1024, 65635)
        dictip['dst'] = kwargs['host']
        dictip['proto'] = kwargs['proto'] if 'proto' in kwargs else 6
        dictip['id'] = kwargs['id'] if 'id' in kwargs else i
        if self.options['SRCIP'][0]:
            if self.isValidIp(
                    host=self.options['SRCIP'][0],
                    interface=kwargs['interface']
                    ):
                dictip['src'] = self.options['SRCIP'][0]
        return IP(**dictip)
    # }}}

    def tcpRequest(self, flags='PA', **kwargs):  # {{{
        """
        Get an IP base request

        @param dport: the destination port
        @param sport: the source port
        @param flags: the flags request (default PA)
        @param seq: the sequence (optional)
        @param ack: the ack number
        """
        dicttcp = {}
        if not self._hasPort(**kwargs):
            raise
        seq = random.randint(1000000, 16000000)
        dicttcp['dport'] = int(kwargs['port'])
        dicttcp['sport'] = random.randint(1024, 65535)
        dicttcp['seq'] = kwargs['seq'] if 'seq' in kwargs else seq
        if self.__isKeyDict(_l='flags', **kwargs):
            dicttcp['flags'] = kwargs['flags']
        if self.isKeyDict(_l=['ack'], **kwargs):
            dicttcp['ack'] = kwargs['ack']
        if self.options['SRCPORT'][0]:
            if self.isValidPort(
                    port=self.options['SRCPORT'][0],
                    interface=kwargs['interface']
                    ):
                dicttcp['sport'] = self.options['SRCPORT'][0]
        return TCP(**dicttcp)
    # }}}

    def getRequest(self, **kwargs):  # {{{
        """
        Get a complete request

        @return: a request
        """
        return self.ipRequest(**kwargs)/self.tcpRequest(
                **kwargs)/self.options['PAYLOAD'][0]
    # }}}

# #############################################################################
#   Request
# #############################################################################

    def filteriptables(self, **kwargs):  # {{{
        subprocess.call([
            'sudo',
            'iptables',
            '-A',
            'OUTPUT',
            '-p',
            'tcp',
            '--tcp-flags',
            'RST',
            'RST',
            '-d',
            self.options['HOST'][0],
            '-j',
            'DROP'
            ])
    # }}}

    def unfilteriptables(self, **kwargs):  # {{{
        subprocess.call('sudo iptables -F')
    # }}}

# #############################################################################
#   Misc
# #############################################################################

    def fuzzingtcp(self, **kwargs):
        pass
