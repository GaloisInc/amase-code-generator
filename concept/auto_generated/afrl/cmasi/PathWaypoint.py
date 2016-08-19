#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Waypoint


class PathWaypoint(Waypoint.Waypoint):

    def __init__(self):
        Waypoint.Waypoint.__init__(self)
        self.LMCP_TYPE = 57
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.PauseTime = 0   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(Waypoint.Waypoint.pack(self))
        buffer.append(struct.pack(">l", self.PauseTime))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = Waypoint.Waypoint.unpack(self, buffer, _pos)
        self.PauseTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        return _pos


    def get_PauseTime(self):
        return self.PauseTime

    def set_PauseTime(self, value):
        self.PauseTime = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = Waypoint.Waypoint.toString(self)
        buf += "From PathWaypoint:\n"
        buf +=    "PauseTime = " + str( self.PauseTime ) + "\n" 

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
        str = ws + "<PathWaypoint>\n";
        #str +=Waypoint.Waypoint.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</PathWaypoint>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += Waypoint.Waypoint.toXMLMembersStr(self, ws)
        buf += ws + "<PauseTime>" + str(self.PauseTime) + "</PauseTime>\n"

        return buf
        
