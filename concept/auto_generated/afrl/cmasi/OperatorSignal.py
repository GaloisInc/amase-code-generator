#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import KeyValuePair


class OperatorSignal(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 38
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Signals = []   #KeyValuePair


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">H", len(self.Signals) ))
        for x in self.Signals:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.Signals = [None] * _arraylen
        _pos += 2
        for x in range(_arraylen):
            _valid = struct.unpack_from("B", buffer, _pos )[0]
            _pos += 1
            if _valid:
                _series = struct.unpack_from(">q", buffer, _pos)[0]
                _pos += 8
                _type = struct.unpack_from(">I", buffer, _pos)[0]
                _pos += 4
                _version = struct.unpack_from(">H", buffer, _pos)[0]
                _pos += 2
                from lmcp import LMCPFactory
                self.Signals[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.Signals[x].unpack(buffer, _pos)
            else:
                self.Signals[x] = None
        return _pos


    def get_Signals(self):
        return self.Signals



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From OperatorSignal:\n"
        buf +=    "Signals = " + str( self.Signals ) + "\n" 

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
        str = ws + "<OperatorSignal>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</OperatorSignal>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<Signals>\n"
        for x in self.Signals:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Signals>\n"

        return buf
        
