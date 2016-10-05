#!/usr/bin/python
###############################################################################
#
# File Name         : interface.py
# Created By        : Thomas Aurel
# Creation Date     : April  5th, 2016
# Version           : 0.1
# Last Change       : August  9th, 2016 at 10:28:51 AM
#
###############################################################################
import random
# Last Changed By   : Thomas Aurel
# Purpose           : Description
import re

from core.eobject import EObject


class EInterface(EObject):

    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[;33m'
    YELLOW2 = '\33[1;33m'
    BLUE = "\33[34m"
    CYAN = "\33[36m"
    ENDC = '\33[m'

    def __init__(self, **kwargs):
        EObject.__init__(self, **kwargs)
        self.getbanner(**kwargs)

    def getClassname(self, **kwargs):  # {{{
        """
        Use to verify if the value is module inside EObject

        @return: 'EInterface'
        """
        return 'EInterface'
    # }}}

# #############################################################################
#   Print Message Variables
# #############################################################################

    # Messages {{{{
    # Banner Message {{{
    skull = [
            "         .AMMMMMMMMMMA.          ",
            "       .AV. :::.:.:.::MA.        ",
            "      A' :..        : .:`A       ",
            "     A'..              . `A.     ",
            "    A' :.    :::::::::  : :`A    ",
            "    M  .    :::.:.:.:::  . .M    ",
            "    M  :   ::.:.....::.:   .M    ",
            "    V : :.::.:........:.:  :V    " + GREEN +
            ",adPPYba, ,adPPYYba, ,adPPYba,  ,adPPYba," + ENDC,
            "   A  A:    ..:...:...:.   A A   " + GREEN +
            "a8P_____88 \"\"     `Y8 I8[    \"\" a8P_____88" + ENDC,
            "  .V  MA:.....:M.::.::. .:AM.M   " + GREEN +
            "8PP\"\"\"\"\"\"\" ,adPPPPP88  `\"Y8ba,  8PP\"\"\"\"\"\"\"" + ENDC,
            " A'  .VMMMMMMMMM:.:AMMMMMMMV: A  " + GREEN +
            "\"8b,   ,aa 88,    ,88 aa    ]8I \"8b,   ,aa" + ENDC,
            ":M .  .`VMMMMMMV.:A `VMMMMV .:M: " + GREEN +
            "`\"Ybbd8\"' `\"8bbdP\"Y8 `\"YbbdP\"'  `\"Ybbd8\"'" + ENDC,
            " V.:.  ..`VMMMV.:AM..`VMV' .: V  ",
            "  V.  .:. .....:AMMA. . .:. .V   ",
            "   VMM...: ...:.MMMM.: .: MMV        version: ",
            "       `VM: . ..M.:M..:::M'          author:  ",
            "         `M::. .:.... .::M       ",
            "          M:.  :. .... ..M       ",
            "          V:  M:. M. :M .V       ",
            "          `V.:M.. M. :M.V'       ",
            ]
    penguin = [
            "  Ease",
            "  version: ",
            "  Author:  ",
            " _  __________________",
            "  \\/",
            " (o<",
            " //\\",
            " V_/_",
            ]
    # }}}
    # Acheviement Message {{{
    unicorn = [  # {{{
                "     \                        ",
                "      \                       ",
                "       \\                     ",
                "        \\                    ",
                "         >\/7                 ",
                "     _.-(6'  \                ",
                "    (=___._/` \               ",
                "         )  \ |               ",
                "        /   / |               ",
                "       /    > /               " + ',adPPYba, 88       88  ' +
                ',adPPYba,  ,adPPYba,  ,adPPYba, ,adPPYba, ,adPPYba, ',
                "      j    < _\               " + 'I8[    "" 88       88 a' +
                '8"     "" a8"     "" a8P_____88 I8[    "" I8[    "" ',
                "  _.-' :      ``.             " + ' `"Y8ba,  88       88 8' +
                'b         8b         8PP"""""""  `"Y8ba,   `"Y8ba,  ',
                "  \ r=._\        `.           " + 'aa    ]8I "8a,   ,a88 "' +
                '8a,   ,aa "8a,   ,aa "8b,   ,aa aa    ]8I aa    ]8I ',
                " <`\\\\_  \         .`-.        " + '`"YbbdP"\'  `"YbbdP\'' +
                'Y8  `"Ybbd8"\'  `"Ybbd8"\'  `"Ybbd8"\' `"YbbdP"\' `"YbbdP"\'',
                "  \ r-7  `-. ._  ' .  `\      ",
                "   \`,      `-.`7  7)   )     ",
                "    \/         \|  \'  / `-._ ",
                "               ||    .'       ",
                "                \\\\  (         ",
                "                 >\  >        ",
                "             ,.-' >.'         ",
                "            <.'_.''           ",
                "              <'              ",
            ]  # }}}
    stext = [
                ',adPPYba, 88       88  ,adPPYba,  ,adPPYba,  ,adPPYba, ,adP' +
                'PYba, ,adPPYba, ',
                'I8[    "" 88       88 a8"     "" a8"     "" a8P_____88 I8[ ' +
                '   "" I8[    "" ',
                ' `"Y8ba,  88       88 8b         8b         8PP"""""""  `"Y' +
                '8ba,   `"Y8ba,  ',
                'aa    ]8I "8a,   ,a88 "8a,   ,aa "8a,   ,aa "8b,   ,aa aa  ' +
                '  ]8I aa    ]8I ',
                '`"YbbdP"\'  `"YbbdP\'Y8  `"Ybbd8"\'  `"Ybbd8"\'  `"Ybbd8"\'' +
                ' `"YbbdP"\' `"YbbdP"\'',
            ]
    # }}}}
    # Failure Message {{{
    ftext = [
        '   ad88            88 88                     88 ',
        '  d8"              "" 88                     88 ',
        '  88                  88                     88 ',
        'MM88MMM ,adPPYYba, 88 88  ,adPPYba,  ,adPPYb,88 ',
        '  88    ""     `Y8 88 88 a8P_____88 a8"    `Y88 ',
        '  88    ,adPPPPP88 88 88 8PP""""""" 8b       88 ',
        '  88    88,    ,88 88 88 "8b,   ,aa "8a,   ,d88 ',
        '  88    `"8bbdP"Y8 88 88  `"Ybbd8"\'  `"8bbdP"Y8 ',
            ]
    # }}}
    # }}}

# #############################################################################
#   Prompt and module function Function
# #############################################################################

    def getbanner(self, **kwargs):  # {{{
        """
        print a banner element

        @param config: a EConfiguration object
        """
        banners = {
                0: self.skull,
                1: self.penguin,
                }
        for i in banners[random.randrange(0, len(banners))]:
            j = i
            if 'config' in kwargs:
                if re.search(r'(?i)author', i):
                    j += kwargs['config'].get(key='author')
                elif re.search(r'(?i)version', i):
                    j += kwargs['config'].get(key='version')
            print j
        # }}}

    def getprompt(self, **kwargs):  # {{{
        """
        Get the prompt for the input user

        @param module: a Module object (optional)
        @return: the user prompt
        """
        prompt = self.GREEN + 'ease' + self.ENDC
        if self._hasModule(**kwargs):
            prompt += ' > ' + self.BLUE + \
                    kwargs['module'].infos['Name'] + self.ENDC
        return prompt + ' > '
    # }}}

# #############################################################################
#   Print Simple Message Methods
# #############################################################################

    def debug(self, **kwargs):
        """
        the debug print message

        @param msg: the message to print
        """
        print self.YELLOW + '[#] DEBUG:    ' + self.ENDC + kwargs['msg']

    def error(self, **kwargs):  # {{{
        """
        the error print message

        @param msg: the message to print
        """
        print self.RED + '[-] ERROR:    ' + self.ENDC + kwargs['msg']
        # }}}

    def info(self, **kwargs):  # {{{
        """
        the info print message

        @param msg: the message to print
        """
        print self.BLUE + '[+] INFO:     ' + self.ENDC + kwargs['msg']
        # }}}

    def help(self, **kwargs):  # {{{
        """
        the help print message

        @param msg: the message to print
        """
        print self.CYAN + '[?] HELP:     ' + self.ENDC + kwargs['msg']
        # }}}

    def warning(self, **kwargs):  # {{{
        """
        the warning print message

        @param msg: the message to print
        """
        print self.YELLOW2 + '[!] WARNING:  ' + self.ENDC + kwargs['msg']
        # }}}

    def success(self, **kwargs):  # {{{
        """
        the success print message

        @param msg: the message to print
        """
        achievement = {
                0: self.unicorn,
                1: self.stext,
                }
        for i in achievement[random.randrange(0, len(achievement))]:
            print i
        print self.GREEN + '[+] SUCCESS:  ' + self.ENDC + kwargs['msg']
        # }}}

    def fail(self, **kwargs):  # {{{
        """
        the fail print message

        @param msg: the message to print
        """
        failure = {
                0: self.ftext,
                }
        for i in failure[random.randrange(0, len(failure))]:
            print i
        print self.RED + '[-] FAIL:     ' + self.ENDC + kwargs['msg']
        # }}}

# #############################################################################
#   Print Simple Message Methods
# #############################################################################

    def helpmsg(self, **kwargs):  # {{{
        """
        Show a help message

        @param payload: a ECommand name to print docs
        """
        if self._hasPayload(**kwargs):
            if kwargs['payload'][0]:
                for l in kwargs['payload'][0].__doc__.split('\n'):
                    self.help(msg=l.strip())
                return
        t = []
        for k in sorted(kwargs['_o'].commands):
            t.append([k, kwargs['_o'].commands[k]])
        self.table(t=t, h=['COMMAND', 'DESCRIPTION'], mode='help')
    # }}}

    def hexdump(self, lenght=16, **kwargs):  # {{{
        """
        Output the packet details with both their hexadecimal value and
        ASCII-printable character

        (hexdump function for "Black Hat Python book")
        taken from: http://code.activestate.com/recipes/142812-hex-dumper/

        @param request: the request message to print
        @param response: the response message to print
        @param lenght: the max element to print (default 16 (for hexa))
        """
        if not self._isKeyDict(_l=['request'], **kwargs):
            return
        l = 'request'
        if self._isKeyDict(_l='response', **kwargs):
            l = 'response'
        src = str(kwargs[l])
        if self._isKeyDict(_l='lenght', **kwargs):
            lenght = kwargs['lenght']
        result = []
        digits = 4 if isinstance(src, unicode) else 2
        self.info(msg=l.upper())
        for i in xrange(0, len(src), lenght):
            s = src[i:i+lenght]
            hexa = b' '.join(['%0*X' % (digits, ord(x)) for x in s])
            text = b' '.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
            result.append(b"%04X    %-*s    %s" % (
                i, lenght*(digits + 1), hexa, text))
        print b'\n'.join(result)
    # }}}

    def table(self, mode='info', **kwargs):  # {{{
        """
        Show a message table

        @param t: the list of list element
        @param h: the header list
        @param mode: the mode where to print the info
        """
        def lenmax(i, t, hi):  # {{{
            """
            Get the size of a maximum size for a element

            @param i: the element of a line
            @param t: the list element
            @param hi: the element of a header column
            @return: the max size command element
            """
            m = len(hi)
            for ti in t:
                m = m if m > len(str(ti[i])) else len(str(ti[i]))
            return m + 2
        # }}}

        def size(t):  # {{{
            """
            return the maximum size of the element list

            @param t: the list of list element
            @return: the maximum size of the list
            """
            l = 0
            for ti in t:
                l = l if len(ti) < l else len(ti)
            return l
        # }}}

        def printline(line, mode, header=None):  # {{{
            """
            print a line with the good header size

            @param line: the line to print
            @param mode: the mode which one print the info
            @param header: True if the line is a header one
            """
            if header:
                line = line + self.ENDC
                if mode == 'error':
                    line = self.RED + line
                elif mode == 'help':
                    line = self.CYAN + line
                else:
                    line = self.BLUE + line
            if mode not in ['info', 'error', 'help'] or mode == 'info':
                self.info(msg=line)
            elif mode == 'error':
                self.error(msg=line)
            else:
                self.help(msg=line)
        # }}}

        def printlines(t, l, FORMAT, mode):  # {{{
            """
            print all line element

            @param t: the list of list element
            @param l: the maximum size of lists
            @param FORMAT: the string which define the line format
            @param mode: the mode where to print the info
            """
            if l == 2:
                for ti in t:
                    printline(FORMAT % (ti[0], ti[1]), mode)
            elif l == 3:
                for ti in t:
                    printline(FORMAT % (ti[0], ti[1], ti[2]), mode)
            elif l == 4:
                for ti in t:
                    printline(FORMAT % (ti[0], ti[1], ti[2], ti[3]), mode)
            return
        # }}}

        if not self._isKeyDict(_l=['t', 'h'], **kwargs):
            kwargs['msg'] = 'table and/or header are missing in %s' % (
                    kwargs['_o'].__class__.__name__)
            self.error(**kwargs)
            return
        if self._isKeyDict(_l=['mode'], **kwargs):
            mode = kwargs['mode']
        if not isinstance(kwargs['h'], list):
            self.error(msg='header is not a list %s' % (
                        kwargs['_o'].__class__.__name__))
            return
        if not isinstance(kwargs['t'], list):
            self.error(msg='table is not a list %s' % (
                        kwargs['_o'].__class__.__name__))
            return
        h = self.upper(l=kwargs['h'], **kwargs)
        FORMAT = ""
        l = size(kwargs['t'])
        for i in range(0, l):
            FORMAT = FORMAT + "%-" + str(lenmax(i, kwargs['t'], h[i])) + "s "
        if len(h) == 2:
            f = FORMAT % (h[0], h[1])
        elif len(h) == 3:
            f = FORMAT % (h[0], h[1], h[2])
        elif len(h) == 4:
            f = FORMAT % (h[0], h[1], h[2], h[3])
        print
        printline(f, mode, True)
        printlines(kwargs['t'], l, FORMAT, mode)
    # }}}

    def upper(self, **kwargs):  # {{{
        """
        Remplace any string in a list into uppercase string

        @param l: the given string list
        @return: a uppercase string list
        """
        if not self._isKeyDict(_l=['l'], **kwargs):
            self.error(msg='no list in upper entry')
            return
        if not isinstance(kwargs['l'], list):
            self.error(msg='the l element is not a list')
        lst = []
        for i in kwargs['l']:
            lst.append(str(i.upper()))
        return lst
    # }}}
