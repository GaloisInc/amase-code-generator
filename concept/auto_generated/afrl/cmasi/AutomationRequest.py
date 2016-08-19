#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *


class AutomationRequest(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 40
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.EntityList = []   #int64
        self.TaskList = []   #int64
        self.TaskRelationships = ""   #string
        self.OperatingRegion = 0   #int64
        self.RedoAllTasks = False   #bool


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">H", len(self.EntityList) ))
        for x in self.EntityList:
            buffer.append(struct.pack(">l", x ))
        buffer.append(struct.pack(">H", len(self.TaskList) ))
        for x in self.TaskList:
            buffer.append(struct.pack(">l", x ))
        buffer.append(struct.pack(">H", len(self.TaskRelationships) ))
        if len(self.TaskRelationships) > 0:
            buffer.append(struct.pack( `len(self.TaskRelationships)` + "s", self.TaskRelationships))
        buffer.append(struct.pack(">l", self.OperatingRegion))
        buffer.append(struct.pack(">B", self.RedoAllTasks))

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.EntityList = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.EntityList = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.TaskList = [None] * _arraylen
        _pos += 2
        if _arraylen > 0:
            self.TaskList = struct.unpack_from(">" + `_arraylen` + "l", buffer, _pos )
            _pos += 8 * _arraylen
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.TaskRelationships = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.TaskRelationships = ""
        self.OperatingRegion = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        self.RedoAllTasks = struct.unpack_from(">B", buffer, _pos)[0]
        _pos += 1
        return _pos


    def get_EntityList(self):
        return self.EntityList

    def get_TaskList(self):
        return self.TaskList

    def get_TaskRelationships(self):
        return self.TaskRelationships

    def set_TaskRelationships(self, value):
        self.TaskRelationships = str( value )

    def get_OperatingRegion(self):
        return self.OperatingRegion

    def set_OperatingRegion(self, value):
        self.OperatingRegion = int( value )

    def get_RedoAllTasks(self):
        return self.RedoAllTasks

    def set_RedoAllTasks(self, value):
        self.RedoAllTasks = bool( value )



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From AutomationRequest:\n"
        buf +=    "EntityList = " + str( self.EntityList ) + "\n" 
        buf +=    "TaskList = " + str( self.TaskList ) + "\n" 
        buf +=    "TaskRelationships = " + str( self.TaskRelationships ) + "\n" 
        buf +=    "OperatingRegion = " + str( self.OperatingRegion ) + "\n" 
        buf +=    "RedoAllTasks = " + str( self.RedoAllTasks ) + "\n" 

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
        str = ws + "<AutomationRequest>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</AutomationRequest>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<EntityList>\n"
        for x in self.EntityList:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</EntityList>\n"
        buf += ws + "<TaskList>\n"
        for x in self.TaskList:
            buf += ws + "<int64>" + str(x) + "</int64>\n"
        buf += ws + "</TaskList>\n"
        buf += ws + "<TaskRelationships>" + str(self.TaskRelationships) + "</TaskRelationships>\n"
        buf += ws + "<OperatingRegion>" + str(self.OperatingRegion) + "</OperatingRegion>\n"
        buf += ws + "<RedoAllTasks>" + str(self.RedoAllTasks) + "</RedoAllTasks>\n"

        return buf
        
