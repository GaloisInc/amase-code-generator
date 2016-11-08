
from xml_helpers import make_node, simple_node


class Location(object):
    __slots__ = ['num', 'lat', 'lon', 'width', 'height']

    def __init__(self, num, lat, lon, width, height):
        self.num = num
        self.lat = lat
        self.lon = lon
        self.width = width
        self.height = height

    def __repr__(self):
        return ('Location({s.num}, lat={s.lat}, lon={s.lon}, ' +
                'width={s.width}, height={s.height})').format(s=self)

    def __str__(self):
        """Location: lat, lon, width, height."""
        return 'L_{s.lat:d}_{s.lon:d}_{s.width:d}_{s.height:d}'.format(s=self)

    def gen_xml(self, doc):
        return make_node(doc, 'AreaSearchTask', {'Series': 'CMASI'}, [
            make_node(doc, 'SearchArea', {}, [
                Location._rectangle(
                    doc, self.lat, self.lon, self.width, self.height)]),
            make_node(doc, 'ViewAngleList', {}, []),
            make_node(doc, 'DesiredWaveLengthBands', {}, []),
            simple_node(doc, 'DwellTime', 0),
            simple_node(doc, 'GroundSampleDistance', 0.0),
            simple_node(doc, 'TaskId', 10 + self.num),
            make_node(doc, 'Label', {}, []),
            simple_node(doc, 'RevisitRate', 0.0),
            make_node(doc, 'Parameters', {}, []),
            simple_node(doc, 'Priority', 0),
            simple_node(doc, 'Required', 'false')])

    @staticmethod
    def _rectangle(doc, lat, lon, width, height):
        return make_node(doc, 'Rectangle', {'Series': 'CMASI'}, [
            Location._center_point(doc, lat, lon),
            simple_node(doc, 'Width', width),
            simple_node(doc, 'Height', height),
            simple_node(doc, 'Rotation', 0.0)])

    @staticmethod
    def _center_point(doc, lat, lon):
        return make_node(doc, 'CenterPoint', {'Series': 'CMASI'}, [
            make_node(doc, 'Location3D', {'Series': 'CMASI'}, [
                simple_node(doc, 'Latitude', lat),
                simple_node(doc, 'Longitude', lon)])])
