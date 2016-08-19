#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import AbstractZone
from afrl.cmasi import ZoneAvoidanceType


class KeepOutZone(AbstractZone.AbstractZone):

    def __init__(self):
        AbstractZone.AbstractZone.__init__(self)
        self.LMCP_TYPE = 30
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.ZoneType = ZoneAvoidanceType.ZoneAvoidanceType.Physical   #ZoneAvoidanceType


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(AbstractZone.AbstractZone.pack(self))
        buffer.append(struct.pack(">i", self.ZoneType))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = AbstractZone.AbstractZone.unpack(self, buffer, _pos)
        self.ZoneType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_ZoneType(self):
        return self.ZoneType

    def set_ZoneType(self, value):
        self.ZoneType = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = AbstractZone.AbstractZone.toString(self)
        buf += "From KeepOutZone:\n"
        buf +=    "ZoneType = " + str( self.ZoneType ) + "\n" 

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
        str = ws + "<KeepOutZone>\n";
        #str +=AbstractZone.AbstractZone.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</KeepOutZone>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += AbstractZone.AbstractZone.toXMLMembersStr(self, ws)
        buf += ws + "<ZoneType>" + ZoneAvoidanceType.get_ZoneAvoidanceType_int(self.ZoneType) + "</ZoneType>\n"

        return buf
        
