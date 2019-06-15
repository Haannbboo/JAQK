import unittest as _unittest
import pandas as _pd
from numpy import ndarray as _ndarray


class test_factors(_unittest.TestCase):
    def test_balance(self):
        from .balance import IC, Invested_Book_Capital, NIBCLS, Total_Assets
        
        f=lambda c: [IC(c), Invested_Book_Capital(c),
                     NIBCLS(c), Total_Assets(c)]
        t=f('AAPL')
        self.assertEqual(len(t), 4)
        [self.assertEqual(len(_), 4) for _ in t]
        self.assertIsInstance(t[0], _ndarray)
        with self.assertRaises(ValueError):
            f('adfjsiojda')
        del t, f
       
    def test_cash_flow(self):
        from .cash_flow import FCF
        t=FCF('AAPL')
        self.assertEqual(len(t), 4)
        self.assertIsInstance(t, _ndarray)

        with self.assertRaises((ValueError, TypeError)):
            FCF('aosdij') # value
            FCF(12345) # type
            FCF(['AAPL','AMZN'])
            FCF(True)
        del t
       
    def test_income(self):
        from .income import Total_Revenue, Cost_of_Revenue, Gross_Profit
        
        f=lambda c: [Total_Revenue(c), Cost_of_Revenue(c), Gross_Profit(c)]
        t=f('AAPL')
        self.assertEqual(len(t), 3)
        self.assertIsInstance(t[0],  _ndarray)
        self.assertGreater(len(t[1]), 3)
        with self.assertRaises(ValueError):
            f('akjdcdc')
        del t, f
            
    def test_stats(self):
        from .stats import ROE, ROA, EBITDA
        
        f=lambda c: [ROE(c), ROA(c), EBITDA(c)]
        t=f('AAPL')
        self.assertIsInstance(f('AAPL'), list)
        self.assertGreater(len(t[0]), 3)
        self.assertIsInstance(t[1], _ndarray)
        with self.assertRaisesRegex(TypeError, "Parameter 'stock' should be a string, not a list"):
            f(['AAPL', 'AMZN'])

        with self.assertRaises(ValueError):
            f('aoijdsoigjs')
        del f, t

    def test_key(self):
        from .key import Beta
        t=Beta('AAPL')
        self.assertIsInstance(t, _ndarray)
            
            


