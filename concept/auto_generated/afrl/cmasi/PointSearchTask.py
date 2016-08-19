#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import SearchTask
from afrl.cmasi import Location3D
from afrl.cmasi import Wedge


class PointSearchTask(SearchTask.SearchTask):

    def __init__(self):
        SearchTask.SearchTask.__init__(self)
        self.LMCP_TYPE = 41
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.SearchLocation = Location3D.Location3D()   #Location3D
        self.StandoffDistance = 0   #real32
        self.ViewAngleList = []   #Wedge


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(SearchTask.SearchTask.pack(self))
        buffer.append(struct.pack("B", self.SearchLocation != None ))
        if self.SearchLocation != None:
            buffer.append(struct.pack(">q", self.SearchLocation.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.SearchLocation.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.SearchLocation.SERIES_VERSION))
            buffer.append(self.SearchLocation.pack())
        buffer.append(struct.pack(">f", self.StandoffDistance))
        buffer.append(struct.pack(">H", len(self.ViewAngleList) ))
        for x in self.ViewAngleList:
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
        _pos = SearchTask.SearchTask.unpack(self, buffer, _pos)
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
            self.SearchLocation = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.SearchLocation.unpack(buffer, _pos)
        else:
            self.SearchLocation = None
        self.StandoffDistance = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.ViewAngleList = [None] * _arraylen
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
                self.ViewAngleList[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.ViewAngleList[x].unpack(buffer, _pos)
            else:
                self.ViewAngleList[x] = None
        return _pos


    def get_SearchLocation(self):
        return self.SearchLocation

    def set_SearchLocation(self, value):
        self.SearchLocation = value 

    def get_StandoffDistance(self):
        return self.StandoffDistance

    def set_StandoffDistance(self, value):
        self.StandoffDistance = float( value )

    def get_ViewAngleList(self):
        return self.ViewAngleList



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = SearchTask.SearchTask.toString(self)
        buf += "From PointSearchTask:\n"
        buf +=    "SearchLocation = " + str( self.SearchLocation ) + "\n" 
        buf +=    "StandoffDistance = " + str( self.StandoffDistance ) + "\n" 
        buf +=    "ViewAngleList = " + str( self.ViewAngleList ) + "\n" 

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
        str = ws + "<PointSearchTask>\n";
        #str +=SearchTask.SearchTask.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</PointSearchTask>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += SearchTask.SearchTask.toXMLMembersStr(self, ws)
        buf += ws + "<SearchLocation>\n"
        if self.SearchLocation == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.SearchLocation.toXMLStr(ws + "    ") 
        buf += ws + "</SearchLocation>\n"
        buf += ws + "<StandoffDistance>" + str(self.StandoffDistance) + "</StandoffDistance>\n"
        buf += ws + "<ViewAngleList>\n"
        for x in self.ViewAngleList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</ViewAngleList>\n"

        return buf
        
