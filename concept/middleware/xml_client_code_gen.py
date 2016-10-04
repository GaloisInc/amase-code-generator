import os
import subprocess
import inspect
import shutil
import sys
import datetime
import itertools

import xml.dom.minidom as MD


# Pretty-printing #############################################################

class Pretty(object):

    __slots__ = [ 'file', 'level' ]

    def __init__(self, file=sys.stdout, level=0):
        self.file = file
        self.level = level

    def indent(self, txt=None):
        return Indent(self, txt)

    def parens(self):
        return Parens(self)

    def write(self, x):
        self.file.write(str(x))

    def writeln(self, x):
        self.file.write(x)
        self.newline()

    def newline(self):
        self.file.write('\n')
        self.file.write(' ' * self.level)

    def sep(self, sep, things):
        if len(things) <= 0:
            return

        self.write(things[0])

        for thing in things[1:]:
            self.write(sep)
            self.write(thing)

    def comment(self, txt):
        self.write('# ')
        self.writeln(txt)

    def define(self, name, *params):
        self.newline()
        self.write('def ')
        self.write(name)

        with self.parens():
            self.sep(', ', params)

        self.write(':')

        indented = self.indent()
        self.newline()

        return indented

class Indent(object):
    def __init__(self, parent, txt=None):
        self.parent = parent
        if txt != None:
            parent.write(txt)

        parent.level += 4

        if txt != None:
            parent.newline()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.parent.level -= 4
        self.parent.newline()

class Parens(object):
    def __init__(self, parent):
        self.parent = parent

    def __enter__(self):
        self.parent.write('(')
        return self

    def __exit__(self, type, value, traceback):
        self.parent.write(')')


# XML Helpers #################################################################

def make_node(doc, tag, attrs={}, children=[]):
    node = doc.createElement(tag)

    for key in attrs:
        node.setAttribute(key, str(attrs[key]))

    for child in children:
        node.childNodes.append(child)

    return node

def simple_node(doc, tag, txt):
    return make_node(doc, tag, {}, [ doc.createTextNode(str(txt)) ])


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

                    # print ('Unknown command: %s' % x[0])

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

    def gen_xml(self):
        doc  = MD.Document()
        doc.childNodes.append(make_node(doc, 'AMASE', {}, [
            self._gen_scenario_data(doc),
            self._gen_event_list(doc)
            ]))

        return doc

    def _gen_scenario_data(self, doc):
        maplat = sum([ loc.lat for loc in self.locs ])/float(len(self.locs))
        maplon = sum([ loc.lon for loc in self.locs ])/float(len(self.locs))
        now    = datetime.datetime.now()

        return make_node(doc, 'ScenarioData', {}, [
            make_node(doc, 'SimulationView', {
                'LongExtend': 0.7,
                'Latitude': maplat,
                'Longitude': maplon,
                }, []),
            simple_node(doc, 'ScenarioName', self.name),
            simple_node(doc, 'Date',
                '%d/%d/%d:%d:%d:%d' % (now.day,now.month,now.year,
                        now.hour,now.minute,now.second)),
            simple_node(doc, 'Duration',
                str(self.duration)),
            ])

    def _gen_event_list(self, doc):
        uavNodes    = list(itertools.chain(*map(lambda uav: uav.gen_xml(doc), self.uavs)))
        searchNodes = map(lambda loc: loc.gen_xml(doc), self.locs)

        return make_node(doc, 'ScenarioEventList', {}, uavNodes + searchNodes)

    def gen_script(self, file=sys.stdout):
        pp = Pretty(file)


        map(pp.writeln, [
            'import socket',
            'from geopy.distance import vincenty',
            'from lmcp import LMCPFactory',
            'from afrl.cmasi import EntityState',
            'from afrl.cmasi import AirVehicleState',
            'from afrl.cmasi import AirVehicleConfiguration',
            'from afrl.cmasi.SessionStatus import SessionStatus',
            'from demo_controller import ExampleCtrl',
            'from PyMASE import UAV, Location, get_args',
            'import string',
            ])

        with pp.define('prepare_ctrl_input', 'uavs', 'ctrl_input_args', 'current_plays'):
            pp.writeln('ctrl_input = dict()')

            behaviors, monitors = self.dependencies()

            # update each monitor
            for monitor in monitors:
                pp.write('ctrl_input["')
                pp.write(str(monitor))
                pp.write('"] = UAVs[')
                pp.write(str(monitor.uav))
                pp.write('].')
                pp.writeln(monitor.amase_parameter())

            # update the current play for each 

            pp.write('return ctrl_input')


        # When a message is received, do one of the following:
        with pp.define('message_received', 'obj', 'configMap', 'stateMap'):

            with pp.indent('if isinstance(obj, AirVehicleConfiguration.AirVehicleConfiguration):'):
                pp.writeln('configMap[obj.get_ID()] = obj')

            with pp.indent('elif isinstance(obj, AirVehicleState.AriVehicleState):'):
                pp.writeln('stateMap[obj.get_ID()] = obj')

            # This line was in the original code generator, though the `ss`
            # variable is never referenced anywhere else.
            # with pp.indent('elif isinstance(obj, SessionState):'):
            #     pp.writeln('ss = obj')

        with pp.define('connect'):
            pp.writeln('sock = socket.server(socket.AF_INET, socket.SOCK_STREAM)')
            pp.writeln('server_address = ("localhost", 5555)')
            pp.writeln('print("connecting to %s port %s" % server_address)')
            pp.writeln('sock.connect(server_address)')
            pp.writeln('print("connected")')
            pp.writeln('return sock')

        pp.writeln('sock = connect()')
        pp.writeln('msg = LMCPFactory.LMCPFactory()')
        pp.newline()

        with pp.indent('try:'):
            with pp.indent('while True:'):
                pp.writeln('message = msg.getObject(sock.recv(2224))')
                pp.newline()
                pp.writeln('message_received(message)')

                # this shouldn't be necessary, as each UAV is set to reference
                # the stateMap at startup. Maybe the stateMap just isn't being
                # updated correctly in message_received?
                with pp.indent('for i in range(0, uav_n):'):
                    pp.writeln('UAVs[i].stateMap = stateMap')

                # We should already know the signature of the controller at this
                # point, so we can just call it directly.

                pp.newline()
                pp.writeln('output = M1.move(ctrl_input)')

        with pp.indent('finally:'):
            pp.writeln('print("closing socket")')
            pp.writeln('sock.close()')


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

    def gen_xml(self, doc):
        return make_node(doc, 'AreaSearchTask', {'Series':'CMASI'}, [
            make_node(doc, 'SearchArea', {}, [
                Location._rectangle(doc, self.lat, self.lon, self.width,
                    self.height),
                ]),
            make_node(doc, 'ViewAngleList', {}, []),
            make_node(doc, 'DesiredWaveLengthBands', {}, []),
            simple_node(doc, 'DwellTime', 0),
            simple_node(doc, 'GroundSampleDistance', 0.0),
            simple_node(doc, 'TaskId', 10 + self.num),
            make_node(doc, 'Label', {}, []),
            simple_node(doc, 'RevisitRate', 0.0),
            make_node(doc, 'Parameters', {}, []),
            simple_node(doc, 'Priority', 0),
            simple_node(doc, 'Required', 'false'),
            ])

    @staticmethod
    def _rectangle(doc, lat, lon, width, height):
        return make_node(doc, 'Rectangle', {'Series':'CMASI'}, [
            Location._center_point(doc, lat, lon),
            simple_node(doc, 'Width', width),
            simple_node(doc, 'Height', height),
            simple_node(doc, 'Rotation', 0.0),
            ])

    @staticmethod
    def _center_point(doc, lat, lon):
        return make_node(doc, 'CenterPoint', {'Series':'CMASI'}, [
            make_node(doc, 'Location3D', {'Series':'CMASI'}, [
                simple_node(doc, 'Latitude', lat),
                simple_node(doc, 'Longitude', lon),
                ])
            ])


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

    def gen_xml(self,doc):
        return [ self.gen_xml_config(doc), self.gen_xml_state(doc) ]

    def gen_xml_config(self,doc):
        """Generate air-vehicle configuration for this UAV"""
        return make_node(doc, 'AirVehicleConfiguration', {
                'Time': 0.0,
                'Series': 'CMASI',
            }, [
                simple_node(doc, 'ID', self.num),
                simple_node(doc, 'Label', 'UAV-' + str(self.num)),
                simple_node(doc, 'MinimumSpeed', 15.0),
                simple_node(doc, 'MaximumSpeed', 15.0),
                make_node(doc, 'NomninalFlightProfile', {}, [
                    UAV._flight_profile(doc, 'Cruise', 20.0, 0.0, 0.0)]),
                make_node(doc, 'AlternateFlightProfiles', {}, [
                    UAV._flight_profile(doc, 'Climb', 15.0, 10.0, 5.0),
                    UAV._flight_profile(doc, 'Descent', 25.0, -5.0, -5.0),
                    UAV._flight_profile(doc, 'Loiter', 20.0, 5.0, 0.0),
                    UAV._flight_profile(doc, 'Dash', 35.0, -2.0, 0.0),
                    ]),
                make_node(doc, 'AvailableTurnTypes', {}, [
                    simple_node(doc, 'TurnType', 'TurnShort'),
                    simple_node(doc, 'TurnType', 'FlyOver'),
                    ]),
                simple_node(doc, 'MinimumAltitude', 0.0),
                simple_node(doc, 'MaximumAltitude', 1000000.0),
                simple_node(doc, 'MinAltAboveGround', 0.0),
            ])

    @staticmethod
    def _flight_profile(doc, name, airspeed, pitchAngle, verticalSpeed,):
        return make_node(doc, 'FlightProfile', {'Series': 'CMASI'}, [
            simple_node(doc, 'Name', name),
            simple_node(doc, 'Airspeed', airspeed),
            simple_node(doc, 'PitchAngle', pitchAngle),
            simple_node(doc, 'VerticalSpeed', verticalSpeed),
            simple_node(doc, 'MaxBankAngle', 30.0),
            simple_node(doc, 'EnergyRate', 0.005),
            ])

    def gen_xml_state(self, doc):
        return make_node(doc, 'AirVehicleState', {
            'Time': '0.0',
            'Series': 'CMASI',
            }, [
            simple_node(doc, 'ID', self.num),
            make_node(doc, 'Location', {}, [
                make_node(doc, 'Location3D', {'Series': 'CMASI'}, [
                    simple_node(doc, 'Altitude', 50.0),
                    simple_node(doc, 'Latitude', self.lat),
                    simple_node(doc, 'Longitude', self.lon),
                    ]),
                ]),
            simple_node(doc, 'u', 0.0),
            simple_node(doc, 'v', 0.0),
            simple_node(doc, 'w', 0.0),
            simple_node(doc, 'udot', 0.0),
            simple_node(doc, 'vdot', 0.0),
            simple_node(doc, 'wdot', 0.0),
            simple_node(doc, 'Heading', 90.0),
            simple_node(doc, 'Pitch', 0.0),
            simple_node(doc, 'Roll', 0.0),
            simple_node(doc, 'Airspeed', 0.0),
            simple_node(doc, 'VerticalSpeed', 0.0),
            simple_node(doc, 'ActualEnergyRate', 0.00008),
            simple_node(doc, 'EnergyAvailable', 100.0),
            simple_node(doc, 'Windspeed', 0.0),
            simple_node(doc, 'WindDirection', 0.0),
            simple_node(doc, 'GroundSpeed', 0.0),
            simple_node(doc, 'GroundTrack', 0.0),
            simple_node(doc, 'CurrentWaypoint', 0),
            simple_node(doc, 'CurrentCommand', 0),
            simple_node(doc, 'Mode', 'Waypoint'),
            make_node(doc, 'AssociatedTasks', {}, []),
            simple_node(doc, 'Time', 0.0),
            ])


# Monitors ####################################################################

class Monitor(object):
    def amase_parameter(self):
        """
        Returns the name of the UAV parameter that is queried for this monitor
        """
        pass

class FuelMonitor(Monitor):
    def __init__(self, uav):
        self.uav = uav

    def __str__(self):
        return ('M_%d_Fuel_0_0' % self.uav)

    def amase_parameter(self):
        return 'Fuel'

class FoundMonitor(Monitor):
    def __init__(self, uav, target):
        self.uav = uav
        self.target = target

    def __str__(self):
        return ('M_%d_Found_%d_0' % (self.uav, self.target))

    def amase_parameter(self):
        return 'Found'


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

    def __init__(self, uav, loc, target):
        print(uav, loc, target)
        self.uav    = int(uav)
        self.target = int(target)
        self.loc    = int(loc)

    def __str__(self):
        return ('P_%d_ST_%d_%d' % (self.uav, self.loc, self.target))

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

    # Write out the XML for AMASE
    with open('../auto_generated/auto_code.xml', 'w') as xml:
        spec.gen_xml().writexml(xml, '', '  ', '\n')

    # Write out the outer loop controller for the scenario
    # with open('../auto_generated/auto_code.py', 'w') as script:
    #     spec.gen_script(script)
    spec.gen_script(sys.stdout)

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
