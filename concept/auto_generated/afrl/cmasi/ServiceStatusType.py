#! /usr/bin/python

class ServiceStatusType:

    Information = 0
    Warning = 1
    Error = 2



def get_ServiceStatusType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "Information": return ServiceStatusType.Information
    if str == "Warning": return ServiceStatusType.Warning
    if str == "Error": return ServiceStatusType.Error


def get_ServiceStatusType_int(val):
    """
    Returns a string representation from an int
    """
    if val == ServiceStatusType.Information: return "Information"
    if val == ServiceStatusType.Warning: return "Warning"
    if val == ServiceStatusType.Error: return "Error"
    return ServiceStatusType.Information


