#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import GimballedPayloadState
from afrl.cmasi import Location3D


class CameraState(GimballedPayloadState.GimballedPayloadState):

    def __init__(self):
        GimballedPayloadState.GimballedPayloadState.__init__(self)
        self.LMCP_TYPE = 21
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.HorizontalFieldOfView = 0   #real32
        self.VerticalFieldOfView = 0   #real32
        self.Footprint = []   #Location3D
        self.Centerpoint = None   #Location3D


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(GimballedPayloadState.GimballedPayloadState.pack(self))
        buffer.append(struct.pack(">f", self.HorizontalFieldOfView))
        buffer.append(struct.pack(">f", self.VerticalFieldOfView))
        buffer.append(struct.pack(">H", len(self.Footprint) ))
        for x in self.Footprint:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack("B", self.Centerpoint != None ))
        if self.Centerpoint != None:
            buffer.append(struct.pack(">q", self.Centerpoint.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.Centerpoint.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.Centerpoint.SERIES_VERSION))
            buffer.append(self.Centerpoint.pack())

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = GimballedPayloadState.GimballedPayloadState.unpack(self, buffer, _pos)
        self.HorizontalFieldOfView = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.VerticalFieldOfView = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.Footprint = [None] * _arraylen
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
                self.Footprint[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.Footprint[x].unpack(buffer, _pos)
            else:
                self.Footprint[x] = None
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
            self.Centerpoint = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.Centerpoint.unpack(buffer, _pos)
        else:
            self.Centerpoint = None
        return _pos


    def get_HorizontalFieldOfView(self):
        return self.HorizontalFieldOfView

    def set_HorizontalFieldOfView(self, value):
        self.HorizontalFieldOfView = float( value )

    def get_VerticalFieldOfView(self):
        return self.VerticalFieldOfView

    def set_VerticalFieldOfView(self, value):
        self.VerticalFieldOfView = float( value )

    def get_Footprint(self):
        return self.Footprint

    def get_Centerpoint(self):
        return self.Centerpoint

    def set_Centerpoint(self, value):
        self.Centerpoint = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = GimballedPayloadState.GimballedPayloadState.toString(self)
        buf += "From CameraState:\n"
        buf +=    "HorizontalFieldOfView = " + str( self.HorizontalFieldOfView ) + "\n" 
        buf +=    "VerticalFieldOfView = " + str( self.VerticalFieldOfView ) + "\n" 
        buf +=    "Footprint = " + str( self.Footprint ) + "\n" 
        buf +=    "Centerpoint = " + str( self.Centerpoint ) + "\n" 

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
        str = ws + "<CameraState>\n";
        #str +=GimballedPayloadState.GimballedPayloadState.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</CameraState>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += GimballedPayloadState.GimballedPayloadState.toXMLMembersStr(self, ws)
        buf += ws + "<HorizontalFieldOfView>" + str(self.HorizontalFieldOfView) + "</HorizontalFieldOfView>\n"
        buf += ws + "<VerticalFieldOfView>" + str(self.VerticalFieldOfView) + "</VerticalFieldOfView>\n"
        buf += ws + "<Footprint>\n"
        for x in self.Footprint:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Footprint>\n"
        buf += ws + "<Centerpoint>\n"
        if self.Centerpoint == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.Centerpoint.toXMLStr(ws + "    ") 
        buf += ws + "</Centerpoint>\n"

        return buf
        
