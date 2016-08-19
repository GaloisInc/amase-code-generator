#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *


class Wedge(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 16
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.AzimuthCenterline = 0   #real32
        self.VerticalCenterline = 0   #real32
        self.AzimuthExtent = 0   #real32
        self.VerticalExtent = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">f", self.AzimuthCenterline))
        buffer.append(struct.pack(">f", self.VerticalCenterline))
        buffer.append(struct.pack(">f", self.AzimuthExtent))
        buffer.append(struct.pack(">f", self.VerticalExtent))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.AzimuthCenterline = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.VerticalCenterline = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.AzimuthExtent = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.VerticalExtent = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_AzimuthCenterline(self):
        return self.AzimuthCenterline

    def set_AzimuthCenterline(self, value):
        self.AzimuthCenterline = float( value )

    def get_VerticalCenterline(self):
        return self.VerticalCenterline

    def set_VerticalCenterline(self, value):
        self.VerticalCenterline = float( value )

    def get_AzimuthExtent(self):
        return self.AzimuthExtent

    def set_AzimuthExtent(self, value):
        self.AzimuthExtent = float( value )

    def get_VerticalExtent(self):
        return self.VerticalExtent

    def set_VerticalExtent(self, value):
        self.VerticalExtent = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From Wedge:\n"
        buf +=    "AzimuthCenterline = " + str( self.AzimuthCenterline ) + "\n" 
        buf +=    "VerticalCenterline = " + str( self.VerticalCenterline ) + "\n" 
        buf +=    "AzimuthExtent = " + str( self.AzimuthExtent ) + "\n" 
        buf +=    "VerticalExtent = " + str( self.VerticalExtent ) + "\n" 

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
        str = ws + "<Wedge>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</Wedge>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<AzimuthCenterline>" + str(self.AzimuthCenterline) + "</AzimuthCenterline>\n"
        buf += ws + "<VerticalCenterline>" + str(self.VerticalCenterline) + "</VerticalCenterline>\n"
        buf += ws + "<AzimuthExtent>" + str(self.AzimuthExtent) + "</AzimuthExtent>\n"
        buf += ws + "<VerticalExtent>" + str(self.VerticalExtent) + "</VerticalExtent>\n"

        return buf
        
