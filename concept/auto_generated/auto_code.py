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

    if "P" == "M":
        ctrl_input["P_1_Loiter_0_0"] = UAVs[0].Loiter

    if "P" == "P":

        if "P_1_Loiter_0_0" in current_plays:
            ctrl_input["P_1_Loiter_0_0"] = 1

        else:
            ctrl_input["P_1_Loiter_0_0"] = 0

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
        ctrl_input["P_1_ST_2_B"] = UAVs[0].ST

    if "P" == "P":

        if "P_1_ST_2_B" in current_plays:
            ctrl_input["P_1_ST_2_B"] = 1

        else:
            ctrl_input["P_1_ST_2_B"] = 0
    return ctrl_input

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

        ctrl_input_args = get_args(M1.move)

        current_plays = ["P_1_ST_2_A", "P_2_Loiter_0_0"]

        ctrl_input = prepare_ctrl_input(UAVs,ctrl_input_args,current_plays)

        output = M1.move(**ctrl_input)

finally:
    print("closing socket")
    sock.close()
