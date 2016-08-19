#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadAction


class GimbalAngleAction(PayloadAction.PayloadAction):

    def __init__(self):
        PayloadAction.PayloadAction.__init__(self)
        self.LMCP_TYPE = 23
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Azimuth = 0   #real32
        self.Elevation = 0   #real32
        self.Rotation = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(PayloadAction.PayloadAction.pack(self))
        buffer.append(struct.pack(">f", self.Azimuth))
        buffer.append(struct.pack(">f", self.Elevation))
        buffer.append(struct.pack(">f", self.Rotation))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = PayloadAction.PayloadAction.unpack(self, buffer, _pos)
        self.Azimuth = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Elevation = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Rotation = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_Azimuth(self):
        return self.Azimuth

    def set_Azimuth(self, value):
        self.Azimuth = float( value )

    def get_Elevation(self):
        return self.Elevation

    def set_Elevation(self, value):
        self.Elevation = float( value )

    def get_Rotation(self):
        return self.Rotation

    def set_Rotation(self, value):
        self.Rotation = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = PayloadAction.PayloadAction.toString(self)
        buf += "From GimbalAngleAction:\n"
        buf +=    "Azimuth = " + str( self.Azimuth ) + "\n" 
        buf +=    "Elevation = " + str( self.Elevation ) + "\n" 
        buf +=    "Rotation = " + str( self.Rotation ) + "\n" 

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
        str = ws + "<GimbalAngleAction>\n";
        #str +=PayloadAction.PayloadAction.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</GimbalAngleAction>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += PayloadAction.PayloadAction.toXMLMembersStr(self, ws)
        buf += ws + "<Azimuth>" + str(self.Azimuth) + "</Azimuth>\n"
        buf += ws + "<Elevation>" + str(self.Elevation) + "</Elevation>\n"
        buf += ws + "<Rotation>" + str(self.Rotation) + "</Rotation>\n"

        return buf
        
