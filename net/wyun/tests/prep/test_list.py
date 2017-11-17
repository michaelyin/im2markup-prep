from unittest import TestCase
import pickle


class TestBatch(TestCase):

    def test_load_idlist(self):
        with open('data/batch/pickle/test.idlist', 'rb') as fin:
            idlist = pickle.load(fin)
            first = idlist[0]
            print first
            print type(first)
