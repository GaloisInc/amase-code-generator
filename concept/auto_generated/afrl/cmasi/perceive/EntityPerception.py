#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Location3D


class EntityPerception(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 1
        self.SERIES_NAME = "PERCEIVE"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 5784119745305990725
        self.SERIES_VERSION = 1

        #Define message fields
        self.PerceivedEntityID = 0   #uint32
        self.PerceiverID = 0   #uint32
        self.PerceiverPayloads = []   #uint32
        self.Velocity = [0]*3   #real32
        self.VelocityError = [0]*3   #real32
        self.VelocityValid = False   #bool
        self.Attitude = [0]*3   #real32
        self.AttitudeError = [0]*3   #real32
        self.AttitudeValid = False   #bool
        self.Location = Location3D.Location3D()   #Location3D
        self.LocationError = [0]*3   #real32
        self.TimeLastSeen = 0   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">I", self.PerceivedEntityID))
        buffer.append(struct.pack(">I", self.PerceiverID))
        buffer.append(struct.pack(">H", len(self.PerceiverPayloads) ))
        for x in self.PerceiverPayloads:
            buffer.append(struct.pack(">I", x ))
        for x in self.Velocity:
            buffer.append(struct.pack(">f", x ))
        for x in self.VelocityError:
            buffer.append(struct.pack(">f", x ))
        buffer.append(struct.pack(">B", self.VelocityValid))
        for x in self.Attitude:
            buffer.append(struct.pack(">f", x ))
        for x in self.AttitudeError:
            buffer.append(struct.pack(">f", x ))
        buffer.append(struct.pack(">B", self.AttitudeValid))
        buffer.append(struct.pack("B", self.Location != None ))
        if self.Location != None:
            buffer.append(struct.pack(">q", self.Location.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.Location.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.Location.SERIES_VERSION))
            buffer.append(self.Location.pack())
        for x in self.LocationError:
            buffer.append(struct.pack(">f", x ))
        buffer.append(struct.pack(">l", self.TimeLastSeen))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.PerceivedEntityID = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        self.PerceiverID = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.PerceiverPayloads = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.PerceiverPayloads = struct.unpack_from(">" + `_arraylen` + "I", buffer, _pos )
            _pos += 4 * _arraylen
        self.Velocity = [None] * 3
        _arraylen = 3
        if _arraylen > 0:
            self.Velocity = struct.unpack_from(">" + `_arraylen` + "f", buffer, _pos )
            _pos += 4 * _arraylen
        self.VelocityError = [None] * 3
        _arraylen = 3
        if _arraylen > 0:
            self.VelocityError = struct.unpack_from(">" + `_arraylen` + "f", buffer, _pos )
            _pos += 4 * _arraylen
        self.VelocityValid = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        self.Attitude = [None] * 3
        _arraylen = 3
        if _arraylen > 0:
            self.Attitude = struct.unpack_from(">" + `_arraylen` + "f", buffer, _pos )
            _pos += 4 * _arraylen
        self.AttitudeError = [None] * 3
        _arraylen = 3
        if _arraylen > 0:
            self.AttitudeError = struct.unpack_from(">" + `_arraylen` + "f", buffer, _pos )
            _pos += 4 * _arraylen
        self.AttitudeValid = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
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
        self.LocationError = [None] * 3
        _arraylen = 3
        if _arraylen > 0:
            self.LocationError = struct.unpack_from(">" + `_arraylen` + "f", buffer, _pos )
            _pos += 4 * _arraylen
        self.TimeLastSeen = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        return _pos


    def get_PerceivedEntityID(self):
        return self.PerceivedEntityID

    def set_PerceivedEntityID(self, value):
        self.PerceivedEntityID = int( value )

    def get_PerceiverID(self):
        return self.PerceiverID

    def set_PerceiverID(self, value):
        self.PerceiverID = int( value )

    def get_PerceiverPayloads(self):
        return self.PerceiverPayloads

    def get_Velocity(self):
        return self.Velocity

    def get_VelocityError(self):
        return self.VelocityError

    def get_VelocityValid(self):
        return self.VelocityValid

    def set_VelocityValid(self, value):
        self.VelocityValid = bool( value )

    def get_Attitude(self):
        return self.Attitude

    def get_AttitudeError(self):
        return self.AttitudeError

    def get_AttitudeValid(self):
        return self.AttitudeValid

    def set_AttitudeValid(self, value):
        self.AttitudeValid = bool( value )

    def get_Location(self):
        return self.Location

    def set_Location(self, value):
        self.Location = value 

    def get_LocationError(self):
        return self.LocationError

    def get_TimeLastSeen(self):
        return self.TimeLastSeen

    def set_TimeLastSeen(self, value):
        self.TimeLastSeen = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From EntityPerception:\n"
        buf +=    "PerceivedEntityID = " + str( self.PerceivedEntityID ) + "\n" 
        buf +=    "PerceiverID = " + str( self.PerceiverID ) + "\n" 
        buf +=    "PerceiverPayloads = " + str( self.PerceiverPayloads ) + "\n" 
        buf +=    "Velocity = " + str( self.Velocity ) + "\n" 
        buf +=    "VelocityError = " + str( self.VelocityError ) + "\n" 
        buf +=    "VelocityValid = " + str( self.VelocityValid ) + "\n" 
        buf +=    "Attitude = " + str( self.Attitude ) + "\n" 
        buf +=    "AttitudeError = " + str( self.AttitudeError ) + "\n" 
        buf +=    "AttitudeValid = " + str( self.AttitudeValid ) + "\n" 
        buf +=    "Location = " + str( self.Location ) + "\n" 
        buf +=    "LocationError = " + str( self.LocationError ) + "\n" 
        buf +=    "TimeLastSeen = " + str( self.TimeLastSeen ) + "\n" 

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
        str = ws + "<EntityPerception>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</EntityPerception>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<PerceivedEntityID>" + str(self.PerceivedEntityID) + "</PerceivedEntityID>\n"
        buf += ws + "<PerceiverID>" + str(self.PerceiverID) + "</PerceiverID>\n"
        buf += ws + "<PerceiverPayloads>\n"
        for x in self.PerceiverPayloads:
            buf += ws + "<uint32>" + str(x) + "</uint32>\n"
        buf += ws + "</PerceiverPayloads>\n"
        buf += ws + "<Velocity>\n"
        for x in self.Velocity:
            buf += ws + "<real32>" + str(x) + "</real32>\n"
        buf += ws + "</Velocity>\n"
        buf += ws + "<VelocityError>\n"
        for x in self.VelocityError:
            buf += ws + "<real32>" + str(x) + "</real32>\n"
        buf += ws + "</VelocityError>\n"
        buf += ws + "<VelocityValid>" + str(self.VelocityValid) + "</VelocityValid>\n"
        buf += ws + "<Attitude>\n"
        for x in self.Attitude:
            buf += ws + "<real32>" + str(x) + "</real32>\n"
        buf += ws + "</Attitude>\n"
        buf += ws + "<AttitudeError>\n"
        for x in self.AttitudeError:
            buf += ws + "<real32>" + str(x) + "</real32>\n"
        buf += ws + "</AttitudeError>\n"
        buf += ws + "<AttitudeValid>" + str(self.AttitudeValid) + "</AttitudeValid>\n"
        buf += ws + "<Location>\n"
        if self.Location == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.Location.toXMLStr(ws + "    ") 
        buf += ws + "</Location>\n"
        buf += ws + "<LocationError>\n"
        for x in self.LocationError:
            buf += ws + "<real32>" + str(x) + "</real32>\n"
        buf += ws + "</LocationError>\n"
        buf += ws + "<TimeLastSeen>" + str(self.TimeLastSeen) + "</TimeLastSeen>\n"

        return buf
        
