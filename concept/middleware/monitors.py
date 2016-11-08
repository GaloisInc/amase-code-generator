
class Monitor(object):
    __slots__ = ['uav', 'target', 'loc']

    # subclasses should override this property
    name = 'monitor'

    def __init__(self, uav, target, loc):
        self.uav = uav
        self.target = target
        self.loc = loc

    def __eq__(self, other):
        return all([
            isinstance(other, type(self)),
            self.uav == other.uav,
            self.target == other.target,
            self.loc == other.loc])

    def __hash__(self):
        return hash((self.uav, self.name, self.target, self.loc))

    def amase_user_monitor(self, arg):
        """The invocation of the user-supplied monitor function."""
        return '{s.name}_monitor({arg}, {s.uav:d}, {s.loc:d})'.format(
            s=self, arg=arg)

    def amase_monitor_def(self, pp):
        """The definition of this monitor for AMASE."""
        pass


class FuelMonitor(Monitor):
    name = 'fuel'

    def __init__(self, uav):
        super(FuelMonitor, self).__init__(uav, 0, 0)

    def __str__(self):
        return ('M_{s.uav:d}_Fuel_0_0'.format(s=self))

    def amase_monitor_def(self, pp):
        with pp.define('fuel_monitor', 'uav', 'uav2', 'loc'):
            pp.writeln('fuel = uav.get_energy()')
            with pp.indent('if 0 < fuel <= 90:'):
                pp.writeln('uav.Fuel = 1')
            with pp.indent('elif fuel > 90:'):
                pp.writeln('uav.Fuel = 0')
            pp.writeln('return uav')


class FoundMonitor(Monitor):
    name = 'found'

    def __init__(self, uav, target):
        super(FoundMonitor, self).__init__(uav, target, 0)

    def __str__(self):
        return ('M_{s.uav:d}_Found_{s.target:d}_0'.format(s=self))

    def amase_monitor_def(self, pp):
        with pp.define('found_monitor', 'uav', 'uav2', 'loc'):
            with pp.indent('dist = vincenty('):
                pp.writeln('(uav.getit("latitude", uav.id),')
                pp.writeln(' uav.getit("longitude", uav.id)),')
                pp.writeln('(uav.getit("latitude", uav2 + 1),')
                pp.writeln(' uav.getit("longitude", uav2 + 1))).meters')
            with pp.indent('if 0 < dist < 600:'):
                pp.writeln('uav.found = 1')
            with pp.indent('else:'):
                pp.writeln('uav.found = 0')
            pp.writeln('return uav')
