#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import AltitudeType
from afrl.cmasi import AbstractGeometry


class AbstractZone(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 10
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.ZoneID = 0   #int64
        self.MinAltitude = 0   #real32
        self.MinAltitudeType = AltitudeType.AltitudeType.AGL   #AltitudeType
        self.MaxAltitude = 0   #real32
        self.MaxAltitudeType = AltitudeType.AltitudeType.MSL   #AltitudeType
        self.AffectedAircraft = []   #int64
        self.StartTime = 0   #int64
        self.EndTime = 0   #int64
        self.Padding = 0   #real32
        self.Label = ""   #string
        self.Boundary = AbstractGeometry.AbstractGeometry()   #AbstractGeometry


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">l", self.ZoneID))
        buffer.append(struct.pack(">f", self.MinAltitude))
        buffer.append(struct.pack(">i", self.MinAltitudeType))
        buffer.append(struct.pack(">f", self.MaxAltitude))
        buffer.append(struct.pack(">i", self.MaxAltitudeType))
        buffer.append(struct.pack(">H", len(self.AffectedAircraft) ))
        for x in self.AffectedAircraft:
            buffer.append(struct.pack(">l", x ))
        buffer.append(struct.pack(">l", self.StartTime))
        buffer.append(struct.pack(">l", self.EndTime))
        buffer.append(struct.pack(">f", self.Padding))
        buffer.append(struct.pack(">H", len(self.Label) ))
        if len(self.Label) > 0:
            buffer.append(struct.pack( `len(self.Label)` + "s", self.Label))
        buffer.append(struct.pack("B", self.Boundary != None ))
        if self.Boundary != None:
            buffer.append(struct.pack(">q", self.Boundary.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.Boundary.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.Boundary.SERIES_VERSION))
            buffer.append(self.Boundary.pack())

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.ZoneID = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.MinAltitude = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MinAltitudeType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.MaxAltitude = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxAltitudeType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.AffectedAircraft = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.AffectedAircraft = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        self.StartTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.EndTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.Padding = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.Label = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.Label = ""
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
            self.Boundary = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.Boundary.unpack(buffer, _pos)
        else:
            self.Boundary = None
        return _pos


    def get_ZoneID(self):
        return self.ZoneID

    def set_ZoneID(self, value):
        self.ZoneID = int( value )

    def get_MinAltitude(self):
        return self.MinAltitude

    def set_MinAltitude(self, value):
        self.MinAltitude = float( value )

    def get_MinAltitudeType(self):
        return self.MinAltitudeType

    def set_MinAltitudeType(self, value):
        self.MinAltitudeType = value 

    def get_MaxAltitude(self):
        return self.MaxAltitude

    def set_MaxAltitude(self, value):
        self.MaxAltitude = float( value )

    def get_MaxAltitudeType(self):
        return self.MaxAltitudeType

    def set_MaxAltitudeType(self, value):
        self.MaxAltitudeType = value 

    def get_AffectedAircraft(self):
        return self.AffectedAircraft

    def get_StartTime(self):
        return self.StartTime

    def set_StartTime(self, value):
        self.StartTime = int( value )

    def get_EndTime(self):
        return self.EndTime

    def set_EndTime(self, value):
        self.EndTime = int( value )

    def get_Padding(self):
        return self.Padding

    def set_Padding(self, value):
        self.Padding = float( value )

    def get_Label(self):
        return self.Label

    def set_Label(self, value):
        self.Label = str( value )

    def get_Boundary(self):
        return self.Boundary

    def set_Boundary(self, value):
        self.Boundary = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From AbstractZone:\n"
        buf +=    "ZoneID = " + str( self.ZoneID ) + "\n" 
        buf +=    "MinAltitude = " + str( self.MinAltitude ) + "\n" 
        buf +=    "MinAltitudeType = " + str( self.MinAltitudeType ) + "\n" 
        buf +=    "MaxAltitude = " + str( self.MaxAltitude ) + "\n" 
        buf +=    "MaxAltitudeType = " + str( self.MaxAltitudeType ) + "\n" 
        buf +=    "AffectedAircraft = " + str( self.AffectedAircraft ) + "\n" 
        buf +=    "StartTime = " + str( self.StartTime ) + "\n" 
        buf +=    "EndTime = " + str( self.EndTime ) + "\n" 
        buf +=    "Padding = " + str( self.Padding ) + "\n" 
        buf +=    "Label = " + str( self.Label ) + "\n" 
        buf +=    "Boundary = " + str( self.Boundary ) + "\n" 

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
        str = ws + "<AbstractZone>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</AbstractZone>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<ZoneID>" + str(self.ZoneID) + "</ZoneID>\n"
        buf += ws + "<MinAltitude>" + str(self.MinAltitude) + "</MinAltitude>\n"
        buf += ws + "<MinAltitudeType>" + AltitudeType.get_AltitudeType_int(self.MinAltitudeType) + "</MinAltitudeType>\n"
        buf += ws + "<MaxAltitude>" + str(self.MaxAltitude) + "</MaxAltitude>\n"
        buf += ws + "<MaxAltitudeType>" + AltitudeType.get_AltitudeType_int(self.MaxAltitudeType) + "</MaxAltitudeType>\n"
        buf += ws + "<AffectedAircraft>\n"
        for x in self.AffectedAircraft:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</AffectedAircraft>\n"
        buf += ws + "<StartTime>" + str(self.StartTime) + "</StartTime>\n"
        buf += ws + "<EndTime>" + str(self.EndTime) + "</EndTime>\n"
        buf += ws + "<Padding>" + str(self.Padding) + "</Padding>\n"
        buf += ws + "<Label>" + str(self.Label) + "</Label>\n"
        buf += ws + "<Boundary>\n"
        if self.Boundary == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.Boundary.toXMLStr(ws + "    ") 
        buf += ws + "</Boundary>\n"

        return buf
        
