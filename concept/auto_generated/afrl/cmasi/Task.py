#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import KeyValuePair


class Task(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 8
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.TaskID = 0   #int64
        self.Label = ""   #string
        self.EligibleEntities = []   #int64
        self.RevisitRate = 0   #real32
        self.Parameters = []   #KeyValuePair
        self.Priority = 0   #byte
        self.Required = True   #bool


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">l", self.TaskID))
        buffer.append(struct.pack(">H", len(self.Label) ))
        if len(self.Label) > 0:
            buffer.append(struct.pack( `len(self.Label)` + "s", self.Label))
        buffer.append(struct.pack(">H", len(self.EligibleEntities) ))
        for x in self.EligibleEntities:
            buffer.append(struct.pack(">l", x ))
        buffer.append(struct.pack(">f", self.RevisitRate))
        buffer.append(struct.pack(">H", len(self.Parameters) ))
        for x in self.Parameters:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">B", self.Priority))
        buffer.append(struct.pack(">B", self.Required))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.TaskID = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.Label = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.Label = ""
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.EligibleEntities = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.EligibleEntities = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        self.RevisitRate = struct.unpack_from(">f", buffer, _pos)[0]
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
        self.Priority = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        self.Required = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        return _pos


    def get_TaskID(self):
        return self.TaskID

    def set_TaskID(self, value):
        self.TaskID = int( value )

    def get_Label(self):
        return self.Label

    def set_Label(self, value):
        self.Label = str( value )

    def get_EligibleEntities(self):
        return self.EligibleEntities

    def get_RevisitRate(self):
        return self.RevisitRate

    def set_RevisitRate(self, value):
        self.RevisitRate = float( value )

    def get_Parameters(self):
        return self.Parameters

    def get_Priority(self):
        return self.Priority

    def set_Priority(self, value):
        self.Priority = int( value )

    def get_Required(self):
        return self.Required

    def set_Required(self, value):
        self.Required = bool( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From Task:\n"
        buf +=    "TaskID = " + str( self.TaskID ) + "\n" 
        buf +=    "Label = " + str( self.Label ) + "\n" 
        buf +=    "EligibleEntities = " + str( self.EligibleEntities ) + "\n" 
        buf +=    "RevisitRate = " + str( self.RevisitRate ) + "\n" 
        buf +=    "Parameters = " + str( self.Parameters ) + "\n" 
        buf +=    "Priority = " + str( self.Priority ) + "\n" 
        buf +=    "Required = " + str( self.Required ) + "\n" 

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
        str = ws + "<Task>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</Task>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<TaskID>" + str(self.TaskID) + "</TaskID>\n"
        buf += ws + "<Label>" + str(self.Label) + "</Label>\n"
        buf += ws + "<EligibleEntities>\n"
        for x in self.EligibleEntities:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</EligibleEntities>\n"
        buf += ws + "<RevisitRate>" + str(self.RevisitRate) + "</RevisitRate>\n"
        buf += ws + "<Parameters>\n"
        for x in self.Parameters:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Parameters>\n"
        buf += ws + "<Priority>" + str(self.Priority) + "</Priority>\n"
        buf += ws + "<Required>" + str(self.Required) + "</Required>\n"

        return buf
        
