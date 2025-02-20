import unittest

from src.matop.row import Row


class TestRow(unittest.TestCase):
    def setUp(self):
        self.row1 = Row(1, 2, 3)
        self.row2 = Row(4, 5, 6)

    def test_nums_property(self):
        self.assertEqual(self.row1.nums, [1, 2, 3])
        
    def test_mul_by_col(self):
        column = [7, 9, 11]
        self.assertEqual(self.row1.mul_by_col(column), 58)
        
    def test_mul_by_scalar(self):
        self.row1.mul_by_scalar(scalar=5)
        self.assertEqual(self.row1.nums, [5, 10, 15])
      
    # operator tests  
    def test_add(self):
        rows_sum = self.row1 + self.row2
        self.assertEqual(rows_sum.nums, [5,7,9])
        
    def test_eq(self):
        self.assertEqual(self.row1.nums, [1,2,3])
        
        self.assertFalse(self.row1 == self.row2)
 