#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import AbstractGeometry
from afrl.cmasi import Location3D


class Circle(AbstractGeometry.AbstractGeometry):

    def __init__(self):
        AbstractGeometry.AbstractGeometry.__init__(self)
        self.LMCP_TYPE = 22
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.CenterPoint = Location3D.Location3D()   #Location3D
        self.Radius = 0   #real32


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
        buffer.append(struct.pack(">f", self.Radius))

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
        self.Radius = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_CenterPoint(self):
        return self.CenterPoint

    def set_CenterPoint(self, value):
        self.CenterPoint = value 

    def get_Radius(self):
        return self.Radius

    def set_Radius(self, value):
        self.Radius = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = AbstractGeometry.AbstractGeometry.toString(self)
        buf += "From Circle:\n"
        buf +=    "CenterPoint = " + str( self.CenterPoint ) + "\n" 
        buf +=    "Radius = " + str( self.Radius ) + "\n" 

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
        str = ws + "<Circle>\n";
        #str +=AbstractGeometry.AbstractGeometry.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</Circle>\n";
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
        buf += ws + "<Radius>" + str(self.Radius) + "</Radius>\n"

        return buf
        
