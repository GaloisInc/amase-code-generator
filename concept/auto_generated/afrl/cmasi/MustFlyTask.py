#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Task
from afrl.cmasi import Location3D


class MustFlyTask(Task.Task):

    def __init__(self):
        Task.Task.__init__(self)
        self.LMCP_TYPE = 37
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Position = Location3D.Location3D()   #Location3D
        self.UseAltitude = True   #bool


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(Task.Task.pack(self))
        buffer.append(struct.pack("B", self.Position != None ))
        if self.Position != None:
            buffer.append(struct.pack(">q", self.Position.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.Position.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.Position.SERIES_VERSION))
            buffer.append(self.Position.pack())
        buffer.append(struct.pack(">B", self.UseAltitude))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = Task.Task.unpack(self, buffer, _pos)
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
            self.Position = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.Position.unpack(buffer, _pos)
        else:
            self.Position = None
        self.UseAltitude = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        return _pos


    def get_Position(self):
        return self.Position

    def set_Position(self, value):
        self.Position = value 

    def get_UseAltitude(self):
        return self.UseAltitude

    def set_UseAltitude(self, value):
        self.UseAltitude = bool( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = Task.Task.toString(self)
        buf += "From MustFlyTask:\n"
        buf +=    "Position = " + str( self.Position ) + "\n" 
        buf +=    "UseAltitude = " + str( self.UseAltitude ) + "\n" 

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
        str = ws + "<MustFlyTask>\n";
        #str +=Task.Task.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</MustFlyTask>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += Task.Task.toXMLMembersStr(self, ws)
        buf += ws + "<Position>\n"
        if self.Position == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.Position.toXMLStr(ws + "    ") 
        buf += ws + "</Position>\n"
        buf += ws + "<UseAltitude>" + str(self.UseAltitude) + "</UseAltitude>\n"

        return buf
        
