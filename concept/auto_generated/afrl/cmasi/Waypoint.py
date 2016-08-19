#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Location3D
from afrl.cmasi import SpeedType
from afrl.cmasi import TurnType
from afrl.cmasi import VehicleAction


class Waypoint(Location3D.Location3D):

    def __init__(self):
        Location3D.Location3D.__init__(self)
        self.LMCP_TYPE = 35
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Number = 0   #int64
        self.NextWaypoint = 0   #int64
        self.Speed = 0   #real32
        self.SpeedType = SpeedType.SpeedType.Airspeed   #SpeedType
        self.ClimbRate = 0   #real32
        self.TurnType = TurnType.TurnType.TurnShort   #TurnType
        self.VehicleActionList = []   #VehicleAction
        self.ContingencyWaypointA = 0   #int64
        self.ContingencyWaypointB = 0   #int64
        self.AssociatedTasks = []   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(Location3D.Location3D.pack(self))
        buffer.append(struct.pack(">q", self.Number))#CHANGED from l to q
        buffer.append(struct.pack(">q", self.NextWaypoint))#CHANGED from l to q
        buffer.append(struct.pack(">f", self.Speed))
        buffer.append(struct.pack(">i", self.SpeedType))
        buffer.append(struct.pack(">f", self.ClimbRate))
        buffer.append(struct.pack(">i", self.TurnType))
        buffer.append(struct.pack(">H", len(self.VehicleActionList) ))
        for x in self.VehicleActionList:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">q", self.ContingencyWaypointA))#CHANGED from l to q
        buffer.append(struct.pack(">q", self.ContingencyWaypointB))#CHANGED from l to q
        buffer.append(struct.pack(">H", len(self.AssociatedTasks) ))
        for x in self.AssociatedTasks:
            buffer.append(struct.pack(">l", x ))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = Location3D.Location3D.unpack(self, buffer, _pos)
        self.Number = struct.unpack_from(">q", buffer, _pos)[0]#CHANGED from l to q
        _pos += 8
        self.NextWaypoint = struct.unpack_from(">q", buffer, _pos)[0]#CHANGED from l to q
        _pos += 8
        self.Speed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.SpeedType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.ClimbRate = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.TurnType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.VehicleActionList = [None] * _arraylen
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
                self.VehicleActionList[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.VehicleActionList[x].unpack(buffer, _pos)
            else:
                self.VehicleActionList[x] = None
        self.ContingencyWaypointA = struct.unpack_from(">q", buffer, _pos)[0]#CHANGED from l to q
        _pos += 8
        self.ContingencyWaypointB = struct.unpack_from(">q", buffer, _pos)[0]#CHANGED from l to q
        _pos += 8
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.AssociatedTasks = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.AssociatedTasks = struct.unpack_from(">" + `_arraylen` + "q", buffer, _pos )#CHANGED from l to q
            _pos += 8 * _arraylen
        return _pos


    def get_Number(self):
        return self.Number

    def set_Number(self, value):
        self.Number = int( value )

    def get_NextWaypoint(self):
        return self.NextWaypoint

    def set_NextWaypoint(self, value):
        self.NextWaypoint = int( value )

    def get_Speed(self):
        return self.Speed

    def set_Speed(self, value):
        self.Speed = float( value )

    def get_SpeedType(self):
        return self.SpeedType

    def set_SpeedType(self, value):
        self.SpeedType = value 

    def get_ClimbRate(self):
        return self.ClimbRate

    def set_ClimbRate(self, value):
        self.ClimbRate = float( value )

    def get_TurnType(self):
        return self.TurnType

    def set_TurnType(self, value):
        self.TurnType = value 

    def get_VehicleActionList(self):
        return self.VehicleActionList

    def get_ContingencyWaypointA(self):
        return self.ContingencyWaypointA

    def set_ContingencyWaypointA(self, value):
        self.ContingencyWaypointA = int( value )

    def get_ContingencyWaypointB(self):
        return self.ContingencyWaypointB

    def set_ContingencyWaypointB(self, value):
        self.ContingencyWaypointB = int( value )

    def get_AssociatedTasks(self):
        return self.AssociatedTasks



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = Location3D.Location3D.toString(self)
        buf += "From Waypoint:\n"
        buf +=    "Number = " + str( self.Number ) + "\n" 
        buf +=    "NextWaypoint = " + str( self.NextWaypoint ) + "\n" 
        buf +=    "Speed = " + str( self.Speed ) + "\n" 
        buf +=    "SpeedType = " + str( self.SpeedType ) + "\n" 
        buf +=    "ClimbRate = " + str( self.ClimbRate ) + "\n" 
        buf +=    "TurnType = " + str( self.TurnType ) + "\n" 
        buf +=    "VehicleActionList = " + str( self.VehicleActionList ) + "\n" 
        buf +=    "ContingencyWaypointA = " + str( self.ContingencyWaypointA ) + "\n" 
        buf +=    "ContingencyWaypointB = " + str( self.ContingencyWaypointB ) + "\n" 
        buf +=    "AssociatedTasks = " + str( self.AssociatedTasks ) + "\n" 

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
        str = ws + "<Waypoint>\n";
        #str +=Location3D.Location3D.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</Waypoint>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += Location3D.Location3D.toXMLMembersStr(self, ws)
        buf += ws + "<Number>" + str(self.Number) + "</Number>\n"
        buf += ws + "<NextWaypoint>" + str(self.NextWaypoint) + "</NextWaypoint>\n"
        buf += ws + "<Speed>" + str(self.Speed) + "</Speed>\n"
        buf += ws + "<SpeedType>" + SpeedType.get_SpeedType_int(self.SpeedType) + "</SpeedType>\n"
        buf += ws + "<ClimbRate>" + str(self.ClimbRate) + "</ClimbRate>\n"
        buf += ws + "<TurnType>" + TurnType.get_TurnType_int(self.TurnType) + "</TurnType>\n"
        buf += ws + "<VehicleActionList>\n"
        for x in self.VehicleActionList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</VehicleActionList>\n"
        buf += ws + "<ContingencyWaypointA>" + str(self.ContingencyWaypointA) + "</ContingencyWaypointA>\n"
        buf += ws + "<ContingencyWaypointB>" + str(self.ContingencyWaypointB) + "</ContingencyWaypointB>\n"
        buf += ws + "<AssociatedTasks>\n"
        for x in self.AssociatedTasks:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</AssociatedTasks>\n"

        return buf
        
