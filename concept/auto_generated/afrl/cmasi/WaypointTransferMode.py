#! /usr/bin/python

class WaypointTransferMode:

    RequestWaypoints = 0
    AddWaypoints = 1
    ClearWaypoints = 2
    ReportWaypoints = 3



def get_WaypointTransferMode_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "RequestWaypoints": return WaypointTransferMode.RequestWaypoints
    if str == "AddWaypoints": return WaypointTransferMode.AddWaypoints
    if str == "ClearWaypoints": return WaypointTransferMode.ClearWaypoints
    if str == "ReportWaypoints": return WaypointTransferMode.ReportWaypoints


def get_WaypointTransferMode_int(val):
    """
    Returns a string representation from an int
    """
    if val == WaypointTransferMode.RequestWaypoints: return "RequestWaypoints"
    if val == WaypointTransferMode.AddWaypoints: return "AddWaypoints"
    if val == WaypointTransferMode.ClearWaypoints: return "ClearWaypoints"
    if val == WaypointTransferMode.ReportWaypoints: return "ReportWaypoints"
    return WaypointTransferMode.RequestWaypoints


