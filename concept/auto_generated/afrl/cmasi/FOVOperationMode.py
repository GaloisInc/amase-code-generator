#! /usr/bin/python

class FOVOperationMode:

    Continuous = 0
    Discrete = 1



def get_FOVOperationMode_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "Continuous": return FOVOperationMode.Continuous
    if str == "Discrete": return FOVOperationMode.Discrete


def get_FOVOperationMode_int(val):
    """
    Returns a string representation from an int
    """
    if val == FOVOperationMode.Continuous: return "Continuous"
    if val == FOVOperationMode.Discrete: return "Discrete"
    return FOVOperationMode.Continuous


