from unittest import TestCase

class TestSample(TestCase):
    def setUp(self):
        # set up all numbers
        self.num_list  = []
        for i in range(1, 31):
            current = self.generate(i)
            self.num_list.append(current)

    def test_sum_10digits(self):
        total = 0
        for num in self.num_list:
            print '\n', num
            total += num
        print '\n', total

    def generate(self, ind):
        sum = 0
        for i in range(0, ind):
            sum += 10 ** i
        return sum