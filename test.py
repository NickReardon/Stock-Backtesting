from algos import sma,ema

import unittest

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        # Initialize data
        self.data = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 
            40]  # Example closing prices for 30 days

    def test_sma(self):
        self.assertEqual(sma(5, 25, self.data), 32.0)

    def test_ema(self):
        self.assertEqual(round(ema(5, 25, self.data)), 33) 

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
