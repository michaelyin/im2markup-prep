from unittest import TestCase
from net.wyun.mer.ink.sample import Sample


class TestStroke(TestCase):
    def setUp(self):
        idd = Sample('data/inkml/65_alfonso.inkml')
        self.stroke0 = idd.traces[0]
        self.stroke1 = idd.traces[1]
        self.stroke2 = idd.traces[2]
        self.stroke9 = idd.traces[9]


    def test_calc_coords_h10000(self):
        '''
        show stroke0's coords data after scaling to H = 10000
        :return:
        '''
        co_h10000 = self.stroke0.coords_h10000
        print 'stroke0 coords_h10000\n', co_h10000
        print 'stroke0 coords_h10000 Transpose\n', co_h10000.T

    def test_stroke0_bbx_h10000(self):
        '''
        stroke 0, bounding box rx, ry, rs, rt should be 0 3018 9622 9811
        :return:
        '''
        rx, ry, rs, rt = self.stroke0.get_bounding_box_h10000()
        print rx, ry, rs, rt
        self.assertTrue((rx, ry, rs, rt) == (0, 3018, 9622, 9811))

    def test_stroke9_bbx_h10000(self):
        '''
        stroke 0, bounding box rx, ry, rs, rt should be 0 3018 9622 9811
        :return:
        '''
        rx, ry, rs, rt = self.stroke9.get_bounding_box_h10000()
        print rx, ry, rs, rt
        self.assertTrue((rx, ry, rs, rt) == (63584, 4716, 68867, 5283))

    def test_distance_1(self):
        dist = self.stroke0.distance(self.stroke1)
        print '\n', dist

    def test_distance_2(self):
        dist = self.stroke0.distance(self.stroke2)
        print '\n', dist

    '''
    stroke 0 print out in render()
aux.x, aux.y: 19: 149
aux.x, aux.y: 5: 145
aux.x, aux.y: 87: 82
aux.x, aux.y: 96: 82
aux.x, aux.y: 106: 87
aux.x, aux.y: 116: 91
aux.x, aux.y: 120: 96
aux.x, aux.y: 130: 101
aux.x, aux.y: 140: 111
aux.x, aux.y: 145: 120
aux.x, aux.y: 154: 130
aux.x, aux.y: 164: 140
aux.x, aux.y: 169: 149
aux.x, aux.y: 178: 164
aux.x, aux.y: 188: 174
aux.x, aux.y: 193: 183
aux.x, aux.y: 202: 198
aux.x, aux.y: 207: 207
aux.x, aux.y: 217: 212
aux.x, aux.y: 222: 222
aux.x, aux.y: 231: 231
aux.x, aux.y: 236: 236
aux.x, aux.y: 241: 241
aux.x, aux.y: 246: 246
aux.x, aux.y: 246: 251
aux.x, aux.y: 251: 251
aux.x, aux.y: 251: 256
aux.x, aux.y: 251: 251
aux.x, aux.y: 246: 241
aux.x, aux.y: 246: 236
    '''