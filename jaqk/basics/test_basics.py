import unittest as _unittest


class test_basics(_unittest.TestCase):
    def test_stocks(self):
        from .stocks import stock_list
        self.assertGreater(len(stock_list()), 6000)
        self.assertGreater(len(stock_list('NYSE')), 3000)
        self.assertGreater(len(stock_list('NASDAQ')), 3000)
        with self.assertRaises(ValueError):
            stock_list('abcdefg')
            stock_list([1,2,3])
            stock_list(True)
