#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *


class KeyValuePair(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 2
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Key = ""   #string
        self.Value = ""   #string


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">H", len(self.Key) ))
        if len(self.Key) > 0:
            buffer.append(struct.pack( `len(self.Key)` + "s", self.Key))
        buffer.append(struct.pack(">H", len(self.Value) ))
        if len(self.Value) > 0:
            buffer.append(struct.pack( `len(self.Value)` + "s", self.Value))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.Key = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.Key = ""
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.Value = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.Value = ""
        return _pos


    def get_Key(self):
        return self.Key

    def set_Key(self, value):
        self.Key = str( value )

    def get_Value(self):
        return self.Value

    def set_Value(self, value):
        self.Value = str( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From KeyValuePair:\n"
        buf +=    "Key = " + str( self.Key ) + "\n" 
        buf +=    "Value = " + str( self.Value ) + "\n" 

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
        str = ws + "<KeyValuePair>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</KeyValuePair>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<Key>" + str(self.Key) + "</Key>\n"
        buf += ws + "<Value>" + str(self.Value) + "</Value>\n"

        return buf
        
