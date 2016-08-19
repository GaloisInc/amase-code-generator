#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadAction
from afrl.cmasi import Location3D


class GimbalStareAction(PayloadAction.PayloadAction):

    def __init__(self):
        PayloadAction.PayloadAction.__init__(self)
        self.LMCP_TYPE = 26
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Starepoint = Location3D.Location3D()   #Location3D
        self.Duration = 0   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(PayloadAction.PayloadAction.pack(self))
        buffer.append(struct.pack("B", self.Starepoint != None ))
        if self.Starepoint != None:
            buffer.append(struct.pack(">q", self.Starepoint.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.Starepoint.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.Starepoint.SERIES_VERSION))
            buffer.append(self.Starepoint.pack())
        buffer.append(struct.pack(">l", self.Duration))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = PayloadAction.PayloadAction.unpack(self, buffer, _pos)
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
            self.Starepoint = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.Starepoint.unpack(buffer, _pos)
        else:
            self.Starepoint = None
        self.Duration = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        return _pos


    def get_Starepoint(self):
        return self.Starepoint

    def set_Starepoint(self, value):
        self.Starepoint = value 

    def get_Duration(self):
        return self.Duration

    def set_Duration(self, value):
        self.Duration = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = PayloadAction.PayloadAction.toString(self)
        buf += "From GimbalStareAction:\n"
        buf +=    "Starepoint = " + str( self.Starepoint ) + "\n" 
        buf +=    "Duration = " + str( self.Duration ) + "\n" 

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
        str = ws + "<GimbalStareAction>\n";
        #str +=PayloadAction.PayloadAction.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</GimbalStareAction>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += PayloadAction.PayloadAction.toXMLMembersStr(self, ws)
        buf += ws + "<Starepoint>\n"
        if self.Starepoint == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.Starepoint.toXMLStr(ws + "    ") 
        buf += ws + "</Starepoint>\n"
        buf += ws + "<Duration>" + str(self.Duration) + "</Duration>\n"

        return buf
        
