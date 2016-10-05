#!/usr/bin/python
###############################################################################
#
# File Name         : eplugins.py
# Created By        : Thomas Aurel
# Creation Date     : June 27th, 2016
# Version           : 0.1
# Last Change       : June 27th, 2016 at 09:56:47 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################

from core.eobject import EObject


class EPlugin(EObject):
    """

    """

    def __init__(self, **kwargs):
        EObject.__init__(self, **kwargs)
