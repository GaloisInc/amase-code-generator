#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import VehicleActionCommand
from afrl.cmasi import Waypoint


class MissionCommand(VehicleActionCommand.VehicleActionCommand):

    def __init__(self):
        VehicleActionCommand.VehicleActionCommand.__init__(self)
        self.LMCP_TYPE = 36
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.WaypointList = []   #Waypoint
        self.FirstWaypoint = 0   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(VehicleActionCommand.VehicleActionCommand.pack(self))
        buffer.append(struct.pack(">H", len(self.WaypointList) ))
        for x in self.WaypointList:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">q", self.FirstWaypoint))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = VehicleActionCommand.VehicleActionCommand.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.WaypointList = [None] * _arraylen
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
                self.WaypointList[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.WaypointList[x].unpack(buffer, _pos)
            else:
                self.WaypointList[x] = None
        self.FirstWaypoint = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        return _pos


    def get_WaypointList(self):
        return self.WaypointList

    def get_FirstWaypoint(self):
        return self.FirstWaypoint

    def set_FirstWaypoint(self, value):
        self.FirstWaypoint = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = VehicleActionCommand.VehicleActionCommand.toString(self)
        buf += "From MissionCommand:\n"
        buf +=    "WaypointList = " + str( self.WaypointList ) + "\n" 
        buf +=    "FirstWaypoint = " + str( self.FirstWaypoint ) + "\n" 

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
        str = ws + "<MissionCommand>\n";
        #str +=VehicleActionCommand.VehicleActionCommand.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</MissionCommand>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += VehicleActionCommand.VehicleActionCommand.toXMLMembersStr(self, ws)
        buf += ws + "<WaypointList>\n"
        for x in self.WaypointList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</WaypointList>\n"
        buf += ws + "<FirstWaypoint>" + str(self.FirstWaypoint) + "</FirstWaypoint>\n"

        return buf
        
