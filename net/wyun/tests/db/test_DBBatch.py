from unittest import TestCase
from net.wyun.mer.prep.dbbatch import DBBatch


class TestDBBatch(TestCase):
    def setUp(self):
        dbhost, dbuser, dbpass, dbname = 'localhost', 'hope', 'hope', 'equation'
        self.dbbatch = DBBatch(dbhost, dbuser, dbpass, dbname)

    def test_generate_db_idlists(self):
        self.dbbatch.generate_db_idlists()

    def test_generate_im2markup_files(self):
        self.dbbatch.generate_im2markup_files()


    def test_process_hw_record_table(self):
        '''
        generate png files for all hw_records
        :return:
        '''
        self.dbbatch.process_hw_record_table()
