
from monitors import FuelMonitor
from behaviors import RefuelBehavior
from xml_helpers import make_node, simple_node


class UAV(object):
    def __init__(self, num, lat, lon):
        self.num = num
        self.lat = lat
        self.lon = lon
        self.plays = []

    def add_play(self, play):
        self.plays.append(play)

    def __repr__(self):
        return 'UAV(num={s.num}, lat={s.lat}, lon={s.lon})'.format(s=self)

    def behaviors(self):
        # start as just the contingency behavior
        deps = set([RefuelBehavior(self.num, 0, 0)])

        # add in behaviors required for each play
        for play in self.plays:
            deps = deps.union(play.behaviors())

        return deps

    def monitors(self):
        """The set of monitors that this UAV requires."""
        # each uav requires the fuel monitor for its refueling contingency
        # behavior
        deps = set([FuelMonitor(self.num)])

        for play in self.plays:
            deps = deps.union(play.monitors())

        return deps

    def gen_xml(self, doc):
        return [self.gen_xml_config(doc), self.gen_xml_state(doc)]

    def gen_xml_config(self, doc):
        """Generate air-vehicle configuration for this UAV."""
        return make_node(
            doc, 'AirVehicleConfiguration', {'Time': 0.0, 'Series': 'CMASI'}, [
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
                    UAV._flight_profile(doc, 'Dash', 35.0, -2.0, 0.0)]),
                make_node(doc, 'AvailableTurnTypes', {}, [
                    simple_node(doc, 'TurnType', 'TurnShort'),
                    simple_node(doc, 'TurnType', 'FlyOver')]),
                simple_node(doc, 'MinimumAltitude', 0.0),
                simple_node(doc, 'MaximumAltitude', 1000000.0),
                simple_node(doc, 'MinAltAboveGround', 0.0)])

    @staticmethod
    def _flight_profile(doc, name, airspeed, pitch_angle, vertical_speed,):
        return make_node(doc, 'FlightProfile', {'Series': 'CMASI'}, [
            simple_node(doc, 'Name', name),
            simple_node(doc, 'Airspeed', airspeed),
            simple_node(doc, 'PitchAngle', pitch_angle),
            simple_node(doc, 'VerticalSpeed', vertical_speed),
            simple_node(doc, 'MaxBankAngle', 30.0),
            simple_node(doc, 'EnergyRate', 0.005)])

    def gen_xml_state(self, doc):
        return make_node(
            doc, 'AirVehicleState', {'Time': '0.0', 'Series': 'CMASI'}, [
                simple_node(doc, 'ID', self.num),
                make_node(doc, 'Location', {}, [
                    make_node(doc, 'Location3D', {'Series': 'CMASI'}, [
                        simple_node(doc, 'Altitude', 50.0),
                        simple_node(doc, 'Latitude', self.lat),
                        simple_node(doc, 'Longitude', self.lon)])]),
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
                simple_node(doc, 'Time', 0)])
