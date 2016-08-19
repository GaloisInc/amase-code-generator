#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import AbstractGeometry
from afrl.cmasi import Location3D


class Rectangle(AbstractGeometry.AbstractGeometry):

    def __init__(self):
        AbstractGeometry.AbstractGeometry.__init__(self)
        self.LMCP_TYPE = 43
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.CenterPoint = Location3D.Location3D()   #Location3D
        self.Width = 0   #real32
        self.Height = 0   #real32
        self.Rotation = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(AbstractGeometry.AbstractGeometry.pack(self))
        buffer.append(struct.pack("B", self.CenterPoint != None ))
        if self.CenterPoint != None:
            buffer.append(struct.pack(">q", self.CenterPoint.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.CenterPoint.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.CenterPoint.SERIES_VERSION))
            buffer.append(self.CenterPoint.pack())
        buffer.append(struct.pack(">f", self.Width))
        buffer.append(struct.pack(">f", self.Height))
        buffer.append(struct.pack(">f", self.Rotation))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = AbstractGeometry.AbstractGeometry.unpack(self, buffer, _pos)
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
            self.CenterPoint = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.CenterPoint.unpack(buffer, _pos)
        else:
            self.CenterPoint = None
        self.Width = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Height = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Rotation = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_CenterPoint(self):
        return self.CenterPoint

    def set_CenterPoint(self, value):
        self.CenterPoint = value 

    def get_Width(self):
        return self.Width

    def set_Width(self, value):
        self.Width = float( value )

    def get_Height(self):
        return self.Height

    def set_Height(self, value):
        self.Height = float( value )

    def get_Rotation(self):
        return self.Rotation

    def set_Rotation(self, value):
        self.Rotation = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = AbstractGeometry.AbstractGeometry.toString(self)
        buf += "From Rectangle:\n"
        buf +=    "CenterPoint = " + str( self.CenterPoint ) + "\n" 
        buf +=    "Width = " + str( self.Width ) + "\n" 
        buf +=    "Height = " + str( self.Height ) + "\n" 
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
        str = ws + "<Rectangle>\n";
        #str +=AbstractGeometry.AbstractGeometry.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</Rectangle>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += AbstractGeometry.AbstractGeometry.toXMLMembersStr(self, ws)
        buf += ws + "<CenterPoint>\n"
        if self.CenterPoint == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.CenterPoint.toXMLStr(ws + "    ") 
        buf += ws + "</CenterPoint>\n"
        buf += ws + "<Width>" + str(self.Width) + "</Width>\n"
        buf += ws + "<Height>" + str(self.Height) + "</Height>\n"
        buf += ws + "<Rotation>" + str(self.Rotation) + "</Rotation>\n"

        return buf
        
