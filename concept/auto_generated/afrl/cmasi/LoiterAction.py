#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import NavigationAction
from afrl.cmasi import LoiterType
from afrl.cmasi import LoiterDirection
from afrl.cmasi import Location3D


class LoiterAction(NavigationAction.NavigationAction):

    def __init__(self):
        NavigationAction.NavigationAction.__init__(self)
        self.LMCP_TYPE = 33
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.LoiterType = LoiterType.LoiterType.VehicleDefault   #LoiterType
        self.Radius = 0   #real32
        self.Axis = 0   #real32
        self.Length = 0   #real32
        self.Direction = LoiterDirection.LoiterDirection.VehicleDefault   #LoiterDirection
        self.Duration = 0   #int64
        self.Airspeed = 0   #real32
        self.Location = Location3D.Location3D()   #Location3D


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(NavigationAction.NavigationAction.pack(self))
        buffer.append(struct.pack(">i", self.LoiterType))
        buffer.append(struct.pack(">f", self.Radius))
        buffer.append(struct.pack(">f", self.Axis))
        buffer.append(struct.pack(">f", self.Length))
        buffer.append(struct.pack(">i", self.Direction))
        buffer.append(struct.pack(">q", self.Duration))#CHANGED from l to q
        buffer.append(struct.pack(">f", self.Airspeed))
        buffer.append(struct.pack("B", self.Location != None ))
        if self.Location != None:
            buffer.append(struct.pack(">q", self.Location.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.Location.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.Location.SERIES_VERSION))
            buffer.append(self.Location.pack())

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = NavigationAction.NavigationAction.unpack(self, buffer, _pos)
        self.LoiterType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.Radius = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Axis = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Length = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.Direction = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.Duration = struct.unpack_from(">q", buffer, _pos)[0]#CHANGED from l to q
        _pos += 8
        self.Airspeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
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
            self.Location = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.Location.unpack(buffer, _pos)
        else:
            self.Location = None
        return _pos


    def get_LoiterType(self):
        return self.LoiterType

    def set_LoiterType(self, value):
        self.LoiterType = value 

    def get_Radius(self):
        return self.Radius

    def set_Radius(self, value):
        self.Radius = float( value )

    def get_Axis(self):
        return self.Axis

    def set_Axis(self, value):
        self.Axis = float( value )

    def get_Length(self):
        return self.Length

    def set_Length(self, value):
        self.Length = float( value )

    def get_Direction(self):
        return self.Direction

    def set_Direction(self, value):
        self.Direction = value 

    def get_Duration(self):
        return self.Duration

    def set_Duration(self, value):
        self.Duration = int( value )

    def get_Airspeed(self):
        return self.Airspeed

    def set_Airspeed(self, value):
        self.Airspeed = float( value )

    def get_Location(self):
        return self.Location

    def set_Location(self, value):
        self.Location = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = NavigationAction.NavigationAction.toString(self)
        buf += "From LoiterAction:\n"
        buf +=    "LoiterType = " + str( self.LoiterType ) + "\n" 
        buf +=    "Radius = " + str( self.Radius ) + "\n" 
        buf +=    "Axis = " + str( self.Axis ) + "\n" 
        buf +=    "Length = " + str( self.Length ) + "\n" 
        buf +=    "Direction = " + str( self.Direction ) + "\n" 
        buf +=    "Duration = " + str( self.Duration ) + "\n" 
        buf +=    "Airspeed = " + str( self.Airspeed ) + "\n" 
        buf +=    "Location = " + str( self.Location ) + "\n" 

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
        str = ws + "<LoiterAction>\n";
        #str +=NavigationAction.NavigationAction.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</LoiterAction>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += NavigationAction.NavigationAction.toXMLMembersStr(self, ws)
        buf += ws + "<LoiterType>" + LoiterType.get_LoiterType_int(self.LoiterType) + "</LoiterType>\n"
        buf += ws + "<Radius>" + str(self.Radius) + "</Radius>\n"
        buf += ws + "<Axis>" + str(self.Axis) + "</Axis>\n"
        buf += ws + "<Length>" + str(self.Length) + "</Length>\n"
        buf += ws + "<Direction>" + LoiterDirection.get_LoiterDirection_int(self.Direction) + "</Direction>\n"
        buf += ws + "<Duration>" + str(self.Duration) + "</Duration>\n"
        buf += ws + "<Airspeed>" + str(self.Airspeed) + "</Airspeed>\n"
        buf += ws + "<Location>\n"
        if self.Location == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.Location.toXMLStr(ws + "    ") 
        buf += ws + "</Location>\n"

        return buf
        
