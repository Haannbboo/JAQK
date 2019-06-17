import unittest as _unittest
# import os as _os
import numpy as _np
from .Open import open_file as _open_file
import os as _os
import pandas as _pd


class test_operations(_unittest.TestCase):
    def test_Folder(self):
        from .Folder import create_folder, p
        path = _os.path.join(p, 'operations')
        orig = _os.listdir(path)
        create_folder('test_folder', 'operations')
        self.assertEqual(len(orig), len(_os.listdir(path)))  # if exists - no change

        from .Folder import exist
        self.assertTrue(exist('AAPL', 'income'))
        self.assertFalse(exist('AAPL', 'oaijc', update=True))
        self.assertTrue(exist('AAPL', ['income', 'balance', 'cash_flow']))
        self.assertFalse(exist('AAPL', ['income', 'sdojvd', 'price_monthly']))
        with self.assertRaises(TypeError):
            exist('AAPL', 123)
            exist('AAPL', True)

    def test_Format(self):
        from .Format import _decimal
        t = _decimal(['302,32', '203,2304,2034.34', '1234,2345'])
        t2 = _np.array([30232.0, 20323042034.34, 12342345.0])
        self.assertEqual(len(t), len(t2))
        [self.assertEqual(t[i], t2[i]) for i in range(len(t))]
        self.assertEqual(len(t), 3)

        from .Format import factor as _factor  # hell a lot to test
        df = _open_file('AAPL', 'income')  # AAPL

        t = _factor(df, 'Total Revenue')
        self.assertGreaterEqual(len(t), 4)
        self.assertIsInstance(t, _np.ndarray)
        (self.assertEqual(_factor(df, 'Others')[i], 0) for i in range(len(t)))

        t = _factor(df, 'Total Revenue', year='NEWEST')  # newest year
        self.assertEqual(len(t), 1)
        self.assertIsInstance(t[0], _np.float64)

        t = _factor(df, 'Total Revenue', [2018, 2017])
        self.assertEqual(len(t), 1)  # [[data]]
        self.assertEqual(len(t[0]), 2)  # two years
        self.assertIsInstance(t[0][0], _np.float64)

        t = _factor(df, ['Total Revenue', 'Gross Profit'])
        self.assertEqual(len(t), 2)
        self.assertEqual(len(t[0]), 4)
        self.assertIsInstance(t, _np.ndarray)
        self.assertIsInstance(t[0], _np.ndarray)
        self.assertIsInstance(t[0][1], _np.float64)

        t = _factor(df, ['Total Revenue', 'Gross Profit', 'Others'])  # when factor is empty
        self.assertEqual(len(t), 3)
        self.assertGreaterEqual(len(t[2]), 4)
        [self.assertEqual(t[2][i], 0) for i in range(len(t[2]))]

        t = _factor(df, ['Total Revenue', 'Gross Profit', 'Others'], 'NEWEST')
        self.assertEqual(len(t), 1)
        self.assertEqual(len(t[0]), 3)
        self.assertIsInstance(t, _np.ndarray)
        self.assertIsInstance(t[0], _np.ndarray)
        self.assertIsInstance(t[0][0], _np.float64)

        t = _factor(df, ['Total Revenue', 'Gross Profit', 'Others'], [2017, 2018])
        self.assertEqual(len(t), 3)
        self.assertEqual(len(t[0]), 2)
        self.assertIsInstance(t[0], _np.ndarray)
        self.assertIsInstance(t[0][0], _np.float64)

        from .Format import _money_digits
        a = _np.array(['123', '234K', '34%'])
        b = _np.array([['12B', '34M', '2%']])
        c = _np.array(['12345'])
        good_a = _np.array(['123', '234000', '0.34'])
        good_b = _np.array([['12000000000', '34000000', '0.02']])
        aa = _money_digits(a)
        bb = _money_digits(b)
        self.assertEqual(len(b), 1)
        [self.assertEqual(aa[i], good_a[i]) for i in range(len(a))]
        [self.assertEqual(bb[i][j], good_b[i][j]) for i in range(len(b)) for j in range(len(b[0]))]
        self.assertEqual(c, c)
        self.assertIsInstance(bb, _np.ndarray)

    def test_Open(self):
        from .Open import open_file
        df = open_file('AAPL', 'income')
        self.assertIsInstance(df, _pd.core.frame.DataFrame)
        self.assertGreaterEqual(len(list(df)), 5)
        self.assertGreaterEqual(len(df), 22)
        self.assertIn('Total Revenue', df.iloc[0:-1, 0].values)
        self.assertIn('Net Income', df.iloc[0:-1, 0].values)
        self.assertIsInstance(df.index, _pd.core.indexes.range.RangeIndex)  # if index=True

        df = open_file('AAPL', 'price_monthly')
        self.assertGreaterEqual(len(list(df)), 6)
        self.assertIsInstance(df.Open[10], _np.float64)
        self.assertIsInstance(df.Date[10], str)

        df = open_file('AAPL', 'Summary')
        self.assertGreaterEqual(len(list(df)), 16)
        self.assertEqual(df.Stock.tolist(), ['AAPL'])

        with self.assertRaises((ValueError, FileNotFoundError, TypeError)):
            open_file('AAPL', '09ioijv')
            open_file('psldnld', 'vjsdf')
            open_file(['AAPL', 'AMZN'], 'income')
            open_file(12234, 'income')

        from .Open import open_general
        self.assertGreaterEqual(len(open_general('NASDAQ.csv')), 3000)
        self.assertGreaterEqual(len(open_general('NYSE.csv')), 3000)

    def test_Path(self):
        from .Path import path
        self.assertEqual(path('Total Revenue'), 'income')
        self.assertEqual(path('price_daily'), 'price_daily')
        with self.assertRaises(ValueError):
            path('notindatabase')

    def test_Save(self):
        from .Save import save_file
        from .Open import open_file
        df = _pd.DataFrame([['a', 1, 2], ['b', 2, 3], ['c', 5, 6], ['d', 10, 11]])  # setup
        df.columns = ['Statements', '01/01/2018', '02/01/2017']
        from .Folder import create_folder
        create_folder('test')
        save_file(df, 'test', 'income')  # save
        df = _pd.DataFrame([['a', 12, 1], ['b', 13, 2], ['c', 14, 5], ['d', 20, 10]])  # mimic update
        df.columns = ['Statements', '03/01/2019', '01/01/2018']
        save_file(df, 'test', 'income', update=True)

        df = open_file('test', 'income')  # start testing
        self.assertEqual(len(list(df)), 4)
        self.assertEqual(list(df)[1], '03/01/2019')
        self.assertEqual(df.iloc[0:-1, 1][0], 12)

        from .Save import save, datapath
        with self.assertRaises(ValueError):
            save(df, 'name', 'csv', test=True)  # '.csv'
        save(df, 'testClientSave', test=True)
        files = _os.listdir(_os.path.join(datapath, 'test'))
        self.assertIn('testClientSave', ''.join(files))
        _os.remove(_os.path.join(datapath, 'test', 'testClientSave.csv'))

        save(df, 'testClientSave2', '.xls', test=True)
        files = _os.listdir(_os.path.join(datapath, 'test'))
        self.assertIn('.xls', ''.join(files))
        _os.remove(_os.path.join(datapath, 'test', 'testClientSave2.xls'))

    def test_Tools(self):
        # database_count() and sheets_names() no need to test
        from .Tools import factors_names
        self.assertEqual(len(factors_names()), 182)
        self.assertEqual(len(factors_names('income')), 21)
        with self.assertRaises(ValueError):
            factors_names('notindatabase')

        from .Tools import code_count
        self.assertGreaterEqual(code_count(), 1888)
        self.assertIsInstance(code_count('lines', True), dict)
        self.assertGreaterEqual(code_count('defs'), 100)
        self.assertGreaterEqual(code_count('chars'), 62888)

        # not testing database_clear() now
        
