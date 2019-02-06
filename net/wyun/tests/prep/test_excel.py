from unittest import TestCase
from net.wyun.mer.prep.xlsx import Excel
from net.wyun.mer.ink.scg import Scg

#1509268610519

class TestExcel(TestCase):

    def setUp(self):
        self.excel = Excel('data/xlsx/hw_record.xlsx')

    def test_get_scg_requestat(self):
        scg_id, scg_content, truth, req_at, resp_at = self.excel.get_scg_record(2)
        scg = Scg(scg_id, scg_content, truth, req_at, resp_at)
        print 'request_at: ', scg.request_at
        self.assertEquals(str(req_at), '2017-10-24 15:46:32')  #convert req_at to str

    def test_saving_image(self):
        self.excel.load_all_scgs()  # read all records from xlsx file
        id = 1509369509259  # fix error
        scg = self.excel.scgs[id]
        scg.save_image('temp/' + str(id) + '.png')

    def test_saving_image_bugfix2(self):
        id = 1509239879109  # fix error, latex '1'
        scg = self.excel.scgs[id]
        print 'latex is 1? ', scg.get_latex() == '1'
        scg.save_image('temp/' + str(id) + '.png')

    # test causes Memory Error
    def test_bugfix_1509259382091(self):
        test_id = 1509259382091
        row = 12312
        id, content, truth, req_at, resp_at = self.excel.get_scg_record(row)
        print id
        self.assertEquals(test_id, id)

        scg = Scg(id, content, truth, req_at, resp_at)
        scg.save_image('temp/' + str(id) + '.png')
    # Memory error
    def test_bugfix_1509714111470(self):
        test_id = 1509714111470
        row = 21838
        id, content, truth, req_at, resp_at = self.excel.get_scg_record(row)
        self.assertEquals(test_id, id)

        scg = Scg(id, content, truth, req_at, resp_at)
        print id
        scg.save_image('temp/' + str(id) + '.png')