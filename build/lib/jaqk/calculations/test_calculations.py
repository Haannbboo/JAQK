import unittest as _unittest

class test_calculations(_unittest.TestCase):
    def test_rank(self):
        # this take a hell long time
        from .rank import factor_percentile, percentile
        self.assertGreater(len(factor_percentile('Total Revenue', 'AAPL')), 3)
        self.assertIsInstance(percentile('Total Assets', 80), list)
        with self.assertRaises(TypeError):
            factor_percentile('Total Revenue', ['AAPL', 'AMZN'])
            factor_percentile(['Total Revenue', 'Gross Profit'], 'AAPL')
            percentile([1,2,3], 10)
            percentile('Total Revenue', '80')
        with self.assertRaises(ValueError):
            percentile('Total Revenue', 120)
            percentile('lajlsdv', 99)
            factor_percentile('oidcdlewuh', 'AAPL')
            factor_percentile('Total Revenue', 'ofisuq')
