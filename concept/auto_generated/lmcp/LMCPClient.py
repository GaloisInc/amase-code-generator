import socket
from lmcp import LMCPFactory

from afrl.cmasi import AbstractGeometry
from afrl.cmasi import KeyValuePair
from afrl.cmasi import Location3D
from afrl.cmasi import PayloadAction
from afrl.cmasi import PayloadConfiguration
from afrl.cmasi import PayloadState
from afrl.cmasi import VehicleAction
from afrl.cmasi import Task
from afrl.cmasi import SearchTask
from afrl.cmasi import AbstractZone
from afrl.cmasi import EntityConfiguration
from afrl.cmasi import FlightProfile
from afrl.cmasi import AirVehicleConfiguration
from afrl.cmasi import EntityState
from afrl.cmasi import AirVehicleState
from afrl.cmasi import Wedge
from afrl.cmasi import AreaSearchTask
from afrl.cmasi import CameraAction
from afrl.cmasi import CameraConfiguration
from afrl.cmasi import GimballedPayloadState
from afrl.cmasi import CameraState
from afrl.cmasi import Circle
from afrl.cmasi import GimbalAngleAction
from afrl.cmasi import GimbalConfiguration
from afrl.cmasi import GimbalScanAction
from afrl.cmasi import GimbalStareAction
from afrl.cmasi import GimbalState
from afrl.cmasi import GoToWaypointAction
from afrl.cmasi import KeepInZone
from afrl.cmasi import KeepOutZone
from afrl.cmasi import LineSearchTask
from afrl.cmasi import NavigationAction
from afrl.cmasi import LoiterAction
from afrl.cmasi import LoiterTask
from afrl.cmasi import Waypoint
from afrl.cmasi import MissionCommand
from afrl.cmasi import MustFlyTask
from afrl.cmasi import OperatorSignal
from afrl.cmasi import OperatingRegion
from afrl.cmasi import AutomationRequest
from afrl.cmasi import PointSearchTask
from afrl.cmasi import Polygon
from afrl.cmasi import Rectangle
from afrl.cmasi import RemoveTasks
from afrl.cmasi import ServiceStatus
from afrl.cmasi import SessionStatus
from afrl.cmasi import VehicleActionCommand
from afrl.cmasi import VideoStreamAction
from afrl.cmasi import VideoStreamConfiguration
from afrl.cmasi import VideoStreamState
from afrl.cmasi import AutomationResponse
from afrl.cmasi import RemoveZones
from afrl.cmasi import RemoveEntities
from afrl.cmasi import FlightDirectorAction
from afrl.cmasi import WeatherReport
from afrl.cmasi import FollowPathCommand
from afrl.cmasi import PathWaypoint
from afrl.cmasi import StopMovementAction
from afrl.cmasi import WaypointTransfer
from afrl.cmasi import PayloadStowAction
from afrl.cmasi.perceive import EntityPerception
from afrl.cmasi.perceive import TrackEntityAction
from afrl.cmasi.perceive import TrackEntityTask


s = socket.socket()
host = socket.gethostname()
port = 11041
s.connect((host, port))
buf = []

#Pack AbstractGeometry
obj = AbstractGeometry.AbstractGeometry()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack KeyValuePair
obj = KeyValuePair.KeyValuePair()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack Location3D
obj = Location3D.Location3D()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack PayloadAction
obj = PayloadAction.PayloadAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack PayloadConfiguration
obj = PayloadConfiguration.PayloadConfiguration()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack PayloadState
obj = PayloadState.PayloadState()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack VehicleAction
obj = VehicleAction.VehicleAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack Task
obj = Task.Task()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack SearchTask
obj = SearchTask.SearchTask()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack AbstractZone
obj = AbstractZone.AbstractZone()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack EntityConfiguration
obj = EntityConfiguration.EntityConfiguration()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack FlightProfile
obj = FlightProfile.FlightProfile()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack AirVehicleConfiguration
obj = AirVehicleConfiguration.AirVehicleConfiguration()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack EntityState
obj = EntityState.EntityState()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack AirVehicleState
obj = AirVehicleState.AirVehicleState()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack Wedge
obj = Wedge.Wedge()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack AreaSearchTask
obj = AreaSearchTask.AreaSearchTask()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack CameraAction
obj = CameraAction.CameraAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack CameraConfiguration
obj = CameraConfiguration.CameraConfiguration()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack GimballedPayloadState
obj = GimballedPayloadState.GimballedPayloadState()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack CameraState
obj = CameraState.CameraState()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack Circle
obj = Circle.Circle()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack GimbalAngleAction
obj = GimbalAngleAction.GimbalAngleAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack GimbalConfiguration
obj = GimbalConfiguration.GimbalConfiguration()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack GimbalScanAction
obj = GimbalScanAction.GimbalScanAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack GimbalStareAction
obj = GimbalStareAction.GimbalStareAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack GimbalState
obj = GimbalState.GimbalState()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack GoToWaypointAction
obj = GoToWaypointAction.GoToWaypointAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack KeepInZone
obj = KeepInZone.KeepInZone()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack KeepOutZone
obj = KeepOutZone.KeepOutZone()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack LineSearchTask
obj = LineSearchTask.LineSearchTask()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack NavigationAction
obj = NavigationAction.NavigationAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack LoiterAction
obj = LoiterAction.LoiterAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack LoiterTask
obj = LoiterTask.LoiterTask()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack Waypoint
obj = Waypoint.Waypoint()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack MissionCommand
obj = MissionCommand.MissionCommand()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack MustFlyTask
obj = MustFlyTask.MustFlyTask()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack OperatorSignal
obj = OperatorSignal.OperatorSignal()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack OperatingRegion
obj = OperatingRegion.OperatingRegion()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack AutomationRequest
obj = AutomationRequest.AutomationRequest()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack PointSearchTask
obj = PointSearchTask.PointSearchTask()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack Polygon
obj = Polygon.Polygon()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack Rectangle
obj = Rectangle.Rectangle()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack RemoveTasks
obj = RemoveTasks.RemoveTasks()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack ServiceStatus
obj = ServiceStatus.ServiceStatus()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack SessionStatus
obj = SessionStatus.SessionStatus()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack VehicleActionCommand
obj = VehicleActionCommand.VehicleActionCommand()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack VideoStreamAction
obj = VideoStreamAction.VideoStreamAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack VideoStreamConfiguration
obj = VideoStreamConfiguration.VideoStreamConfiguration()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack VideoStreamState
obj = VideoStreamState.VideoStreamState()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack AutomationResponse
obj = AutomationResponse.AutomationResponse()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack RemoveZones
obj = RemoveZones.RemoveZones()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack RemoveEntities
obj = RemoveEntities.RemoveEntities()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack FlightDirectorAction
obj = FlightDirectorAction.FlightDirectorAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack WeatherReport
obj = WeatherReport.WeatherReport()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack FollowPathCommand
obj = FollowPathCommand.FollowPathCommand()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack PathWaypoint
obj = PathWaypoint.PathWaypoint()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack StopMovementAction
obj = StopMovementAction.StopMovementAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack WaypointTransfer
obj = WaypointTransfer.WaypointTransfer()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack PayloadStowAction
obj = PayloadStowAction.PayloadStowAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack EntityPerception
obj = EntityPerception.EntityPerception()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack TrackEntityAction
obj = TrackEntityAction.TrackEntityAction()
buf.append(LMCPFactory.packMessage(obj, True))
#Pack TrackEntityTask
obj = TrackEntityTask.TrackEntityTask()
buf.append(LMCPFactory.packMessage(obj, True))


s.send("".join(buf))


