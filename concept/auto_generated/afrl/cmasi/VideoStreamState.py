#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadState


class VideoStreamState(PayloadState.PayloadState):

    def __init__(self):
        PayloadState.PayloadState.__init__(self)
        self.LMCP_TYPE = 50
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.ActiveSensor = 0   #int64


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(PayloadState.PayloadState.pack(self))
        buffer.append(struct.pack(">l", self.ActiveSensor))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = PayloadState.PayloadState.unpack(self, buffer, _pos)
        self.ActiveSensor = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        return _pos


    def get_ActiveSensor(self):
        return self.ActiveSensor

    def set_ActiveSensor(self, value):
        self.ActiveSensor = int( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = PayloadState.PayloadState.toString(self)
        buf += "From VideoStreamState:\n"
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
        str = ws + "<VideoStreamState>\n";
        #str +=PayloadState.PayloadState.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</VideoStreamState>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += PayloadState.PayloadState.toXMLMembersStr(self, ws)
        buf += ws + "<ActiveSensor>" + str(self.ActiveSensor) + "</ActiveSensor>\n"

        return buf
        
