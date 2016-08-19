#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import Task
from afrl.cmasi import LoiterAction


class LoiterTask(Task.Task):

    def __init__(self):
        Task.Task.__init__(self)
        self.LMCP_TYPE = 34
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.DesiredAction = LoiterAction.LoiterAction()   #LoiterAction


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(Task.Task.pack(self))
        buffer.append(struct.pack("B", self.DesiredAction != None ))
        if self.DesiredAction != None:
            buffer.append(struct.pack(">q", self.DesiredAction.SERIES_NAME_ID))
            buffer.append(struct.pack(">I", self.DesiredAction.LMCP_TYPE))
            buffer.append(struct.pack(">H", self.DesiredAction.SERIES_VERSION))
            buffer.append(self.DesiredAction.pack())

        return "".join(buffer)

    def unpack(self, buffer, _pos):
        """
        Unpacks data from a string buffer and sets class members
        """
        _pos = Task.Task.unpack(self, buffer, _pos)
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
            self.DesiredAction = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
            _pos = self.DesiredAction.unpack(buffer, _pos)
        else:
            self.DesiredAction = None
        return _pos


    def get_DesiredAction(self):
        return self.DesiredAction

    def set_DesiredAction(self, value):
        self.DesiredAction = value 



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = Task.Task.toString(self)
        buf += "From LoiterTask:\n"
        buf +=    "DesiredAction = " + str( self.DesiredAction ) + "\n" 

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
        str = ws + "<LoiterTask>\n";
        #str +=Task.Task.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</LoiterTask>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += Task.Task.toXMLMembersStr(self, ws)
        buf += ws + "<DesiredAction>\n"
        if self.DesiredAction == None:
            buf += ws + "    <null/>\n"
        else:
            buf += ws + self.DesiredAction.toXMLStr(ws + "    ") 
        buf += ws + "</DesiredAction>\n"

        return buf
        
