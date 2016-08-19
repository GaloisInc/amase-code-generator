#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import SearchTask
from afrl.cmasi import AbstractGeometry
from afrl.cmasi import Wedge


class AreaSearchTask(SearchTask.SearchTask):

    def __init__(self):
        SearchTask.SearchTask.__init__(self)
        self.LMCP_TYPE = 17
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.SearchArea = AbstractGeometry.AbstractGeometry()   #AbstractGeometry
        self.ViewAngleList = []   #Wedge


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(SearchTask.SearchTask.pack(self))
        buffer.append(struct.pack("B", self.SearchArea != None ))
        if self.SearchArea != None:
            buffer.append(struct.pack(">q", self.SearchArea.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.SearchArea.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.SearchArea.SERIES_VERSION))
            buffer.append(self.SearchArea.pack())
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
            self.SearchArea = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.SearchArea.unpack(buffer, _pos)
        else:
            self.SearchArea = None
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


    def get_SearchArea(self):
        return self.SearchArea

    def set_SearchArea(self, value):
        self.SearchArea = value 

    def get_ViewAngleList(self):
        return self.ViewAngleList



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = SearchTask.SearchTask.toString(self)
        buf += "From AreaSearchTask:\n"
        buf +=    "SearchArea = " + str( self.SearchArea ) + "\n" 
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
        str = ws + "<AreaSearchTask>\n";
        #str +=SearchTask.SearchTask.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</AreaSearchTask>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += SearchTask.SearchTask.toXMLMembersStr(self, ws)
        buf += ws + "<SearchArea>\n"
        if self.SearchArea == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.SearchArea.toXMLStr(ws + "    ") 
        buf += ws + "</SearchArea>\n"
        buf += ws + "<ViewAngleList>\n"
        for x in self.ViewAngleList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</ViewAngleList>\n"

        return buf
        
