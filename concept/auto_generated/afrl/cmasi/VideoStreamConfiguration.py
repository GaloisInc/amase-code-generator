#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadConfiguration


class VideoStreamConfiguration(PayloadConfiguration.PayloadConfiguration):

    def __init__(self):
        PayloadConfiguration.PayloadConfiguration.__init__(self)
        self.LMCP_TYPE = 49
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.AvailableSensorList = []   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(PayloadConfiguration.PayloadConfiguration.pack(self))
        buffer.append(struct.pack(">H", len(self.AvailableSensorList) ))
        for x in self.AvailableSensorList:
            buffer.append(struct.pack(">l", x ))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = PayloadConfiguration.PayloadConfiguration.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.AvailableSensorList = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.AvailableSensorList = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        return _pos


    def get_AvailableSensorList(self):
        return self.AvailableSensorList



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = PayloadConfiguration.PayloadConfiguration.toString(self)
        buf += "From VideoStreamConfiguration:\n"
        buf +=    "AvailableSensorList = " + str( self.AvailableSensorList ) + "\n" 

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
        str = ws + "<VideoStreamConfiguration>\n";
        #str +=PayloadConfiguration.PayloadConfiguration.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</VideoStreamConfiguration>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += PayloadConfiguration.PayloadConfiguration.toXMLMembersStr(self, ws)
        buf += ws + "<AvailableSensorList>\n"
        for x in self.AvailableSensorList:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</AvailableSensorList>\n"

        return buf
        
