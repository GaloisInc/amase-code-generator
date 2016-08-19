#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Task
from afrl.cmasi import WavelengthBand


class TrackEntityTask(Task.Task):

    def __init__(self):
        Task.Task.__init__(self)
        self.LMCP_TYPE = 3
        self.SERIES_NAME = "PERCEIVE"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 5784119745305990725
        self.SERIES_VERSION = 1

        #Define message fields
        self.EntityID = 0   #uint32
        self.SensorModality = WavelengthBand.WavelengthBand.AllAny   #WavelengthBand
        self.GroundSampleDistance = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(Task.Task.pack(self))
        buffer.append(struct.pack(">I", self.EntityID))
        buffer.append(struct.pack(">i", self.SensorModality))
        buffer.append(struct.pack(">f", self.GroundSampleDistance))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = Task.Task.unpack(self, buffer, _pos)
        self.EntityID = struct.unpack_from(">I", buffer, _pos)[0]
        _pos += 4
        self.SensorModality = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.GroundSampleDistance = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_EntityID(self):
        return self.EntityID

    def set_EntityID(self, value):
        self.EntityID = int( value )

    def get_SensorModality(self):
        return self.SensorModality

    def set_SensorModality(self, value):
        self.SensorModality = value 

    def get_GroundSampleDistance(self):
        return self.GroundSampleDistance

    def set_GroundSampleDistance(self, value):
        self.GroundSampleDistance = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = Task.Task.toString(self)
        buf += "From TrackEntityTask:\n"
        buf +=    "EntityID = " + str( self.EntityID ) + "\n" 
        buf +=    "SensorModality = " + str( self.SensorModality ) + "\n" 
        buf +=    "GroundSampleDistance = " + str( self.GroundSampleDistance ) + "\n" 

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
        str = ws + "<TrackEntityTask>\n";
        #str +=Task.Task.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</TrackEntityTask>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += Task.Task.toXMLMembersStr(self, ws)
        buf += ws + "<EntityID>" + str(self.EntityID) + "</EntityID>\n"
        buf += ws + "<SensorModality>" + WavelengthBand.get_WavelengthBand_int(self.SensorModality) + "</SensorModality>\n"
        buf += ws + "<GroundSampleDistance>" + str(self.GroundSampleDistance) + "</GroundSampleDistance>\n"

        return buf
        
