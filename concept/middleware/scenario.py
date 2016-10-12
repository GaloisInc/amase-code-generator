
from xml_helpers import make_doc, make_node, simple_node
from pretty import Pretty
import sys
import datetime
import itertools
import string

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

                    # Format: uav <number> <lat> <lon>
                    if x[0] == 'uav':
                        uavs.append(UAV(int(x[1]) - 1, float(x[2]), float(x[3])))
                        continue

                    # Format: loc <number> <lat> <lon> <width> <height>
                    if x[0] == 'loc':
                        locs.append(Location(int(x[1])-1, float(x[2]),
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

    def __str__(self):
        return '{}\n{}\n{}\n{}\n'.format(self.name,
                [ str(loc) for loc in self.locs ],
                [ str(uav) for uav in self.uavs ],
                str(self.duration))

    def plays(self):
        """All active plays in this scenario"""
        return list(itertools.chain(*map(lambda uav: uav.plays, self.uavs)))

    def dependencies(self):
        """Produce the behavior and monitor dependencies for this scenario"""
        behaviors = set()
        monitors  = set()

        for uav in self.uavs:
            behaviors = behaviors.union(uav.behaviors())
            monitors  = monitors.union(uav.monitors())

        return (behaviors, monitors)

    def gen_xml(self):
        doc = make_doc()
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

        behaviors, monitors = self.dependencies()

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
            '',
            'M1 = ExampleCtrl()',
            'stateMap = dict()',
            'configMap = dict()',
            'ctrl_input = { key: False for key in get_args(M1.move) }'
            ])

        with pp.define('prepare_ctrl_input', 'uavs', 'ctrl_input_args', 'current_plays'):
            pp.writeln('ctrl_input = dict()')

            # update each monitor
            for monitor in monitors:
                pp.writeln('ctrl_input["%s"] = UAVs[%d].%s' % (monitor,
                    monitor.uav, monitor.monitor_name()))

            # update the current play for each 
            for play in self.plays():
                # TODO: `current_plays` is never modified, what is it that drives
                # this input in a running scenario?
                pp.writeln('ctrl_input["%s"] = "%s" in current_plays' %
                        (str(play), str(play)))

            pp.writeln('return ctrl_input')


        # When a message is received, do one of the following:
        with pp.define('message_received', 'obj', 'configMap', 'stateMap'):

            pp.newline()
            with pp.indent('if isinstance(obj, AirVehicleConfiguration.AirVehicleConfiguration):'):
                pp.writeln('configMap[obj.get_ID()] = obj')

            pp.newline()
            with pp.indent('elif isinstance(obj, AirVehicleState.AirVehicleState):'):
                pp.writeln('stateMap[obj.get_ID()] = obj')

            # TODO: This line was in the original code generator, though the
            # `ss` variable is never referenced anywhere else.
            # with pp.indent('elif isinstance(obj, SessionState):'):
            #     pp.writeln('ss = obj')

        with pp.define('connect'):
            pp.writeln('sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)')
            pp.writeln('server_address = ("localhost", 5555)')
            pp.writeln('print("connecting to %s port %s" % server_address)')
            pp.writeln('sock.connect(server_address)')
            pp.writeln('print("connected")')
            pp.writeln('return sock')


        # TODO: these should be outputted once for each class of behavior
        # Write out behavior skeletons
        bs = { b.behavior_name(): b for b in behaviors }
        for name in bs:
            pp.newline()
            bs[name].amase_behavior_def(pp)

        # TODO: these should be outputted once for each class of monitor
        # Write out each monitor
        ms = { m.monitor_name(): m for m in monitors }
        for name in ms:
            pp.newline()
            ms[name].amase_monitor_def(pp)

        pp.newline()
        pp.writeln('sock = connect()')
        pp.writeln('msg = LMCPFactory.LMCPFactory()')

        # Initialize the UAVs
        pp.newline()
        pp.comment('Initialize UAVs')
        with pp.indent('UAVs = ['):
            for uav in self.uavs:
                pp.writeln('UAV(%d, sock, stateMap),' % uav.num)
            pp.writeln(']')

        # Construct an AMASE location for each of our locations
        pp.newline()
        pp.comment('Initialize location state')
        with pp.indent('locations = ['):
            for loc in self.locs:
                pp.writeln('Location(%f,%f,%f,%f,"%s"),' % (loc.lat, loc.lon,
                    loc.height, loc.width, string.ascii_uppercase[loc.num]))
            pp.writeln(']')

        # Consume initialization messages from the socket
        pp.newline()
        pp.comment('Initialize UAV state')
        pp.writeln('flag = False')
        with pp.indent('while flag:'):
            pp.writeln('flag = True')
            pp.writeln('message = msg.getObject(sock.recv(2224))')
            pp.writeln('message_received(message, configMap, stateMap)')
            with pp.indent('for uav in UAVs:'):
                pp.writeln('uav.stateMap = stateMap')
                with pp.indent('if uav.stateMap.get(uav.id) is None:'):
                    pp.writeln('flag = False')

        pp.newline()
        pp.comment('Handle messages')
        with pp.indent('try:'):
            with pp.indent('while True:'):
                pp.writeln('message = msg.getObject(sock.recv(2224))')

                # update monitors
                pp.newline()
                for monitor in monitors:
                    ix = monitor.uav - 1
                    pp.writeln('UAVs[%d] = %s' % (ix,
                        monitor.amase_user_monitor('UAVs[%d]' % ix)))

                # handle a new message
                pp.newline()
                pp.writeln('message_received(message, configMap, stateMap)')

                # this shouldn't be necessary, as each UAV is set to reference
                # the stateMap at startup. Maybe the stateMap just isn't being
                # updated correctly in message_received?
                with pp.indent('for i in range(0, %d):' % len(self.uavs)):
                    pp.writeln('UAVs[i].stateMap = stateMap')

                # at this point, the map `ctrl_input` has members that match the
                # arguments to the controller, so call it with those as the
                # input.
                pp.newline()
                pp.writeln('output = M1.move(**ctrl_input)')
                pp.writeln('print(output)')

                # Update the internal state based on values of output
                pp.newline()
                for behavior in behaviors:
                    with pp.indent('if output["%s"]:' % str(behavior)):
                        pp.writeln('%s(UAVs[%d],%d,%d)' %
                                (behavior.behavior_name(),
                                    behavior.uav,
                                    behavior.uav2,
                                    behavior.loc))
                    pp.newline()

        pp.newline()
        with pp.indent('finally:'):
            pp.writeln('print("closing socket")')
            pp.writeln('sock.close()')


# Locations ###################################################################

class Location(object):
    __slots__ = ['num', 'lat', 'lon', 'width', 'height']

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
            simple_node(doc, 'ActualEnergyRate', '%f' % 0.00008),
            simple_node(doc, 'EnergyAvailable', 100.0),
            simple_node(doc, 'Windspeed', 0.0),
            simple_node(doc, 'WindDirection', 0.0),
            simple_node(doc, 'GroundSpeed', 0.0),
            simple_node(doc, 'GroundTrack', 0.0),
            simple_node(doc, 'CurrentWaypoint', 0),
            simple_node(doc, 'CurrentCommand', 0),
            simple_node(doc, 'Mode', 'Waypoint'),
            make_node(doc, 'AssociatedTasks', {}, []),
            simple_node(doc, 'Time', 0),
            ])


# Monitors ####################################################################

class Monitor(object):
    __slots__ = ['uav', 'target', 'loc']

    def monitor_name(self):
        """
        Returns the name of the UAV parameter that is queried for this monitor
        """
        pass

    def amase_user_monitor(self, arg):
        """
        Returns the invocation of the user-supplied monitor function.
        """
        return '%s_monitor(%s, %d, %d)' % (self.monitor_name(), str(arg),
                self.uav, self.loc)

    def amase_monitor_def(self, pp):
        """
        Returns the definition of this monitor for Amase.
        """
        pass

class FuelMonitor(Monitor):
    def __init__(self, uav):
        self.uav = uav
        self.target = 0
        self.loc = 0

    def __str__(self):
        return ('M_%d_Fuel_0_0' % self.uav)

    def monitor_name(self):
        return 'Fuel'

    def amase_monitor_def(self, pp):
        with pp.define('Fuel_monitor', 'uav', 'uav2', 'loc'):
            pp.writeln('fuel = uav.get_energy()')
            with pp.indent('if fuel <= 90 and fuel != 0:'):
                pp.write('uav.Fuel = 1')

            pp.newline()
            with pp.indent('elif fuel > 90:'):
                pp.write('uav.Fuel = 0')

            pp.newline()
            pp.writeln('return uav')

class FoundMonitor(Monitor):
    def __init__(self, uav, target):
        self.uav = uav
        self.target = target
        self.loc = 0

    def __str__(self):
        return ('M_%d_Found_%d_0' % (self.uav, self.target))

    def monitor_name(self):
        return 'Found'

    def amase_monitor_def(self, pp):
        with pp.define('Found_monitor', 'uav', 'uav2', 'loc'):
            pp.writeln('dist = vincenty((uav.getit("latitude",uav.id),uav.getit("longitude",uav.id))'
                       ',(uav.getit("latitude",uav2+1),uav.getit("longitude",uav2+1))).meters')
            with pp.indent('if dist < 600 and dist != 0:'):
                pp.write('uav.Found = 1')

            pp.newline()
            with pp.indent('else:'):
                pp.write('uav.Found = 0')

            pp.newline()
            pp.writeln('return uav')



# Behaviors ###################################################################

class Behavior(object):
    def __init__(self, uav, loc, uav2):
        self.uav  = int(uav)
        self.uav2 = int(uav2)
        self.loc  = int(loc)

    def __eq__(self, other):
        return self.uav == other.uav \
                and self.uav2 == other.uav2 \
                and self.loc  == other.loc

    def __hash__(self):
        return hash((self.uav, self.uav2, self.loc))

    def __str__(self):
        return 'B_{uav}_{name}_{uav2}_{loc}'.format(
                uav=self.uav, name=self.behavior_name(), uav2=self.uav2,
                loc=self.loc)

    def amase_behavior_def(self, pp):
        """
        The skeleton of how to handle this behavior in AMASE
        """
        with pp.define(self.behavior_name(), 'uav', 'uav2', 'loc'):
            pp.comment('TODO: implement behavior')
            pp.writeln('return 0')

class RefuelBehavior(Behavior):
    """The Refuel behavior"""

    def behavior_name(self):
        return 'Refuel'

class LoiterBehavior(Behavior):
    """The Loiter behavior """

    def behavior_name(self):
        return 'Loiter'

class SearchBehavior(Behavior):
    """The Search behavior"""

    def behavior_name(self):
        return 'Search'

class TrackBehavior(Behavior):
    """The Track behavior"""

    def behavior_name(self):
        return 'Track'


# Plays #######################################################################

class Play(object):
    @staticmethod
    def make(descr):

        # Format: <uav> Loiter <uav2> <loc>
        if descr[2] == 'Loiter':
            return LoiterPlay(int(descr[1])-1)

        # Format: <uav> ST <uav2> <loc>
        elif descr[2] == 'ST':
            return STPlay(int(descr[1])-1, int(descr[3])-1, int(descr[4])-1)

        else:
            raise RuntimeError('Invalid play: ' + descr[2])

    def behaviors(self):
        return set()

    def monitors(self):
        return set()

class STPlay(Play):
    """Search and track for the specified uav, in the region provided.  """

    def __init__(self, uav, target, loc):
        self.uav = uav
        self.target = target
        self.loc = loc

    def behaviors(self):
        return set([
                SearchBehavior(self.uav, self.target, self.loc),
                TrackBehavior(self.uav, self.target, self.loc)])

    def monitors(self):
        return set([FoundMonitor(self.uav, self.target)])

    def play_name(self):
        return 'ST'

    def __str__(self):
        return 'P_{}_ST_{}_{}'.format(self.uav, self.target, self.loc)

class LoiterPlay(Play):
    """The Loiter play"""

    def __init__(self, uav):
        self.uav = uav

    def __str__(self):
        return 'P_{}_Loiter_0_0'.format(self.uav)

    def behaviors(self):
        return set([LoiterBehavior(self.uav, 0, 0)])

    def play_name(self):
        return 'Loiter'


