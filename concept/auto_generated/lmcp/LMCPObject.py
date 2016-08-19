
class LMCPObject:

    SERIES_NAME = ""
    LMCP_TYPE = 0

    def pack(self):
        return []

    def unpack(self, buffer, _pos):
        return _pos

    def toString(self):
        return ""

    def toXML(self):
        return self.toXMLStr("");

    def toXMLStr(self, ws):
        return ""
    
    def toXMLMembersStr(self, ws):
        """
        Returns an XML String of all of the members.  Does not include open and closing object
        name.  This should be used by toXML() to get inherited members.
        """
        return ""

    def unpackFromXMLNode(self, el, seriesFactory):
        """
        Extracts members from a DOM Element.  Expects a minidom Element (e) and a
        SeriesFactory object
        """
        return
