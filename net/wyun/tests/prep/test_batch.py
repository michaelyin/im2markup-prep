from unittest import TestCase
from net.wyun.mer.prep.batch import Batch
import pickle


class TestBatch(TestCase):
    def setUp(self):
        inkml_path = 'data/batch/inkml'
        id_path = 'data/xlsx'
        self.batch = Batch(inkml_path, id_path)

    # inkml file lists: train.flist, validate.flist, and test.flist in data/batch/pickle
    def test_generate_lists(self):
        # inkml_path = '/home/michael/temp/math_hwreco/data/batch/inkml/cuda2z'
        self.batch.generate_filelists()

    # from the flist file, generate following files
    # 1. png files for each inkml file in the flist
    # 2. im2latex_formulas.lst file contains latex truth from each inkml file
    # 3. im2latex_train.lst, im2latex_validate.lst, and im2latex_test.lst
    def test_generate_im2markup_files(self):
        self.batch.generate_im2markup_files()

    # do above two tests in on step
    def test_all(self):
        print 'generate lists now ...'
        self.test_generate_lists()
        self.test_generate_im2markup_files()

    def test_generate_scg_idlists(self):
        self.batch.generate_scg_idlists()
