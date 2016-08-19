#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Task
from afrl.cmasi import WavelengthBand


class SearchTask(Task.Task):

    def __init__(self):
        Task.Task.__init__(self)
        self.LMCP_TYPE = 9
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.DesiredWavelengthBands = []   #WavelengthBand
        self.DwellTime = 0   #int64
        self.GroundSampleDistance = 0   #real32


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(Task.Task.pack(self))
        buffer.append(struct.pack(">H", len(self.DesiredWavelengthBands) ))
        for x in self.DesiredWavelengthBands:
            buffer.append(struct.pack(">i", x ))
        buffer.append(struct.pack(">l", self.DwellTime))
        buffer.append(struct.pack(">f", self.GroundSampleDistance))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = Task.Task.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.DesiredWavelengthBands = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.DesiredWavelengthBands = struct.unpack_from(">" + `_arraylen` + "i", buffer, _pos )
            _pos += 4 * _arraylen
        self.DwellTime = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.GroundSampleDistance = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        return _pos


    def get_DesiredWavelengthBands(self):
        return self.DesiredWavelengthBands

    def get_DwellTime(self):
        return self.DwellTime

    def set_DwellTime(self, value):
        self.DwellTime = int( value )

    def get_GroundSampleDistance(self):
        return self.GroundSampleDistance

    def set_GroundSampleDistance(self, value):
        self.GroundSampleDistance = float( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = Task.Task.toString(self)
        buf += "From SearchTask:\n"
        buf +=    "DesiredWavelengthBands = " + str( self.DesiredWavelengthBands ) + "\n" 
        buf +=    "DwellTime = " + str( self.DwellTime ) + "\n" 
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
        str = ws + "<SearchTask>\n";
        #str +=Task.Task.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</SearchTask>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += Task.Task.toXMLMembersStr(self, ws)
        buf += ws + "<DesiredWavelengthBands>\n"
        for x in self.DesiredWavelengthBands:
            buf += ws + "<WavelengthBand>" + WavelengthBand.get_WavelengthBand_int(x) + "</WavelengthBand>\n"
        buf += ws + "</DesiredWavelengthBands>\n"
        buf += ws + "<DwellTime>" + str(self.DwellTime) + "</DwellTime>\n"
        buf += ws + "<GroundSampleDistance>" + str(self.GroundSampleDistance) + "</GroundSampleDistance>\n"

        return buf
        
