#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *


class OperatingRegion(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 39
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.ID = 0   #int64
        self.KeepInAreas = []   #int64
        self.KeepOutAreas = []   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">l", self.ID))
        buffer.append(struct.pack(">H", len(self.KeepInAreas) ))
        for x in self.KeepInAreas:
            buffer.append(struct.pack(">l", x ))
        buffer.append(struct.pack(">H", len(self.KeepOutAreas) ))
        for x in self.KeepOutAreas:
            buffer.append(struct.pack(">l", x ))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.ID = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.KeepInAreas = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.KeepInAreas = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.KeepOutAreas = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.KeepOutAreas = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        return _pos


    def get_ID(self):
        return self.ID

    def set_ID(self, value):
        self.ID = int( value )

    def get_KeepInAreas(self):
        return self.KeepInAreas

    def get_KeepOutAreas(self):
        return self.KeepOutAreas



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From OperatingRegion:\n"
        buf +=    "ID = " + str( self.ID ) + "\n" 
        buf +=    "KeepInAreas = " + str( self.KeepInAreas ) + "\n" 
        buf +=    "KeepOutAreas = " + str( self.KeepOutAreas ) + "\n" 

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
        str = ws + "<OperatingRegion>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</OperatingRegion>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<ID>" + str(self.ID) + "</ID>\n"
        buf += ws + "<KeepInAreas>\n"
        for x in self.KeepInAreas:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</KeepInAreas>\n"
        buf += ws + "<KeepOutAreas>\n"
        for x in self.KeepOutAreas:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</KeepOutAreas>\n"

        return buf
        
