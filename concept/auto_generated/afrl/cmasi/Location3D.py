#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import AltitudeType


class Location3D(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 3
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Latitude = 0   #real64
        self.Longitude = 0   #real64
        self.Altitude = 0   #real32
        self.AltitudeType = AltitudeType.AltitudeType.MSL   #AltitudeType


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">d", self.Latitude))
        buffer.append(struct.pack(">d", self.Longitude))
        buffer.append(struct.pack(">f", self.Altitude))
        buffer.append(struct.pack(">i", self.AltitudeType))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.Latitude = struct.unpack_from(">d", buffer, _pos)[0]
        _pos += 8
        self.Longitude = struct.unpack_from(">d", buffer, _pos)[0]
        _pos += 8
        self.Altitude = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.AltitudeType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_Latitude(self):
        return self.Latitude

    def set_Latitude(self, value):
        self.Latitude = float( value )

    def get_Longitude(self):
        return self.Longitude

    def set_Longitude(self, value):
        self.Longitude = float( value )

    def get_Altitude(self):
        return self.Altitude

    def set_Altitude(self, value):
        self.Altitude = float( value )

    def get_AltitudeType(self):
        return self.AltitudeType

    def set_AltitudeType(self, value):
        self.AltitudeType = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From Location3D:\n"
        buf +=    "Latitude = " + str( self.Latitude ) + "\n" 
        buf +=    "Longitude = " + str( self.Longitude ) + "\n" 
        buf +=    "Altitude = " + str( self.Altitude ) + "\n" 
        buf +=    "AltitudeType = " + str( self.AltitudeType ) + "\n" 

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
        str = ws + "<Location3D>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</Location3D>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<Latitude>" + str(self.Latitude) + "</Latitude>\n"
        buf += ws + "<Longitude>" + str(self.Longitude) + "</Longitude>\n"
        buf += ws + "<Altitude>" + str(self.Altitude) + "</Altitude>\n"
        buf += ws + "<AltitudeType>" + AltitudeType.get_AltitudeType_int(self.AltitudeType) + "</AltitudeType>\n"

        return buf
        
