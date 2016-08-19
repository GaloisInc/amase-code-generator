#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import AbstractZone


class KeepInZone(AbstractZone.AbstractZone):

    def __init__(self):
        AbstractZone.AbstractZone.__init__(self)
        self.LMCP_TYPE = 29
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(AbstractZone.AbstractZone.pack(self))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = AbstractZone.AbstractZone.unpack(self, buffer, _pos)
        return _pos




    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = AbstractZone.AbstractZone.toString(self)
        buf += "From KeepInZone:\n"

        return buf;

    def getLMCPType(self):
        return self.LMCP_TYPE

    def getSeriesName(self):
        return self.SERIES_NAME

    def getSeriesNameID(self):
        return self.SERIES_NAME_ID

    def getSeriesVersion(self):
        return self.SERIES_VERSION

    def toXMLStr(self, ws):
        str = ws + "<KeepInZone>\n";
        #str +=AbstractZone.AbstractZone.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</KeepInZone>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += AbstractZone.AbstractZone.toXMLMembersStr(self, ws)

        return buf
        
