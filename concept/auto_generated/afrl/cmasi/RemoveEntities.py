#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *


class RemoveEntities(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 53
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.EntityList = []   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">H", len(self.EntityList) ))
        for x in self.EntityList:
            buffer.append(struct.pack(">l", x ))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.EntityList = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.EntityList = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        return _pos


    def get_EntityList(self):
        return self.EntityList



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From RemoveEntities:\n"
        buf +=    "EntityList = " + str( self.EntityList ) + "\n" 

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
        str = ws + "<RemoveEntities>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</RemoveEntities>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<EntityList>\n"
        for x in self.EntityList:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</EntityList>\n"

        return buf
        
