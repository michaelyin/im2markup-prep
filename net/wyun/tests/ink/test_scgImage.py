from unittest import TestCase
from net.wyun.mer.prep.xlsx import Excel
from net.wyun.mer.ink.scgimage import ScgImage
import json


class TestScgImage(TestCase):

    def setUp(self):
        # Load in the workbook
        excel = Excel('data/scg/test.xlsx')
        scg_id, scg_content, truth = excel.get_scg_record(1)
        self.scg = ScgImage(scg_content, scg_id)  # x + y


    def test_save_image(self):
        self.scg.save_image('temp/' + str(self.scg.id) + '.png')


    def test_scg_file(self):
        scgink  = json.load(open('data/x_+_y_square.json'))
        print '\n', scgink
        print '\n', scgink['scg_ink']

        ink = scgink['scg_ink']
        scg = ScgImage(ink, 999)
        scg.save_image('temp/' + str(999) + '.png')

