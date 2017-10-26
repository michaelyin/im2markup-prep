from unittest import TestCase
from net.wyun.mer.prep.batch import Batch


class TestBatch(TestCase):
    def setUp(self):
        inkml_path = 'data/batch/inkml'
        self.batch = Batch(inkml_path)

    def test_process(self):
        # inkml_path = '/home/michael/temp/math_hwreco/data/batch/inkml/cuda2z'
        self.batch.generate_lists()

    def test_generate_im2markup_files(self):
        self.batch.generate_im2markup_files()
