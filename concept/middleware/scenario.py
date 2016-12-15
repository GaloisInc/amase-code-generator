
import sys
import datetime
from itertools import chain

from locations import Location
from plays import Play
from uavs import UAV
from pretty import Pretty
from xml_helpers import make_doc, make_node, simple_node


class Scenario(object):
    __slots__ = ['locs', 'uavs', 'name', 'duration']

    @staticmethod
    def parse(file):
        """Parse the spec file, and produce a scenario."""
        locs = []
        uavs = []

        with open(file, 'r') as f:
            for x in f:
                x = x.split()
                if len(x[0]) > 2:
                    if x[0] == 'uav':
                        uavs.append(
                            UAV(                # Format:
                                int(x[1]) - 1,  # <number>
                                float(x[2]),    # <lat>
                                float(x[3])))   # <lon>
                    elif x[0] == 'loc':
                        locs.append(
                            Location(           # Format:
                                int(x[1]) - 1,  # <number>
                                float(x[2]),    # <lat>
                                float(x[3]),    # <lon>
                                float(x[4]),    # <width>
                                float(x[5])))   # <height>
                    elif x[0] == 'cmd':
                        play = Play.make(x[1:])
                        uavs[play.uav - 1].add_play(play)
                    # else print ('Unknown command: %s' % x[0])

        return Scenario('Test Scenario', locs, uavs)

    def __init__(self, name, locs, uavs):
        self.name = name
        self.locs = locs
        self.uavs = uavs
        self.duration = 60000

    def __repr__(self):
        return "Scenario(name='{s.name}', locs={s.locs}, uavs={s.uavs})".format(s=self)

    def __str__(self):
        """Printable representation of a scenario."""
        return '{name}\n{locs}\n{uavs}\n{dur}\n'.format(
            name=self.name,
            locs=[str(loc) for loc in self.locs],
            uavs=[str(uav) for uav in self.uavs],
            dur=str(self.duration))

    def plays(self):
        """All active plays in this scenario."""
        return list(chain(*map(lambda uav: uav.plays, self.uavs)))

    def dependencies(self):
        """Produce the behavior and monitor dependencies for this scenario."""
        behaviors, monitors = set(), set()
        for uav in self.uavs:
            behaviors = behaviors.union(uav.behaviors())
            monitors = monitors.union(uav.monitors())
        return (behaviors, monitors)

    def gen_xml(self):
        doc = make_doc()
        doc.childNodes.append(
            make_node(
                doc, 'AMASE',
                children=[
                    self._gen_scenario_data(doc),
                    self._gen_event_list(doc)
                ]))
        return doc

    def _gen_scenario_data(self, doc):
        loclen = float(len(self.locs))
        maplat = sum([loc.lat for loc in self.locs]) / loclen
        maplon = sum([loc.lon for loc in self.locs]) / loclen
        now = datetime.datetime.now().strftime('%d/%m/%y:%H:%M:%S')

        return make_node(
            doc, 'ScenarioData',
            children=[
                make_node(
                    doc, 'SimulationView', attrs={
                        'LongExtend': 0.7,
                        'Latitude': maplat,
                        'Longitude': maplon}),
                simple_node(doc, 'ScenarioName', self.name),
                simple_node(doc, 'Date', now),
                simple_node(doc, 'ScenarioDuration', str(self.duration)),
            ])

    def _gen_event_list(self, doc):
        uav_nodes = list(chain(*map(lambda uav: uav.gen_xml(doc), self.uavs)))
        search_nodes = map(lambda loc: loc.gen_xml(doc), self.locs)

        return make_node(
            doc, 'ScenarioEventList', children=uav_nodes + search_nodes)

    def gen_script(self, file=sys.stdout):
        pp = Pretty(file)

        behaviors, monitors = self.dependencies()

        map(pp.writeln, [
            'import socket',
            'from geopy.distance import vincenty',
            'from lmcp import LMCPFactory',
            # 'from afrl.cmasi import EntityState',  # unused
            'from afrl.cmasi import AirVehicleState',
            'from afrl.cmasi import AirVehicleConfiguration',
            # 'from afrl.cmasi.SessionStatus import SessionStatus',  # unused
            'from demo_controller import ExampleCtrl',
            'from PyMASE import UAV, Location, get_args',
            '',
            'M1 = ExampleCtrl()',
            'state_map = {}',
            'config_map = {}',
            'ctrl_input = {key: False for key in get_args(M1.move)}',
            'current_plays = []',
            'config = AirVehicleConfiguration.AirVehicleConfiguration',
            'state = AirVehicleState.AirVehicleState'
        ])

        with pp.define('prepare_ctrl_input', 'uavs', 'current_plays'):
            with pp.indent('return {'):

                # update each monitor
                for m in monitors:
                    pp.writeln("'{m}': UAVs[{m.uav:d}].{m.name},".format(m=m))

                # update the current play for each
                for p in self.plays():
                    # TODO: `current_plays` is never modified, what is it that
                    # drives this input in a running scenario?
                    pp.writeln("'{p}': '{p}' in current_plays,".format(p=p))

            pp.writeln('}')

        # When a message is received, do one of the following:
        with pp.define('message_received', 'obj', 'config_map', 'state_map'):

            with pp.indent('if isinstance(obj, config):'):
                pp.writeln('config_map[obj.get_ID()] = obj')

            with pp.indent('elif isinstance(obj, state):'):
                pp.writeln('state_map[obj.get_ID()] = obj')

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
        bs = {b.name: b for b in behaviors}
        for name in bs:
            bs[name].amase_behavior_def(pp)

        # TODO: these should be outputted once for each class of monitor
        # Write out each monitor
        ms = {m.name: m for m in monitors}
        for name in ms:
            ms[name].amase_monitor_def(pp)

        pp.vspace()
        pp.writeln('sock = connect()')
        pp.writeln('msg = LMCPFactory.LMCPFactory()')

        # Initialize the UAVs
        pp.vspace()
        pp.comment('Initialize UAVs')
        with pp.indent('UAVs = ['):
            for uav in self.uavs:
                pp.writeln('UAV({uav.num:d}, sock, state_map),'.format(uav=uav))
        pp.writeln(']')

        # Construct an AMASE location for each of our locations
        pp.vspace()
        pp.comment('Initialize location state')
        with pp.indent('locations = ['):
            for loc in self.locs:
                pp.writeln(loc.__repr__() + ',')
        pp.writeln(']')

        # Consume initialization messages from the socket
        pp.vspace()
        pp.comment('Initialize UAV state')
        pp.writeln('flag = True')
        with pp.indent('while flag:'):
            pp.writeln('flag = False')
            pp.writeln('message = msg.getObject(sock.recv(2224))')
            pp.writeln('message_received(message, config_map, state_map)')
            with pp.indent('for uav in UAVs:'):
                pp.writeln('uav.stateMap = state_map')
                with pp.indent('if uav.state_map.get(uav.id) is None:'):
                    pp.writeln('flag = True')

        pp.vspace()
        pp.comment('Handle messages')
        with pp.indent('try:'):
            with pp.indent('while True:'):
                pp.writeln('message = msg.getObject(sock.recv(2224))')

                # update monitors
                pp.vspace()
                for monitor in monitors:
                    pp.writeln('UAVs[{m.uav:d}] = {aum}'.format(
                        m=monitor,
                        aum=monitor.amase_user_monitor(
                            'UAVs[{uav:d}]'.format(uav=monitor.uav))))

                # handle a new message
                pp.vspace()
                pp.writeln('message_received(message, config_map, state_map)')

                # this shouldn't be necessary, as each UAV is set to reference
                # the stateMap at startup. Maybe the stateMap just isn't being
                # updated correctly in message_received?
                with pp.indent('for i in range(0, %d):' % len(self.uavs)):
                    pp.writeln('UAVs[i].state_map = state_map')

                # at this point, the map `ctrl_input` has members that match
                # the arguments to the controller, so call it with those as the
                # input.
                pp.vspace()
                pp.writeln('ctrl_input = prepare_ctrl_input(UAVs, current_plays)')
                pp.writeln('output = M1.move(**ctrl_input)')

                # Update the internal state based on values of output
                pp.vspace()
                for behavior in behaviors:
                    with pp.indent('if output["{}"]:'.format(behavior)):
                        pp.writeln('{}(UAVs[{:d}], {:d}, {:d})'.format(
                            behavior.name.lower(),
                            behavior.uav,
                            behavior.uav2,
                            behavior.loc))
                    pp.vspace()

        pp.vspace()
        with pp.indent('finally:'):
            pp.writeln('print("closing socket")')
            pp.writeln('sock.close()')

        pp.vspace()


    def gen_GUI_script(self, file=sys.stdout):
        pp = Pretty(file)

        behaviors, monitors = self.dependencies()
        map(pp.writeln, [
            'package amase.examples;',
            'import afrl.cmasi.SessionStatus;',
            'import afrl.cmasi.Play;',
            'import java.util.HashMap;',
            'import avtas.app.UserExceptions;',
            'import avtas.amase.AmasePlugin;',
            'import avtas.amase.scenario.ScenarioEvent;',
            'import avtas.amase.scenario.ScenarioState;',
            'import avtas.amase.util.CmasiNavUtils;',
            'import avtas.amase.util.CmasiUtils;',
            'import avtas.app.AppEventManager;',
            'import avtas.util.NavUtils;',
            'import java.awt.Component;',
            'import java.awt.FlowLayout;',
            'import java.awt.event.ActionEvent;',
            'import java.awt.event.ActionListener;',
            'import java.util.ArrayList;',
            'import java.util.List;',
            'import java.util.Random;',
            'import java.util.TreeMap;',
            'import javax.swing.JButton;',
            'import javax.swing.JPanel;',
            'import javax.swing.border.EmptyBorder;',
            ''
        ])

        with pp.indent('public class PlayGUI extends AmasePlugin {'):
            pp.writeln('JPanel panel;')
            pp.writeln('SessionStatus lastStatus = null;')
            for uav in self.uavs:
                for play in uav.plays:
                    pp.writeln('JButton {};'.format(play.__str__()))
            with pp.indent('public PlayGUI() {'):
                pp.writeln('setPluginName("Play-GUI");')
                pp.writeln('setupGui();')
            pp.writeln('}')
            pp.vspace()

            pp.writeln('@Override')
            with pp.indent('public void eventOccurred(Object event) {'):
                with pp.indent('if (event instanceof ScenarioEvent) {'):
                    pp.writeln('initScenario((ScenarioEvent) event);')
                pp.writeln('}')
                with pp.indent('else if (event instanceof SessionStatus) {'):
                    pp.writeln('lastStatus = (SessionStatus) event;')
                pp.writeln('}')
            pp.writeln('}')

            with pp.indent('protected void initScenario(ScenarioEvent scenarioEvent) {'):
                pp.writeln('System.out.println("New Scenario loaded.");')
                for uav in self.uavs:
                    for play in uav.plays:
                        pp.writeln('{}.setEnabled(true);'.format(play.__str__()))
            pp.writeln('}')

            pp.writeln('@Override')
            with pp.indent('public Component getGui() {'):
                pp.writeln('return panel;')
            pp.writeln('}')

            with pp.indent('protected void setupGui() {'):
                pp.writeln('panel = new JPanel();')
                pp.writeln('panel.setLayout(new FlowLayout(FlowLayout.CENTER));')
                pp.writeln('panel.setBorder(new EmptyBorder(5, 5, 5, 5));')
                for uav in self.uavs:
                    for i, play in enumerate(uav.plays):
                        pp.writeln('{0} = new JButton("{0}");'.format(play.__str__()))
                        pp.writeln('panel.add({});'.format(play.__str__()))
                        pp.writeln('{0}.setEnabled(false);'.format(play.__str__()))
                        with pp.indent('{0}.addActionListener(new ActionListener() {{'.format(play.__str__())):
                            pp.writeln('@Override')
                            with pp.indent('public void actionPerformed(ActionEvent e) {{'.format(play.__str__())):
                                pp.writeln('notify{}{}();'.format(i+1,play.uav+1))
                            pp.writeln('}')
                        pp.writeln('});')
            pp.writeln('}')

            for uav in self.uavs:
                for i, play in enumerate(uav.plays):
                    with pp.indent('private void notify{}{}() {{'.format(i+1,play.uav+1)):
                        pp.writeln('sendPlay({},{});'.format(i+1,play.uav+1))
                    pp.writeln('}')

            with pp.indent('void sendPlay(int a, int b) {'):
                pp.writeln('Play play = new Play();')
                pp.writeln('play.setPlayID(a);')
                pp.writeln('play.setUAVID(b);')
                pp.writeln('play.setTime(lastStatus.getScenarioTime());')
                pp.writeln('fireEvent(play);')
            pp.writeln('}')
        pp.writeln('}')



#     void sendPlay(int a, int b) {

#         Play play = new Play();
#         play.setPlayID(a);
#         play.setUAVID(b);
#         play.setTime(lastStatus.getScenarioTime());

#         fireEvent(play);
#     }
# }