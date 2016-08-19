#! /usr/bin/python

class LoiterDirection:

    VehicleDefault = 0
    CounterClockwise = 1
    Clockwise = 2



def get_LoiterDirection_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "VehicleDefault": return LoiterDirection.VehicleDefault
    if str == "CounterClockwise": return LoiterDirection.CounterClockwise
    if str == "Clockwise": return LoiterDirection.Clockwise


def get_LoiterDirection_int(val):
    """
    Returns a string representation from an int
    """
    if val == LoiterDirection.VehicleDefault: return "VehicleDefault"
    if val == LoiterDirection.CounterClockwise: return "CounterClockwise"
    if val == LoiterDirection.Clockwise: return "Clockwise"
    return LoiterDirection.VehicleDefault


