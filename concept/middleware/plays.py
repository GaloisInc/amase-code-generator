from behaviors import SearchBehavior, TrackBehavior, LoiterBehavior
from monitors import FoundMonitor


class Play(object):
    @staticmethod
    def make(descr):

        # Format: <uav> Loiter <uav2> <loc>
        if descr[2] == 'Loiter':
            return LoiterPlay(
                int(descr[1]) - 1)

        # Format: <uav> ST <uav2> <loc>
        elif descr[2] == 'ST':
            return STPlay(
                int(descr[1]) - 1,
                int(descr[3]) - 1,
                int(descr[4]) - 1)

        else:
            raise RuntimeError('Invalid play: ' + descr[2])

    def behaviors(self):
        return set()

    def monitors(self):
        return set()


class STPlay(Play):
    """Search and track for the specified uav, in the region provided."""

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
        return 'P_{stp.uav}_ST_{stp.target}_{stp.loc}'.format(stp=self)


class LoiterPlay(Play):

    def __init__(self, uav):
        self.uav = uav

    def __str__(self):
        return 'P_{}_Loiter_0_0'.format(self.uav)

    def behaviors(self):
        return set([LoiterBehavior(self.uav, 0, 0)])

    def play_name(self):
        return 'Loiter'
