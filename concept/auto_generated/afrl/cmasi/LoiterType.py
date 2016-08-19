#! /usr/bin/python

class LoiterType:

    VehicleDefault = 0
    Circular = 1
    Racetrack = 2
    FigureEight = 3
    Hover = 4



def get_LoiterType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "VehicleDefault": return LoiterType.VehicleDefault
    if str == "Circular": return LoiterType.Circular
    if str == "Racetrack": return LoiterType.Racetrack
    if str == "FigureEight": return LoiterType.FigureEight
    if str == "Hover": return LoiterType.Hover


def get_LoiterType_int(val):
    """
    Returns a string representation from an int
    """
    if val == LoiterType.VehicleDefault: return "VehicleDefault"
    if val == LoiterType.Circular: return "Circular"
    if val == LoiterType.Racetrack: return "Racetrack"
    if val == LoiterType.FigureEight: return "FigureEight"
    if val == LoiterType.Hover: return "Hover"
    return LoiterType.VehicleDefault


