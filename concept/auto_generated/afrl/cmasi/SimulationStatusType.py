#! /usr/bin/python

class SimulationStatusType:

    Stopped = 0
    Running = 1
    Paused = 2
    Reset = 3



def get_SimulationStatusType_str(str):
    """
    Returns a numerical value from a string
    """
    if str == "Stopped": return SimulationStatusType.Stopped
    if str == "Running": return SimulationStatusType.Running
    if str == "Paused": return SimulationStatusType.Paused
    if str == "Reset": return SimulationStatusType.Reset


def get_SimulationStatusType_int(val):
    """
    Returns a string representation from an int
    """
    if val == SimulationStatusType.Stopped: return "Stopped"
    if val == SimulationStatusType.Running: return "Running"
    if val == SimulationStatusType.Paused: return "Paused"
    if val == SimulationStatusType.Reset: return "Reset"
    return SimulationStatusType.Stopped


