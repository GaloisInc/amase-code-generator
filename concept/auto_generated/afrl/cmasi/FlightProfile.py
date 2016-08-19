#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *


class FlightProfile(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 12
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.Name = ""   #string
        self.Airspeed = 0   #real32
        self.PitchAngle = 0   #real32
        self.VerticalSpeed = 0   #real32
        self.MaxBankAngle = 0   #real32
        self.EnergyRate = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">H", len(self.Name) ))
        if len(self.Name) > 0:
            buffer.append(struct.pack( `len(self.Name)` + "s", self.Name))
        buffer.append(struct.pack(">f", self.Airspeed))
        buffer.append(struct.pack(">f", self.PitchAngle))
        buffer.append(struct.pack(">f", self.VerticalSpeed))
        buffer.append(struct.pack(">f", self.MaxBankAngle))
        buffer.append(struct.pack(">f", self.EnergyRate))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.Name = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.Name = ""
        self.Airspeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.PitchAngle = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.VerticalSpeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.MaxBankAngle = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        self.EnergyRate = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_Name(self):
        return self.Name

    def set_Name(self, value):
        self.Name = str( value )

    def get_Airspeed(self):
        return self.Airspeed

    def set_Airspeed(self, value):
        self.Airspeed = float( value )

    def get_PitchAngle(self):
        return self.PitchAngle

    def set_PitchAngle(self, value):
        self.PitchAngle = float( value )

    def get_VerticalSpeed(self):
        return self.VerticalSpeed

    def set_VerticalSpeed(self, value):
        self.VerticalSpeed = float( value )

    def get_MaxBankAngle(self):
        return self.MaxBankAngle

    def set_MaxBankAngle(self, value):
        self.MaxBankAngle = float( value )

    def get_EnergyRate(self):
        return self.EnergyRate

    def set_EnergyRate(self, value):
        self.EnergyRate = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From FlightProfile:\n"
        buf +=    "Name = " + str( self.Name ) + "\n" 
        buf +=    "Airspeed = " + str( self.Airspeed ) + "\n" 
        buf +=    "PitchAngle = " + str( self.PitchAngle ) + "\n" 
        buf +=    "VerticalSpeed = " + str( self.VerticalSpeed ) + "\n" 
        buf +=    "MaxBankAngle = " + str( self.MaxBankAngle ) + "\n" 
        buf +=    "EnergyRate = " + str( self.EnergyRate ) + "\n" 

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
        str = ws + "<FlightProfile>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</FlightProfile>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<Name>" + str(self.Name) + "</Name>\n"
        buf += ws + "<Airspeed>" + str(self.Airspeed) + "</Airspeed>\n"
        buf += ws + "<PitchAngle>" + str(self.PitchAngle) + "</PitchAngle>\n"
        buf += ws + "<VerticalSpeed>" + str(self.VerticalSpeed) + "</VerticalSpeed>\n"
        buf += ws + "<MaxBankAngle>" + str(self.MaxBankAngle) + "</MaxBankAngle>\n"
        buf += ws + "<EnergyRate>" + str(self.EnergyRate) + "</EnergyRate>\n"

        return buf
        
