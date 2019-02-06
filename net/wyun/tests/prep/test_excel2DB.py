from unittest import TestCase
from net.wyun.mer.prep.dbbatch import DBBatch
from net.wyun.mer.prep.xlsx2db import Excel2DB
from net.wyun.mer.ink.scg import Scg

class TestExcel2DB(TestCase):

    def setUp(self):
        dbhost, dbuser, dbpass, dbname = 'localhost', 'hope', 'hope', 'equation'
        dbbatch = DBBatch(dbhost, dbuser, dbpass, dbname)
        self.excel2db = Excel2DB(dbbatch, 'data/xlsx/hw_record.xlsx')

    def test_saveScg2db(self):
        self.excel2db.saveRow2db(1)

    def test_saveAllScgs(self):
        nrow = self.excel2db.excel.get_row_number()
        for i in range(1, nrow):
            print 'processing row: ', i
            self.excel2db.saveRow2db(i)


