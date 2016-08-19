#! /usr/bin/python

class GimbalPointingMode:

    Unknown = 0
    AirVehicleRelativeAngle = 1
    AirVehicleRelativeSlewRate = 2
    LatLonSlaved = 3
    InertialRelativeSlewRate = 4
    Scan = 5
    Stowed = 6



def get_GimbalPointingMode_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "Unknown": return GimbalPointingMode.Unknown
    if str == "AirVehicleRelativeAngle": return GimbalPointingMode.AirVehicleRelativeAngle
    if str == "AirVehicleRelativeSlewRate": return GimbalPointingMode.AirVehicleRelativeSlewRate
    if str == "LatLonSlaved": return GimbalPointingMode.LatLonSlaved
    if str == "InertialRelativeSlewRate": return GimbalPointingMode.InertialRelativeSlewRate
    if str == "Scan": return GimbalPointingMode.Scan
    if str == "Stowed": return GimbalPointingMode.Stowed


def get_GimbalPointingMode_int(val):
    """
    Returns a string representation from an int
    """
    if val == GimbalPointingMode.Unknown: return "Unknown"
    if val == GimbalPointingMode.AirVehicleRelativeAngle: return "AirVehicleRelativeAngle"
    if val == GimbalPointingMode.AirVehicleRelativeSlewRate: return "AirVehicleRelativeSlewRate"
    if val == GimbalPointingMode.LatLonSlaved: return "LatLonSlaved"
    if val == GimbalPointingMode.InertialRelativeSlewRate: return "InertialRelativeSlewRate"
    if val == GimbalPointingMode.Scan: return "Scan"
    if val == GimbalPointingMode.Stowed: return "Stowed"
    return GimbalPointingMode.Unknown


