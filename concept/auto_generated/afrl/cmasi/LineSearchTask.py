#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import SearchTask
from afrl.cmasi import Location3D
from afrl.cmasi import Wedge


class LineSearchTask(SearchTask.SearchTask):

    def __init__(self):
        SearchTask.SearchTask.__init__(self)
        self.LMCP_TYPE = 31
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.PointList = []   #Location3D
        self.ViewAngleList = []   #Wedge
        self.UseInertialViewAngles = False   #bool


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(SearchTask.SearchTask.pack(self))
        buffer.append(struct.pack(">H", len(self.PointList) ))
        for x in self.PointList:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">H", len(self.ViewAngleList) ))
        for x in self.ViewAngleList:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">B", self.UseInertialViewAngles))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = SearchTask.SearchTask.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.PointList = [None] * _arraylen
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
                self.PointList[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.PointList[x].unpack(buffer, _pos)
            else:
                self.PointList[x] = None
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
        self.UseInertialViewAngles = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        return _pos


    def get_PointList(self):
        return self.PointList

    def get_ViewAngleList(self):
        return self.ViewAngleList

    def get_UseInertialViewAngles(self):
        return self.UseInertialViewAngles

    def set_UseInertialViewAngles(self, value):
        self.UseInertialViewAngles = bool( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = SearchTask.SearchTask.toString(self)
        buf += "From LineSearchTask:\n"
        buf +=    "PointList = " + str( self.PointList ) + "\n" 
        buf +=    "ViewAngleList = " + str( self.ViewAngleList ) + "\n" 
        buf +=    "UseInertialViewAngles = " + str( self.UseInertialViewAngles ) + "\n" 

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
        str = ws + "<LineSearchTask>\n";
        #str +=SearchTask.SearchTask.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</LineSearchTask>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += SearchTask.SearchTask.toXMLMembersStr(self, ws)
        buf += ws + "<PointList>\n"
        for x in self.PointList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</PointList>\n"
        buf += ws + "<ViewAngleList>\n"
        for x in self.ViewAngleList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</ViewAngleList>\n"
        buf += ws + "<UseInertialViewAngles>" + str(self.UseInertialViewAngles) + "</UseInertialViewAngles>\n"

        return buf
        
