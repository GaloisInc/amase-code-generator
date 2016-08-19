#! /usr/bin/python

class ZoneAvoidanceType:

    Physical = 1
    Regulatory = 2
    Acoustic = 3
    Threat = 4
    Visual = 5



def get_ZoneAvoidanceType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "Physical": return ZoneAvoidanceType.Physical
    if str == "Regulatory": return ZoneAvoidanceType.Regulatory
    if str == "Acoustic": return ZoneAvoidanceType.Acoustic
    if str == "Threat": return ZoneAvoidanceType.Threat
    if str == "Visual": return ZoneAvoidanceType.Visual


def get_ZoneAvoidanceType_int(val):
    """
    Returns a string representation from an int
    """
    if val == ZoneAvoidanceType.Physical: return "Physical"
    if val == ZoneAvoidanceType.Regulatory: return "Regulatory"
    if val == ZoneAvoidanceType.Acoustic: return "Acoustic"
    if val == ZoneAvoidanceType.Threat: return "Threat"
    if val == ZoneAvoidanceType.Visual: return "Visual"
    return ZoneAvoidanceType.Physical


