#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import KeyValuePair


class PayloadConfiguration(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 5
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.PayloadID = 0   #int64
        self.PayloadKind = ""   #string
        self.Parameters = []   #KeyValuePair


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">l", self.PayloadID))
        buffer.append(struct.pack(">H", len(self.PayloadKind) ))
        if len(self.PayloadKind) > 0:
            buffer.append(struct.pack( `len(self.PayloadKind)` + "s", self.PayloadKind))
        buffer.append(struct.pack(">H", len(self.Parameters) ))
        for x in self.Parameters:
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
        self.PayloadID = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.PayloadKind = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.PayloadKind = ""
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.Parameters = [None] * _arraylen
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
                self.Parameters[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.Parameters[x].unpack(buffer, _pos)
            else:
                self.Parameters[x] = None
        return _pos


    def get_PayloadID(self):
        return self.PayloadID

    def set_PayloadID(self, value):
        self.PayloadID = int( value )

    def get_PayloadKind(self):
        return self.PayloadKind

    def set_PayloadKind(self, value):
        self.PayloadKind = str( value )

    def get_Parameters(self):
        return self.Parameters



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From PayloadConfiguration:\n"
        buf +=    "PayloadID = " + str( self.PayloadID ) + "\n" 
        buf +=    "PayloadKind = " + str( self.PayloadKind ) + "\n" 
        buf +=    "Parameters = " + str( self.Parameters ) + "\n" 

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
        str = ws + "<PayloadConfiguration>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</PayloadConfiguration>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<PayloadID>" + str(self.PayloadID) + "</PayloadID>\n"
        buf += ws + "<PayloadKind>" + str(self.PayloadKind) + "</PayloadKind>\n"
        buf += ws + "<Parameters>\n"
        for x in self.Parameters:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Parameters>\n"

        return buf
        
