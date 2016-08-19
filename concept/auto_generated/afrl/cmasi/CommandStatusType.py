#! /usr/bin/python

class CommandStatusType:

    Pending = 0
    Approved = 1
    InProcess = 2
    Executed = 3
    Cancelled = 4



def get_CommandStatusType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "Pending": return CommandStatusType.Pending
    if str == "Approved": return CommandStatusType.Approved
    if str == "InProcess": return CommandStatusType.InProcess
    if str == "Executed": return CommandStatusType.Executed
    if str == "Cancelled": return CommandStatusType.Cancelled


def get_CommandStatusType_int(val):
    """
    Returns a string representation from an int
    """
    if val == CommandStatusType.Pending: return "Pending"
    if val == CommandStatusType.Approved: return "Approved"
    if val == CommandStatusType.InProcess: return "InProcess"
    if val == CommandStatusType.Executed: return "Executed"
    if val == CommandStatusType.Cancelled: return "Cancelled"
    return CommandStatusType.Pending


