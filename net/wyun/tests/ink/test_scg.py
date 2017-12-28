from unittest import TestCase

from openpyxl import load_workbook
from net.wyun.mer.ink.scg import Scg
from net.wyun.mer.prep.xlsx import Excel




class TestScg(TestCase):

    def setUp(self):
        # Load in the workbook
        excel = Excel('data/scg/test.xlsx')
        scg_id, scg_content, truth, req_at, resp_at = excel.get_scg_record(1)
        self.scg1 = Scg(scg_id, scg_content, truth, req_at, resp_at)  # x + y

        scg_id, scg_content, truth, req_at, resp_at = excel.get_scg_record(2)
        self.scg2 = Scg(scg_id, scg_content, truth, req_at, resp_at)  # x + y

    def test_save_image1(self):
        self.scg1.save_image('temp/'  + str(self.scg1.id) + '.png')

    def test_get_latex1(self):
        latex = self.scg1.get_latex()
        print latex

    def test_save_image2(self):
        self.scg2.save_image('temp/'  + str(self.scg2.id) + '.png')

    def test_get_latex2(self):
        latex = self.scg2.get_latex()
        print latex
        aspect = self.scg2.w_h_ratio
        print 'aspect ratio: ', aspect
        print 'request_at: ', self.scg2.request_at
