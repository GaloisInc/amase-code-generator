#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import VehicleActionCommand
from afrl.cmasi import PathWaypoint
from afrl.cmasi import TravelMode


class FollowPathCommand(VehicleActionCommand.VehicleActionCommand):

    def __init__(self):
        VehicleActionCommand.VehicleActionCommand.__init__(self)
        self.LMCP_TYPE = 56
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.FirstWaypoint = 0   #int64
        self.WaypointList = []   #PathWaypoint
        self.StartTime = 0   #int64
        self.StopTime = 0   #int64
        self.RepeatMode = TravelMode.TravelMode.SinglePass   #TravelMode


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(VehicleActionCommand.VehicleActionCommand.pack(self))
        buffer.append(struct.pack(">l", self.FirstWaypoint))
        buffer.append(struct.pack(">H", len(self.WaypointList) ))
        for x in self.WaypointList:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">l", self.StartTime))
        buffer.append(struct.pack(">l", self.StopTime))
        buffer.append(struct.pack(">i", self.RepeatMode))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = VehicleActionCommand.VehicleActionCommand.unpack(self, buffer, _pos)
        self.FirstWaypoint = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
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
        self.StartTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.StopTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.RepeatMode = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_FirstWaypoint(self):
        return self.FirstWaypoint

    def set_FirstWaypoint(self, value):
        self.FirstWaypoint = int( value )

    def get_WaypointList(self):
        return self.WaypointList

    def get_StartTime(self):
        return self.StartTime

    def set_StartTime(self, value):
        self.StartTime = int( value )

    def get_StopTime(self):
        return self.StopTime

    def set_StopTime(self, value):
        self.StopTime = int( value )

    def get_RepeatMode(self):
        return self.RepeatMode

    def set_RepeatMode(self, value):
        self.RepeatMode = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = VehicleActionCommand.VehicleActionCommand.toString(self)
        buf += "From FollowPathCommand:\n"
        buf +=    "FirstWaypoint = " + str( self.FirstWaypoint ) + "\n" 
        buf +=    "WaypointList = " + str( self.WaypointList ) + "\n" 
        buf +=    "StartTime = " + str( self.StartTime ) + "\n" 
        buf +=    "StopTime = " + str( self.StopTime ) + "\n" 
        buf +=    "RepeatMode = " + str( self.RepeatMode ) + "\n" 

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
        str = ws + "<FollowPathCommand>\n";
        #str +=VehicleActionCommand.VehicleActionCommand.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</FollowPathCommand>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += VehicleActionCommand.VehicleActionCommand.toXMLMembersStr(self, ws)
        buf += ws + "<FirstWaypoint>" + str(self.FirstWaypoint) + "</FirstWaypoint>\n"
        buf += ws + "<WaypointList>\n"
        for x in self.WaypointList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</WaypointList>\n"
        buf += ws + "<StartTime>" + str(self.StartTime) + "</StartTime>\n"
        buf += ws + "<StopTime>" + str(self.StopTime) + "</StopTime>\n"
        buf += ws + "<RepeatMode>" + TravelMode.get_TravelMode_int(self.RepeatMode) + "</RepeatMode>\n"

        return buf
        
