import socket
from geopy.distance import vincenty
from lmcp import LMCPFactory
from afrl.cmasi import EntityState
from afrl.cmasi import AirVehicleState
from afrl.cmasi import AirVehicleConfiguration
from afrl.cmasi.SessionStatus import SessionStatus
from demo_controller import ExampleCtrl
from PyMASE import UAV, Location, get_args
import string

stateMap = dict()
M1 = ExampleCtrl()
configMap = dict()
move_keys = get_args(M1.move)
ctrl_input = {key: 0 for key in move_keys}

def prepare_ctrl_input(UAVs,ctrl_input_args,current_plays):

    ctrl_input = dict(zip(ctrl_input_args, [0]*len(ctrl_input_args)))

    if "B" == "M":
        ctrl_input["B_1_Refuel_0_0"] = UAVs[0].Refuel

    if "B" == "P":

        if "B_1_Refuel_0_0" in current_plays:
            ctrl_input["B_1_Refuel_0_0"] = 1

        else:
            ctrl_input["B_1_Refuel_0_0"] = 0

    if "B" == "M":
        ctrl_input["B_2_Refuel_0_0"] = UAVs[1].Refuel

    if "B" == "P":

        if "B_2_Refuel_0_0" in current_plays:
            ctrl_input["B_2_Refuel_0_0"] = 1

        else:
            ctrl_input["B_2_Refuel_0_0"] = 0

    if "B" == "M":
        ctrl_input["B_2_Loiter_0_0"] = UAVs[1].Loiter

    if "B" == "P":

        if "B_2_Loiter_0_0" in current_plays:
            ctrl_input["B_2_Loiter_0_0"] = 1

        else:
            ctrl_input["B_2_Loiter_0_0"] = 0

    if "M" == "M":
        ctrl_input["M_2_Fuel_0_0"] = UAVs[1].Fuel

    if "M" == "P":

        if "M_2_Fuel_0_0" in current_plays:
            ctrl_input["M_2_Fuel_0_0"] = 1

        else:
            ctrl_input["M_2_Fuel_0_0"] = 0

    if "M" == "M":
        ctrl_input["M_1_Found_2_0"] = UAVs[0].Found

    if "M" == "P":

        if "M_1_Found_2_0" in current_plays:
            ctrl_input["M_1_Found_2_0"] = 1

        else:
            ctrl_input["M_1_Found_2_0"] = 0

    if "B" == "M":
        ctrl_input["B_1_Track_2_0"] = UAVs[0].Track

    if "B" == "P":

        if "B_1_Track_2_0" in current_plays:
            ctrl_input["B_1_Track_2_0"] = 1

        else:
            ctrl_input["B_1_Track_2_0"] = 0

    if "B" == "M":
        ctrl_input["B_1_Loiter_0_0"] = UAVs[0].Loiter

    if "B" == "P":

        if "B_1_Loiter_0_0" in current_plays:
            ctrl_input["B_1_Loiter_0_0"] = 1

        else:
            ctrl_input["B_1_Loiter_0_0"] = 0

    if "M" == "M":
        ctrl_input["M_1_Fuel_0_0"] = UAVs[0].Fuel

    if "M" == "P":

        if "M_1_Fuel_0_0" in current_plays:
            ctrl_input["M_1_Fuel_0_0"] = 1

        else:
            ctrl_input["M_1_Fuel_0_0"] = 0

    if "B" == "M":
        ctrl_input["B_1_Search_0_1"] = UAVs[0].Search

    if "B" == "P":

        if "B_1_Search_0_1" in current_plays:
            ctrl_input["B_1_Search_0_1"] = 1

        else:
            ctrl_input["B_1_Search_0_1"] = 0

    if "B" == "M":
        ctrl_input["B_1_Search_0_0"] = UAVs[0].Search

    if "B" == "P":

        if "B_1_Search_0_0" in current_plays:
            ctrl_input["B_1_Search_0_0"] = 1

        else:
            ctrl_input["B_1_Search_0_0"] = 0

    if "P" == "M":
        ctrl_input["P_1_ST_2_B"] = UAVs[0].ST

    if "P" == "P":

        if "P_1_ST_2_B" in current_plays:
            ctrl_input["P_1_ST_2_B"] = 1

        else:
            ctrl_input["P_1_ST_2_B"] = 0

    if "P" == "M":
        ctrl_input["P_2_Loiter_0_0"] = UAVs[1].Loiter

    if "P" == "P":

        if "P_2_Loiter_0_0" in current_plays:
            ctrl_input["P_2_Loiter_0_0"] = 1

        else:
            ctrl_input["P_2_Loiter_0_0"] = 0

    if "P" == "M":
        ctrl_input["P_1_ST_2_A"] = UAVs[0].ST

    if "P" == "P":

        if "P_1_ST_2_A" in current_plays:
            ctrl_input["P_1_ST_2_A"] = 1

        else:
            ctrl_input["P_1_ST_2_A"] = 0

    if "P" == "M":
        ctrl_input["P_1_Loiter_0_0"] = UAVs[0].Loiter

    if "P" == "P":

        if "P_1_Loiter_0_0" in current_plays:
            ctrl_input["P_1_Loiter_0_0"] = 1

        else:
            ctrl_input["P_1_Loiter_0_0"] = 0
    return ctrl_input

def Refuel(uav,uav2,loc):
    uav.refuel(locations[0])

def Loiter(uav,uav2,loc):
    uav.loiter(locations[uav.id-1])

def Fuel_monitor(uav,uav2,loc):
    fuel = uav.get_energy()
    if fuel <= 90 and fuel != 0:
        uav.Fuel = 1
    elif fuel > 90:
        uav.Fuel = 0
    return uav

def Found_monitor(uav,uav2,loc):
    dist = vincenty((uav.getit("latitude",uav.id),uav.getit("longitude",uav.id))\
    ,(uav.getit("latitude",uav2+1),uav.getit("longitude",uav2+1))).meters
    if dist < 600 and dist != 0:
        uav.Found = 1
    else:
        uav.Found = 0
    return uav

def Track(uav,uav2,loc):
    return 0

def Search(uav,uav2,loc):
    return 0

def message_received(obj):
    global stateMap
    global configMap
    if isinstance(obj ,AirVehicleConfiguration.AirVehicleConfiguration):
        configMap[obj.get_ID()] = obj
    elif isinstance(obj, AirVehicleState.AirVehicleState): 
        stateMap[obj.get_ID()] = obj
    elif isinstance(obj, SessionStatus):
        ss = obj

def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 5555)
    print("connecting to %s port %s") % (server_address)
    sock.connect(server_address)
    print("connected")
    return sock

sock = connect()
msg = LMCPFactory.LMCPFactory()

uav_n = 3
loc_n = 3
UAVs = []

for i in range(0,uav_n):
    UAVs.append(UAV(i+1,sock,stateMap))

locations = []
lon = [2.0, 2.05, 1.978]
lat = [1.0, 1.05, 1.04]
height = [1000.0, 4000.0, 5000.0]
width = [2000.0, 3000.0, 5000.0]

for i in range(0,loc_n):
    locations.append(Location(lat[i],lon[i],height[i],width[i],string.ascii_uppercase[i]))

flag = 0
while flag != 1:
    flag = 1
    message = msg.getObject(sock.recv(2224))
    message_received(message)
    for i in range(0,uav_n):
        UAVs[i].stateMap = stateMap
        if UAVs[i].stateMap.get(UAVs[i].id) is None:
            flag = 0
try:
    while True:

        message = msg.getObject(sock.recv(2224))

        message_received(message)
        for i in range(0,uav_n):
            UAVs[i].stateMap = stateMap

        UAVs[1] = Fuel_monitor(UAVs[1],0,0)

        UAVs[0] = Found_monitor(UAVs[0],2,0)

        UAVs[0] = Fuel_monitor(UAVs[0],0,0)

        ctrl_input_args = get_args(M1.move)

        current_plays = ["P_1_ST_2_A", "P_2_Loiter_0_0"]

        ctrl_input = prepare_ctrl_input(UAVs,ctrl_input_args,current_plays)

        output = M1.move(**ctrl_input)

        if output["B_1_Refuel_0_0"] == 1:
            Refuel(UAVs[0],0,locations[0])

        if output["B_2_Refuel_0_0"] == 1:
            Refuel(UAVs[1],0,locations[0])

        if output["B_2_Loiter_0_0"] == 1:
            Loiter(UAVs[1],0,locations[0])

        if output["B_1_Track_2_0"] == 1:
            Track(UAVs[0],2,locations[0])

        if output["B_1_Loiter_0_0"] == 1:
            Loiter(UAVs[0],0,locations[0])

        if output["B_1_Search_0_1"] == 1:
            Search(UAVs[0],0,locations[1])

        if output["B_1_Search_0_0"] == 1:
            Search(UAVs[0],0,locations[0])

finally:
    print("closing socket")
    sock.close()
