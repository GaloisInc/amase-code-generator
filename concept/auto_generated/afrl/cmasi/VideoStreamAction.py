#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import VehicleAction


class VideoStreamAction(VehicleAction.VehicleAction):

    def __init__(self):
        VehicleAction.VehicleAction.__init__(self)
        self.LMCP_TYPE = 48
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.VideoStreamID = 0   #int32
        self.ActiveSensor = 0   #int32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(VehicleAction.VehicleAction.pack(self))
        buffer.append(struct.pack(">i", self.VideoStreamID))
        buffer.append(struct.pack(">i", self.ActiveSensor))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = VehicleAction.VehicleAction.unpack(self, buffer, _pos)
        self.VideoStreamID = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        self.ActiveSensor = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_VideoStreamID(self):
        return self.VideoStreamID

    def set_VideoStreamID(self, value):
        self.VideoStreamID = int( value )

    def get_ActiveSensor(self):
        return self.ActiveSensor

    def set_ActiveSensor(self, value):
        self.ActiveSensor = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = VehicleAction.VehicleAction.toString(self)
        buf += "From VideoStreamAction:\n"
        buf +=    "VideoStreamID = " + str( self.VideoStreamID ) + "\n" 
        buf +=    "ActiveSensor = " + str( self.ActiveSensor ) + "\n" 

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
        str = ws + "<VideoStreamAction>\n";
        #str +=VehicleAction.VehicleAction.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</VideoStreamAction>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += VehicleAction.VehicleAction.toXMLMembersStr(self, ws)
        buf += ws + "<VideoStreamID>" + str(self.VideoStreamID) + "</VideoStreamID>\n"
        buf += ws + "<ActiveSensor>" + str(self.ActiveSensor) + "</ActiveSensor>\n"

        return buf
        
