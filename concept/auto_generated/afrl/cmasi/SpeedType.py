#! /usr/bin/python

class SpeedType:

    Airspeed = 0
    Groundspeed = 1



def get_SpeedType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "Airspeed": return SpeedType.Airspeed
    if str == "Groundspeed": return SpeedType.Groundspeed


def get_SpeedType_int(val):
    """
    Returns a string representation from an int
    """
    if val == SpeedType.Airspeed: return "Airspeed"
    if val == SpeedType.Groundspeed: return "Groundspeed"
    return SpeedType.Airspeed


