from lmcp.LMCPObject import *

import EntityPerception
import TrackEntityAction
import TrackEntityTask


SERIES_NAME = "PERCEIVE"
#Series Name turned into a long for quick comparisons.
SERIES_NAME_ID = 5784119745305990725
SERIES_VERSION = 1


class SeriesEnum:

    def getName(self, type):
        if(type ==  1): return "EntityPerception"
        if(type ==  2): return "TrackEntityAction"
        if(type ==  3): return "TrackEntityTask"


    def getType(self, name):
        if ( name == "EntityPerception"): return 1
        if ( name == "TrackEntityAction"): return 2
        if ( name == "TrackEntityTask"): return 3

        return -1

    def getInstance(self, type):
        if(type ==  1): return EntityPerception.EntityPerception()
        if(type ==  2): return TrackEntityAction.TrackEntityAction()
        if(type ==  3): return TrackEntityTask.TrackEntityTask()

        return None
