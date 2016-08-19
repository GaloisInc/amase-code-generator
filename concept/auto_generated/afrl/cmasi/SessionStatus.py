#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import SimulationStatusType
from afrl.cmasi import KeyValuePair


class SessionStatus(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 46
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.State = SimulationStatusType.SimulationStatusType.Stopped   #SimulationStatusType
        self.StartTime = 0   #int64
        self.ScenarioTime = 0   #int64
        self.RealTimeMultiple = 0   #real32
        self.Parameters = []   #KeyValuePair


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">i", self.State))
        buffer.append(struct.pack(">l", self.StartTime))
        buffer.append(struct.pack(">l", self.ScenarioTime))
        buffer.append(struct.pack(">f", self.RealTimeMultiple))
        buffer.append(struct.pack(">H", len(self.Parameters) ))
        for x in self.Parameters:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.State = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.StartTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.ScenarioTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.RealTimeMultiple = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.Parameters = [None] * _arraylen
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
                self.Parameters[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.Parameters[x].unpack(buffer, _pos)
            else:
                self.Parameters[x] = None
        return _pos


    def get_State(self):
        return self.State

    def set_State(self, value):
        self.State = value 

    def get_StartTime(self):
        return self.StartTime

    def set_StartTime(self, value):
        self.StartTime = int( value )

    def get_ScenarioTime(self):
        return self.ScenarioTime

    def set_ScenarioTime(self, value):
        self.ScenarioTime = int( value )

    def get_RealTimeMultiple(self):
        return self.RealTimeMultiple

    def set_RealTimeMultiple(self, value):
        self.RealTimeMultiple = float( value )

    def get_Parameters(self):
        return self.Parameters



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From SessionStatus:\n"
        buf +=    "State = " + str( self.State ) + "\n" 
        buf +=    "StartTime = " + str( self.StartTime ) + "\n" 
        buf +=    "ScenarioTime = " + str( self.ScenarioTime ) + "\n" 
        buf +=    "RealTimeMultiple = " + str( self.RealTimeMultiple ) + "\n" 
        buf +=    "Parameters = " + str( self.Parameters ) + "\n" 

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
        str = ws + "<SessionStatus>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</SessionStatus>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<State>" + SimulationStatusType.get_SimulationStatusType_int(self.State) + "</State>\n"
        buf += ws + "<StartTime>" + str(self.StartTime) + "</StartTime>\n"
        buf += ws + "<ScenarioTime>" + str(self.ScenarioTime) + "</ScenarioTime>\n"
        buf += ws + "<RealTimeMultiple>" + str(self.RealTimeMultiple) + "</RealTimeMultiple>\n"
        buf += ws + "<Parameters>\n"
        for x in self.Parameters:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Parameters>\n"

        return buf
        
