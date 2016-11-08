
class Behavior(object):

    # subclasses should override this property
    name = 'behavior'

    def __init__(self, uav, loc, uav2):
        self.uav  = int(uav)
        self.uav2 = int(uav2)
        self.loc  = int(loc)

    def __eq__(self, other):
        return all([
            isinstance(other, type(self)),
            self.uav == other.uav,
            self.uav2 == other.uav2,
            self.loc == other.loc])

    def __hash__(self):
        return hash((self.uav, self.name, self.uav2, self.loc))

    def __repr__(self):
        return '{cls}(uav={s.uav}, loc={s.loc}, uav2={s.uav2})'.format(
            cls=self.__class__.__name__, s=self)

    def __str__(self):
        return 'B_{s.uav}_{s.name}_{s.uav2}_{s.loc}'.format(s=self)

    def amase_behavior_def(self, pp):
        """The skeleton of how to handle this behavior in AMASE."""
        with pp.define(self.name.lower(), 'uav', 'uav2', 'loc'):
            pp.comment('TODO: implement behavior')
            pp.writeln('return 0')


class RefuelBehavior(Behavior):
    name = 'Refuel'


class LoiterBehavior(Behavior):
    name = 'Loiter'


class SearchBehavior(Behavior):
    name = 'Search'


class TrackBehavior(Behavior):
    name = 'Track'
