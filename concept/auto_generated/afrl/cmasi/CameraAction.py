#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadAction


class CameraAction(PayloadAction.PayloadAction):

    def __init__(self):
        PayloadAction.PayloadAction.__init__(self)
        self.LMCP_TYPE = 18
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.HorizontalFieldOfView = 0   #real32
        self.AssociatedActions = []   #PayloadAction


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(PayloadAction.PayloadAction.pack(self))
        buffer.append(struct.pack(">f", self.HorizontalFieldOfView))
        buffer.append(struct.pack(">H", len(self.AssociatedActions) ))
        for x in self.AssociatedActions:
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
        _pos = PayloadAction.PayloadAction.unpack(self, buffer, _pos)
        self.HorizontalFieldOfView = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.AssociatedActions = [None] * _arraylen
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
                self.AssociatedActions[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.AssociatedActions[x].unpack(buffer, _pos)
            else:
                self.AssociatedActions[x] = None
        return _pos


    def get_HorizontalFieldOfView(self):
        return self.HorizontalFieldOfView

    def set_HorizontalFieldOfView(self, value):
        self.HorizontalFieldOfView = float( value )

    def get_AssociatedActions(self):
        return self.AssociatedActions



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = PayloadAction.PayloadAction.toString(self)
        buf += "From CameraAction:\n"
        buf +=    "HorizontalFieldOfView = " + str( self.HorizontalFieldOfView ) + "\n" 
        buf +=    "AssociatedActions = " + str( self.AssociatedActions ) + "\n" 

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
        str = ws + "<CameraAction>\n";
        #str +=PayloadAction.PayloadAction.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</CameraAction>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += PayloadAction.PayloadAction.toXMLMembersStr(self, ws)
        buf += ws + "<HorizontalFieldOfView>" + str(self.HorizontalFieldOfView) + "</HorizontalFieldOfView>\n"
        buf += ws + "<AssociatedActions>\n"
        for x in self.AssociatedActions:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</AssociatedActions>\n"

        return buf
        
