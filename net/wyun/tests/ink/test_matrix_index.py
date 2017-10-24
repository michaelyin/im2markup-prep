from unittest import TestCase
from net.wyun.mer.ink.sample import Sample

import numpy as np

'''
test fancy index on matrix
'''


class TestSample(TestCase):
    def setUp(self):
        m, n = 5, 6
        self.mat1 = a = np.arange(m * n).reshape(m, n)
        print '\n'


    def test_matrix_index1(self):
        '''
        test fancy index
        array of indices on the matrix
        used a lot in 2-D matrix value update
        :return:
        '''

        i = np.array([1, 3, 4, 3])
        j = np.array([2, 4, 5, 5])

        print self.mat1

        print self.mat1[i, j]
        # ==> mat1[1, 2], mat1[3, 4], mat1[4, 5] are set to 999
        self.mat1[i, j] = 999

        print "mat1 after: \n", self.mat1

    def test_matrix_index2(self):
        i = np.array([1, 3, 4])
        j = np.array([2, 4, 4])
        ij = np.vstack((i, j))

        print 'ij: \n', ij

        self.mat1[ij.T] = 100 # all rows except row 0 are set 0

        print "mat1 after: \n", self.mat1


