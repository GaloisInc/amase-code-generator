#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Waypoint
from afrl.cmasi import WaypointTransferMode


class WaypointTransfer(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 59
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.EntityID = 0   #int64
        self.Waypoints = []   #Waypoint
        self.TransferMode = WaypointTransferMode.WaypointTransferMode.AddWaypoints   #WaypointTransferMode


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">l", self.EntityID))
        buffer.append(struct.pack(">H", len(self.Waypoints) ))
        for x in self.Waypoints:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">i", self.TransferMode))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.EntityID = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.Waypoints = [None] * _arraylen
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
                self.Waypoints[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.Waypoints[x].unpack(buffer, _pos)
            else:
                self.Waypoints[x] = None
        self.TransferMode = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_EntityID(self):
        return self.EntityID

    def set_EntityID(self, value):
        self.EntityID = int( value )

    def get_Waypoints(self):
        return self.Waypoints

    def get_TransferMode(self):
        return self.TransferMode

    def set_TransferMode(self, value):
        self.TransferMode = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From WaypointTransfer:\n"
        buf +=    "EntityID = " + str( self.EntityID ) + "\n" 
        buf +=    "Waypoints = " + str( self.Waypoints ) + "\n" 
        buf +=    "TransferMode = " + str( self.TransferMode ) + "\n" 

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
        str = ws + "<WaypointTransfer>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</WaypointTransfer>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<EntityID>" + str(self.EntityID) + "</EntityID>\n"
        buf += ws + "<Waypoints>\n"
        for x in self.Waypoints:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Waypoints>\n"
        buf += ws + "<TransferMode>" + WaypointTransferMode.get_WaypointTransferMode_int(self.TransferMode) + "</TransferMode>\n"

        return buf
        
