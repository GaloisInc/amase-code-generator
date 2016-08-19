#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadConfiguration
from afrl.cmasi import GimbalPointingMode


class GimbalConfiguration(PayloadConfiguration.PayloadConfiguration):

    def __init__(self):
        PayloadConfiguration.PayloadConfiguration.__init__(self)
        self.LMCP_TYPE = 24
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.SupportedPointingModes = []   #GimbalPointingMode
        self.MinAzimuth = -180   #real32
        self.MaxAzimuth = 180   #real32
        self.IsAzimuthClamped = False   #bool
        self.MinElevation = -180   #real32
        self.MaxElevation = 180   #real32
        self.IsElevationClamped = False   #bool
        self.MinRotation = 0   #real32
        self.MaxRotation = 0   #real32
        self.IsRotationClamped = True   #bool
        self.MaxAzimuthSlewRate = 0   #real32
        self.MaxElevationSlewRate = 0   #real32
        self.MaxRotationRate = 0   #real32
        self.ContainedPayloadList = []   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(PayloadConfiguration.PayloadConfiguration.pack(self))
        buffer.append(struct.pack(">H", len(self.SupportedPointingModes) ))
        for x in self.SupportedPointingModes:
            buffer.append(struct.pack(">i", x ))
        buffer.append(struct.pack(">f", self.MinAzimuth))
        buffer.append(struct.pack(">f", self.MaxAzimuth))
        buffer.append(struct.pack(">B", self.IsAzimuthClamped))
        buffer.append(struct.pack(">f", self.MinElevation))
        buffer.append(struct.pack(">f", self.MaxElevation))
        buffer.append(struct.pack(">B", self.IsElevationClamped))
        buffer.append(struct.pack(">f", self.MinRotation))
        buffer.append(struct.pack(">f", self.MaxRotation))
        buffer.append(struct.pack(">B", self.IsRotationClamped))
        buffer.append(struct.pack(">f", self.MaxAzimuthSlewRate))
        buffer.append(struct.pack(">f", self.MaxElevationSlewRate))
        buffer.append(struct.pack(">f", self.MaxRotationRate))
        buffer.append(struct.pack(">H", len(self.ContainedPayloadList) ))
        for x in self.ContainedPayloadList:
            buffer.append(struct.pack(">l", x ))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = PayloadConfiguration.PayloadConfiguration.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.SupportedPointingModes = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.SupportedPointingModes = struct.unpack_from(">" + `_arraylen` + "i", buffer, _pos )
            _pos += 4 * _arraylen
        self.MinAzimuth = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxAzimuth = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.IsAzimuthClamped = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        self.MinElevation = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxElevation = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.IsElevationClamped = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        self.MinRotation = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxRotation = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.IsRotationClamped = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        self.MaxAzimuthSlewRate = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxElevationSlewRate = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxRotationRate = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.ContainedPayloadList = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.ContainedPayloadList = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        return _pos


    def get_SupportedPointingModes(self):
        return self.SupportedPointingModes

    def get_MinAzimuth(self):
        return self.MinAzimuth

    def set_MinAzimuth(self, value):
        self.MinAzimuth = float( value )

    def get_MaxAzimuth(self):
        return self.MaxAzimuth

    def set_MaxAzimuth(self, value):
        self.MaxAzimuth = float( value )

    def get_IsAzimuthClamped(self):
        return self.IsAzimuthClamped

    def set_IsAzimuthClamped(self, value):
        self.IsAzimuthClamped = bool( value )

    def get_MinElevation(self):
        return self.MinElevation

    def set_MinElevation(self, value):
        self.MinElevation = float( value )

    def get_MaxElevation(self):
        return self.MaxElevation

    def set_MaxElevation(self, value):
        self.MaxElevation = float( value )

    def get_IsElevationClamped(self):
        return self.IsElevationClamped

    def set_IsElevationClamped(self, value):
        self.IsElevationClamped = bool( value )

    def get_MinRotation(self):
        return self.MinRotation

    def set_MinRotation(self, value):
        self.MinRotation = float( value )

    def get_MaxRotation(self):
        return self.MaxRotation

    def set_MaxRotation(self, value):
        self.MaxRotation = float( value )

    def get_IsRotationClamped(self):
        return self.IsRotationClamped

    def set_IsRotationClamped(self, value):
        self.IsRotationClamped = bool( value )

    def get_MaxAzimuthSlewRate(self):
        return self.MaxAzimuthSlewRate

    def set_MaxAzimuthSlewRate(self, value):
        self.MaxAzimuthSlewRate = float( value )

    def get_MaxElevationSlewRate(self):
        return self.MaxElevationSlewRate

    def set_MaxElevationSlewRate(self, value):
        self.MaxElevationSlewRate = float( value )

    def get_MaxRotationRate(self):
        return self.MaxRotationRate

    def set_MaxRotationRate(self, value):
        self.MaxRotationRate = float( value )

    def get_ContainedPayloadList(self):
        return self.ContainedPayloadList



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = PayloadConfiguration.PayloadConfiguration.toString(self)
        buf += "From GimbalConfiguration:\n"
        buf +=    "SupportedPointingModes = " + str( self.SupportedPointingModes ) + "\n" 
        buf +=    "MinAzimuth = " + str( self.MinAzimuth ) + "\n" 
        buf +=    "MaxAzimuth = " + str( self.MaxAzimuth ) + "\n" 
        buf +=    "IsAzimuthClamped = " + str( self.IsAzimuthClamped ) + "\n" 
        buf +=    "MinElevation = " + str( self.MinElevation ) + "\n" 
        buf +=    "MaxElevation = " + str( self.MaxElevation ) + "\n" 
        buf +=    "IsElevationClamped = " + str( self.IsElevationClamped ) + "\n" 
        buf +=    "MinRotation = " + str( self.MinRotation ) + "\n" 
        buf +=    "MaxRotation = " + str( self.MaxRotation ) + "\n" 
        buf +=    "IsRotationClamped = " + str( self.IsRotationClamped ) + "\n" 
        buf +=    "MaxAzimuthSlewRate = " + str( self.MaxAzimuthSlewRate ) + "\n" 
        buf +=    "MaxElevationSlewRate = " + str( self.MaxElevationSlewRate ) + "\n" 
        buf +=    "MaxRotationRate = " + str( self.MaxRotationRate ) + "\n" 
        buf +=    "ContainedPayloadList = " + str( self.ContainedPayloadList ) + "\n" 

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
        str = ws + "<GimbalConfiguration>\n";
        #str +=PayloadConfiguration.PayloadConfiguration.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</GimbalConfiguration>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += PayloadConfiguration.PayloadConfiguration.toXMLMembersStr(self, ws)
        buf += ws + "<SupportedPointingModes>\n"
        for x in self.SupportedPointingModes:
            buf += ws + "<GimbalPointingMode>" + GimbalPointingMode.get_GimbalPointingMode_int(x) + "</GimbalPointingMode>\n"
        buf += ws + "</SupportedPointingModes>\n"
        buf += ws + "<MinAzimuth>" + str(self.MinAzimuth) + "</MinAzimuth>\n"
        buf += ws + "<MaxAzimuth>" + str(self.MaxAzimuth) + "</MaxAzimuth>\n"
        buf += ws + "<IsAzimuthClamped>" + str(self.IsAzimuthClamped) + "</IsAzimuthClamped>\n"
        buf += ws + "<MinElevation>" + str(self.MinElevation) + "</MinElevation>\n"
        buf += ws + "<MaxElevation>" + str(self.MaxElevation) + "</MaxElevation>\n"
        buf += ws + "<IsElevationClamped>" + str(self.IsElevationClamped) + "</IsElevationClamped>\n"
        buf += ws + "<MinRotation>" + str(self.MinRotation) + "</MinRotation>\n"
        buf += ws + "<MaxRotation>" + str(self.MaxRotation) + "</MaxRotation>\n"
        buf += ws + "<IsRotationClamped>" + str(self.IsRotationClamped) + "</IsRotationClamped>\n"
        buf += ws + "<MaxAzimuthSlewRate>" + str(self.MaxAzimuthSlewRate) + "</MaxAzimuthSlewRate>\n"
        buf += ws + "<MaxElevationSlewRate>" + str(self.MaxElevationSlewRate) + "</MaxElevationSlewRate>\n"
        buf += ws + "<MaxRotationRate>" + str(self.MaxRotationRate) + "</MaxRotationRate>\n"
        buf += ws + "<ContainedPayloadList>\n"
        for x in self.ContainedPayloadList:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</ContainedPayloadList>\n"

        return buf
        
