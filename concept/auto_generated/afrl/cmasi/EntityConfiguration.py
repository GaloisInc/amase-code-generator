#! /usr/bin/python

import struct
from lmcp import LMCPObject
#import xml.dom.minidom

#from lmcp import *
from afrl.cmasi import PayloadConfiguration
from afrl.cmasi import KeyValuePair


class EntityConfiguration(LMCPObject.LMCPObject):

    def __init__(self):

        self.LMCP_TYPE = 11
        self.SERIES_NAME = "CMASI"
        #Series Name turned into a long for quick comparisons.
        self.SERIES_NAME_ID = 4849604199710720000
        self.SERIES_VERSION = 3

        #Define message fields
        self.ID = 0   #int64
        self.Affiliation = "Unknown"   #string
        self.EntityType = ""   #string
        self.Label = ""   #string
        self.NominalSpeed = 0   #real32
        self.PayloadConfigurationList = []   #PayloadConfiguration
        self.Info = []   #KeyValuePair


    def pack(self):
        """
        Packs the object data and returns a string that contains all of the serialized
        members.
        """
        buffer = []
        buffer.extend(LMCPObject.LMCPObject.pack(self))
        buffer.append(struct.pack(">l", self.ID))
        buffer.append(struct.pack(">H", len(self.Affiliation) ))
        if len(self.Affiliation) > 0:
            buffer.append(struct.pack( `len(self.Affiliation)` + "s", self.Affiliation))
        buffer.append(struct.pack(">H", len(self.EntityType) ))
        if len(self.EntityType) > 0:
            buffer.append(struct.pack( `len(self.EntityType)` + "s", self.EntityType))
        buffer.append(struct.pack(">H", len(self.Label) ))
        if len(self.Label) > 0:
            buffer.append(struct.pack( `len(self.Label)` + "s", self.Label))
        buffer.append(struct.pack(">f", self.NominalSpeed))
        buffer.append(struct.pack(">H", len(self.PayloadConfigurationList) ))
        for x in self.PayloadConfigurationList:
           buffer.append(struct.pack("B", x != None ))
           if x != None:
               buffer.append(struct.pack(">q", x.SERIES_NAME_ID))
               buffer.append(struct.pack(">I", x.LMCP_TYPE))
               buffer.append(struct.pack(">H", x.SERIES_VERSION))
               buffer.append(x.pack())
        buffer.append(struct.pack(">H", len(self.Info) ))
        for x in self.Info:
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
        _pos = LMCPObject.LMCPObject.unpack(self, buffer, _pos)
        self.ID = struct.unpack_from(">l", buffer, _pos)[0]
        _pos += 8
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.Affiliation = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.Affiliation = ""
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.EntityType = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.EntityType = ""
        _strlen = struct.unpack_from(">H", buffer, _pos )[0]
        _pos += 2
        if _strlen > 0:
            self.Label = struct.unpack_from( `_strlen` + "s", buffer, _pos )[0]
            _pos += _strlen
        else:
             self.Label = ""
        self.NominalSpeed = struct.unpack_from(">f", buffer, _pos)[0]
        _pos += 4
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        _arraylen = struct.unpack_from(">H", buffer, _pos )[0]
        self.PayloadConfigurationList = [None] * _arraylen
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
                self.PayloadConfigurationList[x] = LMCPFactory.LMCPFactory().createObject(_series, _version, _type )
                _pos = self.PayloadConfigurationList[x].unpack(buffer, _pos)
            else:
                self.PayloadConfigurationList[x] = None
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
        return _pos


    def get_ID(self):
        return self.ID

    def set_ID(self, value):
        self.ID = int( value )

    def get_Affiliation(self):
        return self.Affiliation

    def set_Affiliation(self, value):
        self.Affiliation = str( value )

    def get_EntityType(self):
        return self.EntityType

    def set_EntityType(self, value):
        self.EntityType = str( value )

    def get_Label(self):
        return self.Label

    def set_Label(self, value):
        self.Label = str( value )

    def get_NominalSpeed(self):
        return self.NominalSpeed

    def set_NominalSpeed(self, value):
        self.NominalSpeed = float( value )

    def get_PayloadConfigurationList(self):
        return self.PayloadConfigurationList

    def get_Info(self):
        return self.Info



    def toString(self):
        """
        Returns a string representation of all variables
        """
        buf = LMCPObject.LMCPObject.toString(self)
        buf += "From EntityConfiguration:\n"
        buf +=    "ID = " + str( self.ID ) + "\n" 
        buf +=    "Affiliation = " + str( self.Affiliation ) + "\n" 
        buf +=    "EntityType = " + str( self.EntityType ) + "\n" 
        buf +=    "Label = " + str( self.Label ) + "\n" 
        buf +=    "NominalSpeed = " + str( self.NominalSpeed ) + "\n" 
        buf +=    "PayloadConfigurationList = " + str( self.PayloadConfigurationList ) + "\n" 
        buf +=    "Info = " + str( self.Info ) + "\n" 

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
        str = ws + "<EntityConfiguration>\n";
        #str +=LMCPObject.LMCPObject.toXMLMembersStr(self, ws + "  ")
        str += self.toXMLMembersStr(ws + "  ")
        str += ws + "</EntityConfiguration>\n";
        return str

    def toXMLMembersStr(self, ws):
        buf = ""
        buf += LMCPObject.LMCPObject.toXMLMembersStr(self, ws)
        buf += ws + "<ID>" + str(self.ID) + "</ID>\n"
        buf += ws + "<Affiliation>" + str(self.Affiliation) + "</Affiliation>\n"
        buf += ws + "<EntityType>" + str(self.EntityType) + "</EntityType>\n"
        buf += ws + "<Label>" + str(self.Label) + "</Label>\n"
        buf += ws + "<NominalSpeed>" + str(self.NominalSpeed) + "</NominalSpeed>\n"
        buf += ws + "<PayloadConfigurationList>\n"
        for x in self.PayloadConfigurationList:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</PayloadConfigurationList>\n"
        buf += ws + "<Info>\n"
        for x in self.Info:
            if x == None:
                buf += ws + "    <null/>\n"
            else:
                buf += x.toXMLStr(ws + "    ") 
        buf += ws + "</Info>\n"

        return buf
        
