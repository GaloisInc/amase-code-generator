#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import EntityState


class AirVehicleState(EntityState.EntityState):

    def __init__(self):
        EntityState.EntityState.__init__(self)
        self.LMCP_TYPE = 15
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Airspeed = 0   #real32
        self.VerticalSpeed = 0   #real32
        self.WindSpeed = 0   #real32
        self.WindDirection = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(EntityState.EntityState.pack(self))
        buffer.append(struct.pack(">f", self.Airspeed))
        buffer.append(struct.pack(">f", self.VerticalSpeed))
        buffer.append(struct.pack(">f", self.WindSpeed))
        buffer.append(struct.pack(">f", self.WindDirection))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = EntityState.EntityState.unpack(self, buffer, _pos)
        self.Airspeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.VerticalSpeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.WindSpeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.WindDirection = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_Airspeed(self):
        return self.Airspeed

    def set_Airspeed(self, value):
        self.Airspeed = float( value )

    def get_VerticalSpeed(self):
        return self.VerticalSpeed

    def set_VerticalSpeed(self, value):
        self.VerticalSpeed = float( value )

    def get_WindSpeed(self):
        return self.WindSpeed

    def set_WindSpeed(self, value):
        self.WindSpeed = float( value )

    def get_WindDirection(self):
        return self.WindDirection

    def set_WindDirection(self, value):
        self.WindDirection = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = EntityState.EntityState.toString(self)
        buf += "From AirVehicleState:\n"
        buf +=    "Airspeed = " + str( self.Airspeed ) + "\n" 
        buf +=    "VerticalSpeed = " + str( self.VerticalSpeed ) + "\n" 
        buf +=    "WindSpeed = " + str( self.WindSpeed ) + "\n" 
        buf +=    "WindDirection = " + str( self.WindDirection ) + "\n" 

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
        str = ws + "<AirVehicleState>\n";
        #str +=EntityState.EntityState.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</AirVehicleState>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += EntityState.EntityState.toXMLMembersStr(self, ws)
        buf += ws + "<Airspeed>" + str(self.Airspeed) + "</Airspeed>\n"
        buf += ws + "<VerticalSpeed>" + str(self.VerticalSpeed) + "</VerticalSpeed>\n"
        buf += ws + "<WindSpeed>" + str(self.WindSpeed) + "</WindSpeed>\n"
        buf += ws + "<WindDirection>" + str(self.WindDirection) + "</WindDirection>\n"

        return buf
        
