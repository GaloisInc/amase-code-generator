#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import VehicleAction


class TrackEntityAction(VehicleAction.VehicleAction):

    def __init__(self):
        VehicleAction.VehicleAction.__init__(self)
        self.LMCP_TYPE = 2
        self.SERIES_NAME = "PERCEIVE"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 5784119745305990725
        self.SERIES_VERSION = 1

        #Define message fields
        self.EntityID = 0   #uint32
        self.SensorID = 0   #uint32
        self.ReturnToWaypoint = 0   #uint32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(VehicleAction.VehicleAction.pack(self))
        buffer.append(struct.pack(">I", self.EntityID))
        buffer.append(struct.pack(">I", self.SensorID))
        buffer.append(struct.pack(">I", self.ReturnToWaypoint))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = VehicleAction.VehicleAction.unpack(self, buffer, _pos)
        self.EntityID = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        self.SensorID = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        self.ReturnToWaypoint = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_EntityID(self):
        return self.EntityID

    def set_EntityID(self, value):
        self.EntityID = int( value )

    def get_SensorID(self):
        return self.SensorID

    def set_SensorID(self, value):
        self.SensorID = int( value )

    def get_ReturnToWaypoint(self):
        return self.ReturnToWaypoint

    def set_ReturnToWaypoint(self, value):
        self.ReturnToWaypoint = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = VehicleAction.VehicleAction.toString(self)
        buf += "From TrackEntityAction:\n"
        buf +=    "EntityID = " + str( self.EntityID ) + "\n" 
        buf +=    "SensorID = " + str( self.SensorID ) + "\n" 
        buf +=    "ReturnToWaypoint = " + str( self.ReturnToWaypoint ) + "\n" 

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
        str = ws + "<TrackEntityAction>\n";
        #str +=VehicleAction.VehicleAction.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</TrackEntityAction>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += VehicleAction.VehicleAction.toXMLMembersStr(self, ws)
        buf += ws + "<EntityID>" + str(self.EntityID) + "</EntityID>\n"
        buf += ws + "<SensorID>" + str(self.SensorID) + "</SensorID>\n"
        buf += ws + "<ReturnToWaypoint>" + str(self.ReturnToWaypoint) + "</ReturnToWaypoint>\n"

        return buf
        
