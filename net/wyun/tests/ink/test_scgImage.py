from unittest import TestCase
from net.wyun.mer.prep.xlsx import Excel
from net.wyun.mer.ink.scgimage import ScgImage
import json


class TestScgImage(TestCase):

    def setUp(self):
        # Load in the workbook
        excel = Excel('data/scg/test.xlsx')
        scg_id, scg_content, truth, dt1, dt2 = excel.get_scg_record(1)
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

    def test_scg_file_bug(self):
        num = str(610)
        file_name = 'temp/2018-09-17/' + num + '_scg.txt'
        with open(file_name, 'r') as myfile:
            data = myfile.read()

        print data
        scg = ScgImage(data, num)
        scg.save_image('temp/' + num + '.png')
