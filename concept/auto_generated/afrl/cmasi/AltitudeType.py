#! /usr/bin/python

class AltitudeType:

    AGL = 0
    MSL = 1



def get_AltitudeType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "AGL": return AltitudeType.AGL
    if str == "MSL": return AltitudeType.MSL


def get_AltitudeType_int(val):
    """
    Returns a string representation from an int
    """
    if val == AltitudeType.AGL: return "AGL"
    if val == AltitudeType.MSL: return "MSL"
    return AltitudeType.AGL


