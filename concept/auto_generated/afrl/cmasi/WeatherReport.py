#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import AbstractZone


class WeatherReport(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 55
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Area = None   #AbstractZone
        self.WindSpeed = 0   #real32
        self.WindDirection = 0   #real32
        self.Visibility = 0   #real32
        self.CloudCeiling = 0   #real32
        self.CloudCoverage = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack("B", self.Area != None ))
        if self.Area != None:
            buffer.append(struct.pack(">q", self.Area.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.Area.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.Area.SERIES_VERSION))
            buffer.append(self.Area.pack())
        buffer.append(struct.pack(">f", self.WindSpeed))
        buffer.append(struct.pack(">f", self.WindDirection))
        buffer.append(struct.pack(">f", self.Visibility))
        buffer.append(struct.pack(">f", self.CloudCeiling))
        buffer.append(struct.pack(">f", self.CloudCoverage))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
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
            self.Area = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.Area.unpack(buffer, _pos)
        else:
            self.Area = None
        self.WindSpeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.WindDirection = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Visibility = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.CloudCeiling = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.CloudCoverage = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_Area(self):
        return self.Area

    def set_Area(self, value):
        self.Area = value 

    def get_WindSpeed(self):
        return self.WindSpeed

    def set_WindSpeed(self, value):
        self.WindSpeed = float( value )

    def get_WindDirection(self):
        return self.WindDirection

    def set_WindDirection(self, value):
        self.WindDirection = float( value )

    def get_Visibility(self):
        return self.Visibility

    def set_Visibility(self, value):
        self.Visibility = float( value )

    def get_CloudCeiling(self):
        return self.CloudCeiling

    def set_CloudCeiling(self, value):
        self.CloudCeiling = float( value )

    def get_CloudCoverage(self):
        return self.CloudCoverage

    def set_CloudCoverage(self, value):
        self.CloudCoverage = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From WeatherReport:\n"
        buf +=    "Area = " + str( self.Area ) + "\n" 
        buf +=    "WindSpeed = " + str( self.WindSpeed ) + "\n" 
        buf +=    "WindDirection = " + str( self.WindDirection ) + "\n" 
        buf +=    "Visibility = " + str( self.Visibility ) + "\n" 
        buf +=    "CloudCeiling = " + str( self.CloudCeiling ) + "\n" 
        buf +=    "CloudCoverage = " + str( self.CloudCoverage ) + "\n" 

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
        str = ws + "<WeatherReport>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</WeatherReport>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<Area>\n"
        if self.Area == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.Area.toXMLStr(ws + "    ") 
        buf += ws + "</Area>\n"
        buf += ws + "<WindSpeed>" + str(self.WindSpeed) + "</WindSpeed>\n"
        buf += ws + "<WindDirection>" + str(self.WindDirection) + "</WindDirection>\n"
        buf += ws + "<Visibility>" + str(self.Visibility) + "</Visibility>\n"
        buf += ws + "<CloudCeiling>" + str(self.CloudCeiling) + "</CloudCeiling>\n"
        buf += ws + "<CloudCoverage>" + str(self.CloudCoverage) + "</CloudCoverage>\n"

        return buf
        
