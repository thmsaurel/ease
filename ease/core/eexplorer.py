#!/usr/bin/python
###############################################################################
#
# File Name         : explorer.py
# Created By        : Thomas Aurel
# Creation Date     : May 25th, 2016
# Version           : 0.1
# Last Change       : July 26th, 2016 at 03:06:05 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import os
import re

from core.eobject import EObject


class EExplorer(EObject):
    """
    The Explorer Class

    Use to every files and/or folders manipulations
    """

    @staticmethod
    def existFile(_s):  # {{{
        """
        Check if a file exists in an exiting directory.

        @param _s: file pathname
        @return: 'True' if file exists
        """
        return os.path.isfile(EExplorer.normalize(_s))
    # }}}

    @staticmethod
    def existFolder(_s):  # {{{
        """
        Check if a folder exists in an exiting directory.

        @param _s: folder pathname
        @return: 'True' if folder exists
        """
        return os.path.isdir(EExplorer.normalize(_s))
    # }}}

    @staticmethod
    def normalize(_s):  # {{{
        """
        Normalize a path

        @param _s: pathname
        @return: path normalized
        """
        return os.path.normpath(_s)
    # }}}

    @staticmethod
    def getPath(_p):  # {{{
        """
        Normalize path a given path and given an absolute path

        @param _p: path to normalize
        @return: absolute path
        """
        return os.path.abspath(EExplorer.normalize(_p))
    # }}}

    @staticmethod
    def getPythonFiles(_r):  # {{{
        """
        Get a list from all python files from a repository (without __init__)

        @param _r: the repository
        @return: a list with all python file
        """
        l = []
        for top, dirs, files in os.walk(_r):
            for f in files:
                if os.path.splitext(f)[1] == '.py' and not \
                        os.path.splitext(f)[0] == '__init__':
                    pythonfile = str(top + '/' + f).replace(_r, '')
                    if re.match("/.*", pythonfile):
                        pythonfile = pythonfile[1:]
                    l.append(pythonfile)
        return l
    # }}}

    @staticmethod
    def getPythonExecFiles(_r):  # {{{
        """
        Get a list from all executable python files from a repository

        @param _r: the repository
        @return: a list with all python file
        """
        l = []
        for top, dirs, files in os.walk(_r):
            for f in files:
                if os.path.splitext(f)[1] == '.pyc':
                    l.append(str(top + '/' + f).replace(_r, ''))
        return l
    # }}}

    @staticmethod
    def getALLPythonFiles(_r):  # {{{
        """
        Get all python files from a repository (source code and executable)

        @param _r: the repository
        @return: a list with all python file
        """
        return EExplorer.getPythonFiles(_r) + EExplorer.getPythonExecFiles(_r)
    # }}}

    @staticmethod
    def getRepository(_r):
        l = []
        for top, dirs, files in os.walk(_r):
            for d in dirs:
                l.append(d)
        return l
