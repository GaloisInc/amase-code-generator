#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadConfiguration
from afrl.cmasi import WavelengthBand
from afrl.cmasi import FOVOperationMode


class CameraConfiguration(PayloadConfiguration.PayloadConfiguration):

    def __init__(self):
        PayloadConfiguration.PayloadConfiguration.__init__(self)
        self.LMCP_TYPE = 19
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.SupportedWavelengthBand = WavelengthBand.WavelengthBand.EO   #WavelengthBand
        self.FieldOfViewMode = FOVOperationMode.FOVOperationMode.Continuous   #FOVOperationMode
        self.MinHorizontalFieldOfView = 0   #real32
        self.MaxHorizontalFieldOfView = 0   #real32
        self.DiscreteHorizontalFieldOfViewList = []   #real32
        self.VideoStreamHorizontalResolution = 0   #uint32
        self.VideoStreamVerticalResolution = 0   #uint32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(PayloadConfiguration.PayloadConfiguration.pack(self))
        buffer.append(struct.pack(">i", self.SupportedWavelengthBand))
        buffer.append(struct.pack(">i", self.FieldOfViewMode))
        buffer.append(struct.pack(">f", self.MinHorizontalFieldOfView))
        buffer.append(struct.pack(">f", self.MaxHorizontalFieldOfView))
        buffer.append(struct.pack(">H", len(self.DiscreteHorizontalFieldOfViewList) ))
        for x in self.DiscreteHorizontalFieldOfViewList:
            buffer.append(struct.pack(">f", x ))
        buffer.append(struct.pack(">I", self.VideoStreamHorizontalResolution))
        buffer.append(struct.pack(">I", self.VideoStreamVerticalResolution))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = PayloadConfiguration.PayloadConfiguration.unpack(self, buffer, _pos)
        self.SupportedWavelengthBand = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.FieldOfViewMode = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.MinHorizontalFieldOfView = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxHorizontalFieldOfView = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.DiscreteHorizontalFieldOfViewList = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.DiscreteHorizontalFieldOfViewList = struct.unpack_from(">" + `_arraylen` + "f", buffer, _pos )
            _pos += 4 * _arraylen
        self.VideoStreamHorizontalResolution = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        self.VideoStreamVerticalResolution = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_SupportedWavelengthBand(self):
        return self.SupportedWavelengthBand

    def set_SupportedWavelengthBand(self, value):
        self.SupportedWavelengthBand = value 

    def get_FieldOfViewMode(self):
        return self.FieldOfViewMode

    def set_FieldOfViewMode(self, value):
        self.FieldOfViewMode = value 

    def get_MinHorizontalFieldOfView(self):
        return self.MinHorizontalFieldOfView

    def set_MinHorizontalFieldOfView(self, value):
        self.MinHorizontalFieldOfView = float( value )

    def get_MaxHorizontalFieldOfView(self):
        return self.MaxHorizontalFieldOfView

    def set_MaxHorizontalFieldOfView(self, value):
        self.MaxHorizontalFieldOfView = float( value )

    def get_DiscreteHorizontalFieldOfViewList(self):
        return self.DiscreteHorizontalFieldOfViewList

    def get_VideoStreamHorizontalResolution(self):
        return self.VideoStreamHorizontalResolution

    def set_VideoStreamHorizontalResolution(self, value):
        self.VideoStreamHorizontalResolution = int( value )

    def get_VideoStreamVerticalResolution(self):
        return self.VideoStreamVerticalResolution

    def set_VideoStreamVerticalResolution(self, value):
        self.VideoStreamVerticalResolution = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = PayloadConfiguration.PayloadConfiguration.toString(self)
        buf += "From CameraConfiguration:\n"
        buf +=    "SupportedWavelengthBand = " + str( self.SupportedWavelengthBand ) + "\n" 
        buf +=    "FieldOfViewMode = " + str( self.FieldOfViewMode ) + "\n" 
        buf +=    "MinHorizontalFieldOfView = " + str( self.MinHorizontalFieldOfView ) + "\n" 
        buf +=    "MaxHorizontalFieldOfView = " + str( self.MaxHorizontalFieldOfView ) + "\n" 
        buf +=    "DiscreteHorizontalFieldOfViewList = " + str( self.DiscreteHorizontalFieldOfViewList ) + "\n" 
        buf +=    "VideoStreamHorizontalResolution = " + str( self.VideoStreamHorizontalResolution ) + "\n" 
        buf +=    "VideoStreamVerticalResolution = " + str( self.VideoStreamVerticalResolution ) + "\n" 

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
        str = ws + "<CameraConfiguration>\n";
        #str +=PayloadConfiguration.PayloadConfiguration.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</CameraConfiguration>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += PayloadConfiguration.PayloadConfiguration.toXMLMembersStr(self, ws)
        buf += ws + "<SupportedWavelengthBand>" + WavelengthBand.get_WavelengthBand_int(self.SupportedWavelengthBand) + "</SupportedWavelengthBand>\n"
        buf += ws + "<FieldOfViewMode>" + FOVOperationMode.get_FOVOperationMode_int(self.FieldOfViewMode) + "</FieldOfViewMode>\n"
        buf += ws + "<MinHorizontalFieldOfView>" + str(self.MinHorizontalFieldOfView) + "</MinHorizontalFieldOfView>\n"
        buf += ws + "<MaxHorizontalFieldOfView>" + str(self.MaxHorizontalFieldOfView) + "</MaxHorizontalFieldOfView>\n"
        buf += ws + "<DiscreteHorizontalFieldOfViewList>\n"
        for x in self.DiscreteHorizontalFieldOfViewList:
            buf += ws + "<real32>" + str(x) + "</real32>\n"
        buf += ws + "</DiscreteHorizontalFieldOfViewList>\n"
        buf += ws + "<VideoStreamHorizontalResolution>" + str(self.VideoStreamHorizontalResolution) + "</VideoStreamHorizontalResolution>\n"
        buf += ws + "<VideoStreamVerticalResolution>" + str(self.VideoStreamVerticalResolution) + "</VideoStreamVerticalResolution>\n"

        return buf
        
