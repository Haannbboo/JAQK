import unittest as _unittest
from .__init__ import *
from .profile import description
import pandas as _pd


class test_stocks(_unittest.TestCase):
    def test_analysis(self):
        
        f=lambda c: [EPS_Revisions(c), EPS_Trend(c),
                     Growth_Estimates(c), Revenue_Estimate(c),
                     Earnings_Estimate(c), Earnings_History(c)]
        self.assertEqual(len(f('AAPL')), 6)
        with self.assertRaises(ValueError):
            f('adfjsiojda')
       
    def test_financials(self):
        df=stats('AAPL')
        self.assertIsInstance(df, _pd.core.frame.DataFrame)
#        self.assertEqual(stats('aoidfjso'), "Something wrong with the data for stats for {}".format(stock))
        f=lambda c: {Valuation_Measures(c), Financial_Highlights(c),
                     Trading_Information(c), Cash_Flow(c),
                     Balance(c), Income(c)}
        with self.assertRaises((ValueError, TypeError)):
            f('aosdij') # value
            f(12345) # type
            f(['AAPL','AMZN'])
            f(True)
       
    def test_prices(self):
        f=lambda c, t1, t2: (daily(c), daily(c, t1), daily(c, t1, t2),
                             weekly(c), weekly(c, t1), weekly(c, t1, t2),
                             monthly(c), monthly(c, t1), monthly(c, t1, t2))
        self.assertIsInstance(f('AAPL', '2018-12-01', '2019-05-01'),  tuple)
        self.assertGreater(len(daily('AAPL', '2018-12-01', '2019-05-01')), 5) # avoid empty
        with self.assertRaises(ValueError):
            f('kjdnsdnv', '2018-12-01', '2019-05-01')
            
    def test_profile(self):
        f=lambda c: [Key_Executives(c), summary(c), description(c)]
        self.assertIsInstance(f('AAPL'), list)
#        self.assertIsInstance(description('AAPL', 'zh'), str) # translation
#        with self.assertRaisesRegex(KeyError, 'trans_result'):
#            description('AAPL', 'ladkjsdlv')
        with self.assertRaises(ValueError):
            f('aoijdsoigjs')
            
            


