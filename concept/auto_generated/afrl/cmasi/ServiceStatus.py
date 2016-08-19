#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import KeyValuePair
from afrl.cmasi import ServiceStatusType


class ServiceStatus(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 45
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.PercentComplete = 0   #real32
        self.Info = []   #KeyValuePair
        self.StatusType = ServiceStatusType.ServiceStatusType.Information   #ServiceStatusType


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">f", self.PercentComplete))
        buffer.append(struct.pack(">H", len(self.Info) ))
        for x in self.Info:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">i", self.StatusType))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.PercentComplete = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.Info = [None] * _arraylen
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
                self.Info[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.Info[x].unpack(buffer, _pos)
            else:
                self.Info[x] = None
        self.StatusType = struct.unpack_from(">i", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_PercentComplete(self):
        return self.PercentComplete

    def set_PercentComplete(self, value):
        self.PercentComplete = float( value )

    def get_Info(self):
        return self.Info

    def get_StatusType(self):
        return self.StatusType

    def set_StatusType(self, value):
        self.StatusType = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From ServiceStatus:\n"
        buf +=    "PercentComplete = " + str( self.PercentComplete ) + "\n" 
        buf +=    "Info = " + str( self.Info ) + "\n" 
        buf +=    "StatusType = " + str( self.StatusType ) + "\n" 

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
        str = ws + "<ServiceStatus>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</ServiceStatus>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<PercentComplete>" + str(self.PercentComplete) + "</PercentComplete>\n"
        buf += ws + "<Info>\n"
        for x in self.Info:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Info>\n"
        buf += ws + "<StatusType>" + ServiceStatusType.get_ServiceStatusType_int(self.StatusType) + "</StatusType>\n"

        return buf
        
