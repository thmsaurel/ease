#!/usr/bin/python
###############################################################################
#
# File Name         : emopcua.py
# Created By        : Thomas Aurel
# Creation Date     : June 30th, 2016
# Version           : 0.1
# Last Change       : July 21th, 2016 at 01:23:45 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
from calendar import timegm
from datetime import datetime, timedelta, tzinfo

from models.emodule import EModule
from protocols.opcua import opcuaResponseDecoder


class EModuleOpcua(EModule):
    def __init__(self, **kwargs):
        EModule.__init__(self, **kwargs)

# #############################################################################
#   Main EModule Methods
# #############################################################################

    def run(self, **kwargs):
        EModule.run(self, **kwargs)

    def do(self, **kwargs):
        kwargs = EModule.do(self, **kwargs)
        kwargs['socket'] = self.initsocket(**kwargs)
        if not self._hasSocket(**kwargs):
            self.error(msg="Can't create a socket", **kwargs)
            raise
        return kwargs

# #############################################################################
#   Verify if the options dict has correct values
# #############################################################################

    def verify(self, **kwargs):
        error = EModule.verify(self, **kwargs)
        return error

    def __hasField(self, **kwargs):
        if not self._hasRequest(**kwargs):
            return False
        if not self._isKeyDict(_l='field', **kwargs):
            return False
        l = []
        for f in kwargs['request'].fields_desc:
            l.append(f.name)
        return kwargs['field'] in l

    def getTimestamp(self, **kwargs):
        class UTC(tzinfo):
            def utcoffset(self, dt):
                return timedelta(9)

            def tzname(self, dt):
                return "UTC"

            def dst(self, dt):
                return timedelta(0)

        dt = datetime.now()
        if not dt.tzinfo or not dt.tzinfo.utcoffset(dt):
            dt = dt.replace(tzinfo=UTC())
            ft = 116444664000000000 + timegm(dt.timetuple()) * 10000000
            return ft + (dt.microsecond * 10)


# #############################################################################
#   Auxiliary Usefull Methods for Module
# #############################################################################

    # def opcuaRequest(self, **kwargs):
    #     pass
    def opcuaRequest(self, _r):
        _r.messageSize = len(_r)

    def sendmessagesocket(self, **kwargs):
        kwargs['request'].messageSize = len(kwargs['request'])
        if self.__hasField(field='timestamp', **kwargs):
            kwargs['request'].timestamp = self.getTimestamp(**kwargs)
        rp = EModule.sendmessagesocket(self, **kwargs)
        return opcuaResponseDecoder(rp)
