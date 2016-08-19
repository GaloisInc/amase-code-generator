#! /usr/bin/python

class TurnType:

    TurnShort = 0
    FlyOver = 1



def get_TurnType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "TurnShort": return TurnType.TurnShort
    if str == "FlyOver": return TurnType.FlyOver


def get_TurnType_int(val):
    """
    Returns a string representation from an int
    """
    if val == TurnType.TurnShort: return "TurnShort"
    if val == TurnType.FlyOver: return "FlyOver"
    return TurnType.TurnShort


