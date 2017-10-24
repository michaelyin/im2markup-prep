from unittest import TestCase
from net.wyun.mer.ink.sample import Sample
from scipy import misc

import numpy as np

'''
all tests in this module and test_stroke.py are base on file data/inkml/65_alfonso.inkml
'''


class TestSample(TestCase):
    def setUp(self):
        self.idd = Sample('data/inkml/65_alfonso.inkml')
        self.stroke0 = self.idd.traces[0]
        self.stroke1 = self.idd.traces[1]
        self.stroke2 = self.idd.traces[2]
        prev = self.idd.traces[1]


    def test_get_bounding_box_h1000(self):
        self.assertEqual((0, 0, 69622, 10000), (self.idd.ox, self.idd.oy, self.idd.os, self.idd.ot))

    def test_getAVGstroke_size(self):
        avgW, avgH = self.idd.getAVGstroke_size()
        targetW = 6075.5
        targetH = 4320.8999
        self.assertTrue(abs(avgW - targetW) < 1.0 / 2)
        self.assertTrue(abs(avgH - targetH) < 1.0 / 2)
        print avgW, avgH

    def test_nStrokes(self):
        ns = self.idd.nStrokes()
        self.assertEquals(10, ns)

    def test_detRefSymbol(self):
        '''
        expect (5764, 5063)
        :return:
        '''
        RX, RY = self.idd.detRefSymbol()
        print RX, RY
        self.assertEquals((5764, 5063), (RX, RY))

    def test_stroke_aspect_area(self):
        # expect 9623, 6794, 1.41639686, 65378662
        i = 0
        ancho, alto, aspectratio, area = self.idd.stroke_aspect_area(i)
        print ancho, alto, aspectratio, area
        self.assertEquals(9623, ancho)
        self.assertEquals(6794, alto)
        self.assertEquals(65378662, area)
        self.assertAlmostEqual(1.41639686, aspectratio)

    def test_median_vmedx(self):
        vmedx = [9623, 6039, 7360, 7360, 6982, 4152, 3586, 3586, 6793, 5284]
        print vmedx
        vmedx.sort()
        print vmedx
        l = len(vmedx)
        print vmedx[l / 2]
        self.assertEquals(6793, vmedx[l / 2])
        import numpy
        medx = numpy.median(vmedx)  # average of 6039 and 6793
        self.assertEquals(6416.0, medx)

    def test_stroke_distance1(self):
        self.idd.render()
        # distance between stroke 0 and stroke 2. the distance is before the normalization
        dmin = self.idd.stroke_distance(0, 2)
        self.assertEqual(7902.4310183639063, dmin)
        print dmin

    def test_stroke_distance2(self):
        img, W, H = self.idd.render()
        dmin = self.idd.stroke_distance(4, 7)
        print dmin

    def test_find_closest_pair(self):
        dmin, p1, p2 = self.idd.find_closest_pair(0, 2)
        print dmin
        self.assertAlmostEqual(7902.43115, dmin, 3)
        self.assertEqual((9433, 9056), p1)
        self.assertEqual((16037, 4716), p2)

    def test_render(self):
        '''
        testing rendering image from inkml file
        save image at temp/all.png
        :return:
        '''
        img, W, H = self.idd.render()
        print 'save image to temp/all.png: '
        misc.imsave('temp/all.png', img)
        print img[15, 9]
        print W, H
        self.assertEqual(255, img[15, 9])
        self.assertEqual((1792, 266), (W, H))

    def test_linea(self):
        W, H = 1792, 266
        img = np.ones((H, W), dtype=int) * 255
        self.idd.pix_stk = np.ones((H, W), dtype=int) * (-1)
        pa = (19.4867649, 149.881516)
        pb = (5, 145.043594)

        self.idd.linea(img, pa, pb, 0)
        print np.where(img == 0)
        print img

        self.assertEqual(0, img[145, 5])
        self.assertEqual(0, img[150, 20])

    def test_compute_strokes_distances(self):
        RX = 5764
        RY = 5063
        img, W, H = self.idd.render()
        stk_dis = self.idd.compute_strokes_distances(RX, RY)

        print '(x, y): (1169, 119): ', img[119][1169], self.idd.pix_stk[119][1169]
        self.assertEqual(0, img[119][1169])
        self.assertEqual(5, self.idd.pix_stk[119][1169])
        print stk_dis


    def test_get_close_strokes(self):
        self.idd.detRefSymbol()
        self.idd.render()
        self.idd.compute_strokes_distances(self.idd.RX, self.idd.RY)
        L = []
        self.idd.get_close_strokes(7, L, 0.69474973)
        self.assertEqual((6, 5), (L[0], L[1]))
        print L

        L = []
        self.idd.get_close_strokes(6, L, 0.69474973)
        self.assertEqual(5, L[0])

        L = []
        self.idd.get_close_strokes(8, L, 0.69474973)
        self.assertEqual((7, 6), (L[0], L[1]))
