#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import NavigationAction


class GoToWaypointAction(NavigationAction.NavigationAction):

    def __init__(self):
        NavigationAction.NavigationAction.__init__(self)
        self.LMCP_TYPE = 28
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.WaypointNumber = 0   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(NavigationAction.NavigationAction.pack(self))
        buffer.append(struct.pack(">l", self.WaypointNumber))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = NavigationAction.NavigationAction.unpack(self, buffer, _pos)
        self.WaypointNumber = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        return _pos


    def get_WaypointNumber(self):
        return self.WaypointNumber

    def set_WaypointNumber(self, value):
        self.WaypointNumber = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = NavigationAction.NavigationAction.toString(self)
        buf += "From GoToWaypointAction:\n"
        buf +=    "WaypointNumber = " + str( self.WaypointNumber ) + "\n" 

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
        str = ws + "<GoToWaypointAction>\n";
        #str +=NavigationAction.NavigationAction.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</GoToWaypointAction>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += NavigationAction.NavigationAction.toXMLMembersStr(self, ws)
        buf += ws + "<WaypointNumber>" + str(self.WaypointNumber) + "</WaypointNumber>\n"

        return buf
        
