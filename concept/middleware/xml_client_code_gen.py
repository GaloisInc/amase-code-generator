import os
import subprocess
import inspect
import shutil
import sys
import datetime

import xml.dom.minidom as MD


# XML Helpers #################################################################

def make_node(doc, tag, attrs={}, children=[]):
    node = doc.createElement(tag)

    for key in attrs:
        node.setAttribute(key, attrs[key])

    for child in children:
        node.childNodes.append(child)

    return node


# Scenario Specification ######################################################

class Scenario(object):
    __slots__ = [ 'locs', 'uavs', 'name', 'duration' ]

    @staticmethod
    def parse(file):
        """Parse the spec file, and produce a scenario"""
        locs = []
        uavs = []

        with open(file, 'r') as f:
            for x in f:
                x = x.split()
                if len(x[0]) > 2:

                    if x[0] == 'uav':
                        uavs.append(UAV(int(x[1]), float(x[2]), float(x[3])))
                        continue

                    if x[0] == 'loc':
                        locs.append(Location(int(x[1]), float(x[2]),
                            float(x[3]), float(x[4]), float(x[5])))
                        continue

                    if x[0] == 'cmd':
                        play = Play.make(x[1:])
                        uavs[play.uav - 1].addPlay(play)
                        continue

                    print ('Unknown command: %s' % x[0])

        return Scenario('Test Scenario', locs, uavs)


    def __init__(self, name, locs, uavs):
        self.name = name
        self.locs = locs
        self.uavs = uavs
        self.duration = 60000

    def dependencies(self):
        """Produce the behavior and monitor dependencies for this scenario"""
        behaviors = set()
        monitors  = set()

        for uav in self.uavs:
            behaviors = behaviors.union(uav.behaviors())
            monitors  = monitors.union(uav.monitors())

        return (behaviors, monitors)

    def genXML(self):
        doc = MD.Document()

        root = doc.createElement('AMASE')
        root.childNodes.append(self.genScenarioData(doc))
        root.childNodes.append(self.genEventList(doc))
        doc.childNodes.append(root)

        return doc

    def genScenarioData(self, doc):
        maplat = sum([ loc.lat for loc in self.locs ])/float(len(self.locs))
        maplon = sum([ loc.lon for loc in self.locs ])/float(len(self.locs))
        now    = datetime.datetime.now()

        return make_node(doc, 'ScenarioData', {}, [
            make_node(doc, 'SimulationView', {
                'LongExtend': '0.7',
                'Latitude': str(maplat),
                'Longitude': str(maplon),
                }, []),
            make_node(doc, 'ScenarioName', {}, [
                doc.createTextNode(self.name),
                ]),
            make_node(doc, 'Date', {}, [
                doc.createTextNode('%d/%d/%d:%d:%d:%d' % (now.day,now.month,now.year,
                        now.hour,now.minute,now.second)),
                ]),
            make_node(doc, 'Duration', {}, [
                doc.createTextNode(str(self.duration)),
                ]),
            ])

    def genEventList(self, doc):
        return make_node(doc, 'ScenarioEventList', {},
                map(lambda uav: uav.genXML(doc), self.uavs))


# Locations ###################################################################

class Location(object):
    def __init__(self, num, lat, lon, width, height):
        self.num    = num
        self.lat    = lat
        self.lon    = lon
        self.width  = width
        self.height = height

    def __str__(self):
        return ('L_%d_%d_%d_%d' % (self.lat, self.lon, self.width, self.height))


# UAVs ########################################################################

class UAV(object):
    def __init__(self, num, lat, lon):
        self.num   = num
        self.lat   = lat
        self.lon   = lon
        self.plays = []

    def addPlay(self, play):
        self.plays.append(play)

    def __str__(self):
        return '<UAV ' + str(self.num) + ' ' \
                + str(self.lat) + ' ' \
                + str(self.lon) + '>'

    def behaviors(self):
        # start as just the contingency behavior
        deps = set([RefuelBehavior(self.num, 0, 0)])

        # add in behaviors required for each play
        for play in self.plays:
            deps = deps.union(play.behaviors())

        return deps

    def monitors(self):
        """The set of monitors that this UAV requires"""
        # each uav requires the fuel monitor for its refueling contingency
        # behavior
        deps = set([FuelMonitor(self.num)])

        for play in self.plays:
            deps = deps.union(play.monitors())

        return deps

    def genXML(self,doc):
        return make_node(doc, 'AirVehicleConfiguration', {
                'Time': '0.0',
                'Series': 'CMASI',
            }, [
                make_node(doc, 'ID', {}, [
                    doc.createTextNode(str(self.num)),
                    ]),
            ])


# Monitors ####################################################################

class Monitor(object):
    pass

class FuelMonitor(Monitor):
    def __init__(self, uav):
        self.uav = uav

    def __str__(self):
        return ('M_%d_Fuel_0_0' % self.uav)

class FoundMonitor(Monitor):
    def __init__(self, uav, target):
        self.uav = uav
        self.target = target

    def __str__(self):
        return ('M_%d_Found_%d_0' % (self.uav, self.target))


# Behaviors ###################################################################

class Behavior(object):
    def __init__(self, uav, uav2, loc):
        self.uav  = int(uav)
        self.uav2 = int(uav2)
        self.loc  = int(loc)

    def __eq__(self, other):
        return self.uav == other.uav \
                and self.uav2 == other.uav2 \
                and self.loc  == other.loc

    def __hash__(self):
        return hash((self.uav, self.uav2, self.loc))

class RefuelBehavior(Behavior):
    """The Refuel behavior"""

    def __str__(self):
        return ('B_%d_Refuel_%d_%d' % (self.uav, self.uav2, self.loc))

class LoiterBehavior(Behavior):
    """The Loiter behavior """

    def __str__(self):
        return ('B_%d_Loiter_%d_%d' % (self.uav, self.uav2, self.loc))

class SearchBehavior(Behavior):
    """The Search behavior"""

    def __str__(self):
        return ('B_%d_Search_%d_%d' % (self.uav, self.uav2, self.loc))

class TrackBehavior(Behavior):
    """The Track behavior"""

    def __str__(self):
        return ('B_%d_Track_%d_%d' % (self.uav, self.uav2, self.loc))


# Plays #######################################################################

class Play(object):
    @staticmethod
    def make(descr):
        if descr[2] == 'Loiter':
            return LoiterPlay(descr[1], descr[3])

        elif descr[2] == 'ST':
            return STPlay(descr[1], descr[3], descr[4])

        else:
            raise RuntimeError('Invalid play: ' + descr[2])

    def behaviors(self):
        return set()

    def monitors(self):
        return set()

class STPlay(Play):
    """Search and track for the spescified uav, in the region provided.  """

    def __init__(self, uav, target, loc):
        self.uav    = int(uav)
        self.target = int(target)
        self.loc    = loc

    def __str__(self):
        return ('P_%s_ST_%s_%s' % (self.uav, self.target, self.loc))

    def behaviors(self):
        return set([
                SearchBehavior(self.uav, self.target, self.loc),
                TrackBehavior(self.uav, self.target, self.loc)])

    def monitors(self):
        return set([
            FoundMonitor(self.uav, self.target)])

class LoiterPlay(Play):
    """The Loiter play"""

    def __init__(self, uav, loc):
        self.uav = int(uav)
        self.loc = int(loc)

    def __str__(self):
        return ('P_%s_Loiter_0_0' % self.uav)

    def behaviors(self):
        return set([
                LoiterBehavior(self.uav, 0, self.loc)])


# Code-gen Support ############################################################

def tokenize(string):
    keys = ['Type','UAV','Definition','Aux_UAV','Aux_Loc']
    return dict(zip(keys,string.split('_')))

def stringify(lst):
    s = "_"
    return s.join(lst)

def get_args(func):
    args = inspect.getargspec(func).args
    args = [arg for arg in args if arg != 'self']
    return args

def make_xml(n_uav,uav_lat,uav_lon,n_loc,loc_lat,loc_lon,width,height):

    maplat = sum(uav_lat)/float(len(uav_lat))
    maplon = sum(uav_lon)/float(len(uav_lon))

    xmlscript = ('<?xml version="1.0" ?>\n'
    '<AMASE>\n'
      '<ScenarioData>\n'
        '<SimulationView LongExtent=".07" Latitude="{lat}" Longitude="{lon}"/>\n'
        '<ScenarioName>Test Scenario</ScenarioName>\n'
        '<Date>24/04/2008:00:00:00</Date>\n'
        '<ScenarioDuration>60000</ScenarioDuration>\n'
      '</ScenarioData>\n'
      '<ScenarioEventList>\n').format(lat = maplat, lon = maplon)

    for i in range(0,n_uav):

        xmlscript += ('<AirVehicleConfiguration Time="0.0" Series="CMASI">\n'
          '<ID>{id}</ID>\n'
          '<Label>UAV{id}</Label>\n'
          '<MinimumSpeed>15.0</MinimumSpeed>\n'
          '<MaximumSpeed>35.0</MaximumSpeed>\n'
          '<NominalFlightProfile>\n'
           ' <FlightProfile Series="CMASI">\n'
            '  <Name>Cruise</Name>\n'
             ' <Airspeed>20.0</Airspeed>\n'
              '<PitchAngle>0.0</PitchAngle>\n'
              '<VerticalSpeed>0.0</VerticalSpeed>\n'
              '<MaxBankAngle>30.0</MaxBankAngle>\n'
              '<EnergyRate>0.005</EnergyRate>\n'
            '</FlightProfile>\n'
          '</NominalFlightProfile>\n'
          '<AlternateFlightProfiles>\n'
            '<FlightProfile Series="CMASI">\n'
              '<Name>Climb</Name>\n'
              '<Airspeed>15.0</Airspeed>\n'
              '<PitchAngle>10.0</PitchAngle>\n'
              '<VerticalSpeed>5.0</VerticalSpeed>\n'
              '<MaxBankAngle>30.0</MaxBankAngle>\n'
              '<EnergyRate>0.01</EnergyRate>\n'
            '</FlightProfile>\n'
            '<FlightProfile Series="CMASI">\n'
              '<Name>Descent</Name>\n'
              '<Airspeed>25.0</Airspeed>\n'
              '<PitchAngle>-5.0</PitchAngle>\n'
              '<VerticalSpeed>-5.0</VerticalSpeed>\n'
              '<MaxBankAngle>30.0</MaxBankAngle>\n'
              '<EnergyRate>0.005</EnergyRate>\n'
            '</FlightProfile>\n'
            '<FlightProfile Series="CMASI">\n'
              '<Name>Loiter</Name>\n'
              '<Airspeed>20.0</Airspeed>\n'
              '<PitchAngle>5.0</PitchAngle>\n'
              '<VerticalSpeed>0.0</VerticalSpeed>\n'
              '<MaxBankAngle>30.0</MaxBankAngle>\n'
              '<EnergyRate>0.005</EnergyRate>\n'
            '</FlightProfile>\n'
            '<FlightProfile Series="CMASI">\n'
              '<Name>Dash</Name>\n'
              '<Airspeed>35.0</Airspeed>\n'
              '<PitchAngle>-2.0</PitchAngle>\n'
              '<VerticalSpeed>0.0</VerticalSpeed>\n'
              '<MaxBankAngle>30.0</MaxBankAngle>\n'
              '<EnergyRate>0.01</EnergyRate>\n'
            '</FlightProfile>\n'
          '</AlternateFlightProfiles>\n'
          '<AvailableTurnTypes>\n'
            '<TurnType>TurnShort</TurnType>\n'
            '<TurnType>FlyOver</TurnType>\n'
          '</AvailableTurnTypes>\n'
          '<MinimumAltitude>0.0</MinimumAltitude>\n'
          '<MaximumAltitude>1000000.0</MaximumAltitude>\n'
          '<MinAltAboveGround>0.0</MinAltAboveGround>\n'
        '</AirVehicleConfiguration>\n'
        '<AirVehicleState Time="0.0" Series="CMASI">\n'
          '<ID>{id}</ID>\n'
          '<Location>\n'
            '<Location3D Series="CMASI">\n'
              '<Altitude>50.0</Altitude>\n'
              '<Latitude>{lat}</Latitude>\n'
              '<Longitude>{lon}</Longitude>\n'
            '</Location3D>\n'
          '</Location>\n'
          '<u>0.0</u>\n'
          '<v>0.0</v>\n'
          '<w>0.0</w>\n'
          '<udot>0.0</udot>\n'
          '<vdot>0.0</vdot>\n'
          '<wdot>0.0</wdot>\n'
          '<Heading>90.0</Heading>\n'
          '<Pitch>0.0</Pitch>\n'
          '<Roll>0.0</Roll>\n'
          '<p>0.0</p>\n'
          '<q>0.0</q>\n'
          '<r>0.0</r>\n'
          '<Airspeed>0.0</Airspeed>\n'
          '<VerticalSpeed>0.0</VerticalSpeed>\n'
          '<ActualEnergyRate>0.00008</ActualEnergyRate>\n'
          '<EnergyAvailable>100.0</EnergyAvailable>\n'
          '<WindSpeed>0.0</WindSpeed>\n'
          '<WindDirection>0.0</WindDirection>\n'
          '<GroundSpeed>0.0</GroundSpeed>\n'
          '<GroundTrack>0.0</GroundTrack>\n'
          '<CurrentWaypoint>0</CurrentWaypoint>\n'
          '<CurrentCommand>0</CurrentCommand>\n'
          '<Mode>Waypoint</Mode>\n'
          '<AssociatedTasks/>\n'
          '<Time>0</Time>\n'
        '</AirVehicleState>\n').format(id=i+1,lat=uav_lat[i],lon=uav_lon[i])

    for i in range(0,n_loc):

        xmlscript +=('<AreaSearchTask Series="CMASI">\n'
          '<SearchArea>\n'
        '<Rectangle Series="CMASI">\n'
          '<CenterPoint>\n'
            '<Location3D Series="CMASI">\n'
              '<Latitude>{lat}</Latitude>\n'
             ' <Longitude>{lon}</Longitude>\n'
            '</Location3D>\n'
          '</CenterPoint>\n'
          '<Width>{width}</Width>\n'
          '<Height>{height}</Height>\n'
          '<Rotation>0.0</Rotation>\n'
        '</Rectangle>\n'
      '</SearchArea>\n'
        '<ViewAngleList/>\n'
        '<DesiredWavelengthBands/>\n'
        '<DwellTime>0</DwellTime>\n'
        '<GroundSampleDistance>0.0</GroundSampleDistance>\n'
        '<TaskID>{taskid}</TaskID>\n'
        '<Label/>\n'
        '<RevisitRate>0.0</RevisitRate>\n'
        '<Parameters/>\n'
        '<Priority>0</Priority>\n'
        '<Required>false</Required>\n'
      '</AreaSearchTask>\n').format(lat=loc_lat[i],lon=loc_lon[i],width=width[i]\
      ,height=height[i],taskid = 10 + i)

    xmlscript +=('</ScenarioEventList>\n'
      '</AMASE>\n').format()

    text_file = open("../auto_generated/auto_code.xml", "w+")
    text_file.write("%s" % xmlscript)
    text_file.close()


def make_script(n_uav, n_loc, height, width, loc_lon, loc_lat,ctrl_input):

    output = csynth.move(**ctrl_input)
    ctrl_in = [key for key in ctrl_input.keys() if ctrl_input[key] == 1] 
    output = [key for key in output.keys() if output[key] == 1]
    output_input = output + ctrl_in
    log = []

    script = (
        'import socket{sep}'
        'from geopy.distance import vincenty{sep}'
        'from lmcp import LMCPFactory{sep}'
        'from afrl.cmasi import EntityState{sep}'
        'from afrl.cmasi import AirVehicleState{sep}'
        'from afrl.cmasi import AirVehicleConfiguration{sep}'
        'from afrl.cmasi.SessionStatus import SessionStatus{sep}'
        'from demo_controller import ExampleCtrl{sep}'
        'from PyMASE import UAV, Location, get_args{sep}'
        'import string{sep}'
        '{sep}stateMap = dict(){sep}'
        'M1 = ExampleCtrl(){sep}'
        'configMap = dict(){sep}'
        'move_keys = get_args(M1.move){sep}'
        'ctrl_input = {{key: 0 for key in move_keys}}{sep}').format(sep='\n', ind='    ') 
    
    script += (
        '{sep}def prepare_ctrl_input(UAVs,ctrl_input_args,current_plays):{sep}'
        '{sep}{ind}ctrl_input = dict(zip(ctrl_input_args, [0]*len(ctrl_input_args))){sep}')\
    .format(sep='\n', ind='    ') 

    for string in output_input:

        token = tokenize(string)
        script += ('{sep}{ind}if "{key_type}" == "M":{sep}'
                '{ind}{ind}ctrl_input["{key}"] = UAVs[{idl}].{key_def}{sep}'
                '{sep}{ind}if "{key_type}" == "P":{sep}'
                '{sep}{ind}{ind}if "{key}" in current_plays:{sep}'
                '{ind}{ind}{ind}ctrl_input["{key}"] = 1{sep}'
                '{sep}{ind}{ind}else:{sep}'
                '{ind}{ind}{ind}ctrl_input["{key}"] = 0{sep}'
                '').format(sep='\n', ind='    ', key=string, key_def=token["Definition"]
                , key_type=token["Type"],idl=str(int(token["UAV"])-1)) 

    script += (
        '{ind}return ctrl_input{sep}').format(sep='\n', ind='    ') 

    for string in output:

        token = tokenize(string)

        if token["Type"] == 'M':          

            if token["Type"]+token["Definition"] not in log:

                log.append(token["Type"]+token["Definition"])

                if token["Definition"] == "Fuel":

                    script += (
                    '{sep}def {monitor}_monitor(uav,uav2,loc):{sep}'
                    '{ind}fuel = uav.get_energy(){sep}'
                    '{ind}if fuel <= 90 and fuel != 0:{sep}'
                    '{ind}{ind}uav.Fuel = 1{sep}'
                    '{ind}elif fuel > 90:{sep}'
                    '{ind}{ind}uav.Fuel = 0{sep}'
                    '{ind}return uav{sep}'
                    ).format(sep='\n', ind='    ', id=token["UAV"], monitor = token["Definition"]\
                    , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc']) 


                elif token["Definition"] == "Found":

                    script += (
                    '{sep}def {monitor}_monitor(uav,uav2,loc):{sep}'
                    '{ind}dist = vincenty((uav.getit("latitude",uav.id),uav.getit("longitude",uav.id))\{sep}'+
                    '{ind},(uav.getit("latitude",uav2+1),uav.getit("longitude",uav2+1))).meters{sep}'
                    '{ind}if dist < 600 and dist != 0:{sep}'
                    '{ind}{ind}uav.Found = 1{sep}'
                    '{ind}else:{sep}'
                    '{ind}{ind}uav.Found = 0{sep}'
                    '{ind}return uav{sep}'
                    ).format(sep='\n', ind='    ', id=token["UAV"], monitor = token["Definition"]\
                    , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc']) 

                else:

                    script += (
                    '{sep}def {monitor}_monitor(uav,uav2,loc):{sep}'
                    '{ind}return uav{sep}'
                    ).format(sep='\n', ind='    ', id=token["UAV"], monitor = token["Definition"]\
                    , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc'])                    


        if token["Type"] == 'B':

            if token["Type"]+token["Definition"] not in log:

                log.append(token["Type"]+token["Definition"])

                if token["Definition"] == "Refuel":

                    script += (
                    '{sep}def {behaviour}(uav,uav2,loc):{sep}'
                    '{ind}uav.refuel(locations[0]){sep}'
                    ).format(sep='\n', ind='    ', id=token["UAV"], behaviour = token["Definition"]\
                    , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc'])

                elif token["Definition"] == "Loiter":

                    script += (
                    '{sep}def {behaviour}(uav,uav2,loc):{sep}'
                    '{ind}uav.loiter(locations[uav.id-1]){sep}'
                    ).format(sep='\n', ind='    ', id=token["UAV"], behaviour = token["Definition"]\
                    , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc'])

                else:

                    script += (
                    '{sep}def {behaviour}(uav,uav2,loc):{sep}'
                    '{ind}return 0{sep}'
                    ).format(sep='\n', ind='    ', id=token["UAV"], behaviour = token["Definition"]\
                    , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc']) 

    script +=(

        '{sep}def message_received(obj):{sep}'
        '{ind}global stateMap{sep}'
        '{ind}global configMap{sep}'
        '{ind}if isinstance(obj ,AirVehicleConfiguration.AirVehicleConfiguration):{sep}'
        '{ind}{ind}configMap[obj.get_ID()] = obj{sep}'
        '{ind}elif isinstance(obj, AirVehicleState.AirVehicleState): {sep}'
        '{ind}{ind}stateMap[obj.get_ID()] = obj{sep}'
        '{ind}elif isinstance(obj, SessionStatus):{sep}'
        '{ind}{ind}ss = obj{sep}'

        '{sep}def connect():{sep}'
        '{ind}sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM){sep}'
        '{ind}server_address = ("localhost", 5555){sep}'
        '{ind}print("connecting to %s port %s") % (server_address){sep}'
        '{ind}sock.connect(server_address){sep}'
        '{ind}print("connected"){sep}'
        '{ind}return sock{sep}'

        '{sep}sock = connect(){sep}'
        'msg = LMCPFactory.LMCPFactory(){sep}'

        '{sep}uav_n = {uav_n}{sep}'
        'loc_n = {loc_n}{sep}'
        'UAVs = []{sep}'

        '{sep}for i in range(0,uav_n):{sep}'
        '{ind}UAVs.append(UAV(i+1,sock,stateMap)){sep}'
        
        '{sep}locations = []{sep}'
        'lon = {lons}{sep}'
        'lat = {lats}{sep}'
        'height = {heights}{sep}'
        'width = {widths}{sep}'

        '{sep}for i in range(0,loc_n):{sep}'
        '{ind}locations.append(Location(lat[i],lon[i],height[i],width[i],string.ascii_uppercase[i])){sep}'

        '{sep}flag = 0'
        '{sep}while flag != 1:'
        '{sep}{ind}flag = 1'
        '{sep}{ind}message = msg.getObject(sock.recv(2224))'
        '{sep}{ind}message_received(message)'
        '{sep}{ind}for i in range(0,uav_n):'
        '{sep}{ind}{ind}UAVs[i].stateMap = stateMap'
        '{sep}{ind}{ind}if UAVs[i].stateMap.get(UAVs[i].id) is None:'
        '{sep}{ind}{ind}{ind}flag = 0'

        '{sep}try:{sep}'
        '{ind}while True:{sep}'

        '{sep}{ind}{ind}message = msg.getObject(sock.recv(2224)){sep}'

        '{sep}{ind}{ind}message_received(message){sep}'
        '{ind}{ind}for i in range(0,uav_n):{sep}'        
        '{ind}{ind}{ind}UAVs[i].stateMap = stateMap{sep}'        

        ).format(sep='\n', ind='    ', loc_n = n_loc, uav_n = n_uav, heights = height\
        , lons = loc_lon, lats = loc_lat, widths = width)     


    for string in output:

        token = tokenize(string)

        if token["Type"] == 'M':

            script += (
            '{sep}{ind}{ind}UAVs[{idl}] = {monitor}_monitor(UAVs[{idl}],{aux1},{aux2}){sep}'
            ).format(sep='\n', ind='    ', id=token["UAV"], idl=str(int(token["UAV"])-1)\
            , monitor = token["Definition"]\
            , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc'])      

    script += ('{sep}{ind}{ind}ctrl_input_args = get_args(M1.move){sep}'
        '{sep}{ind}{ind}current_plays = ["P_1_ST_2_A", "P_2_Loiter_0_0"]{sep}'
        '{sep}{ind}{ind}ctrl_input = prepare_ctrl_input(UAVs,ctrl_input_args,current_plays){sep}'
        '{sep}{ind}{ind}output = M1.move(**ctrl_input){sep}'
        ).format(sep='\n',ind='    ')

    for string in output:

        token = tokenize(string)

        if token["Type"] == 'B':

            script += ('{sep}{ind}{ind}if output["B_{id}_{behaviour}_{aux1}_{aux2}"] == 1:'
                    '{sep}{ind}{ind}{ind}{behaviour}(UAVs[{idl}],{aux1},locations[{aux2}]){sep}')\
                    .format(sep='\n', ind='    ', id=token["UAV"], idl=str(int(token["UAV"])-1)\
                    , behaviour = token["Definition"]\
                    , aux1 = token['Aux_UAV'], aux2 = token['Aux_Loc']) 

    script += (
        '{sep}finally:{sep}'
        '{ind}print("closing socket"){sep}'
        '{ind}sock.close(){sep}'
        ).format(sep='\n',ind='    ')

    text_file = open("../auto_generated/auto_code.py", "w+")
    text_file.write("%s" % script)
    text_file.close()


if __name__ == "__main__":

    # TODO: maybe switch the specification format to JSON?
    spec = Scenario.parse('spec.txt')

    # determine which monitors will be required by the scenario
    behaviors, monitors = spec.dependencies()

    print [ str(x) for x in behaviors ]
    print [ str(x) for x in monitors ]

    print spec.genXML().writexml(sys.stdout, '', '  ', '\n')
    print ""

    sys.exit()

    xml_keys    = get_args(make_xml)
    script_keys = get_args(make_script)
    move_keys   = get_args(csynth.move)
    ctrl_input  = {key: 1 if key in output['commands'] else 0 for key in move_keys}
    output['ctrl_input'] = ctrl_input
    xml_input = { key: output[key] for key in xml_keys }
    script_input = { key: output[key] for key in script_keys }
    make_xml(**xml_input)
    make_script(**script_input)

    # TODO: generate the controller from the specification

    # Run salty to generate the final controller
    os.chdir("../salt")
    subprocess.check_output("make", shell=True)
