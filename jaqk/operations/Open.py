import os as _os
import pandas as _pd

import gc as _gc


from ..operations.Path import path as _path

p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
global datapath
datapath = _os.path.join(p, 'database')


def open_file(stock, name):
    """
    opener for opening sheets for client
    stock - company name (e.g AAPL for apple inc.)
    name - name of the sheet (e.g 'income' / 'balace'), use sheets_names() to see all names
    returns a csv sheet of the sheet of the company
    """
    # datapath='/Users/hanbo/Desktop/ML/QA/JAQK/database/'
    if not isinstance(stock, str):
        raise TypeError("Parameter 'stock' should be a string, not a "
                        + type(stock).__name__)
    names = ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders',
             'Trading_Information', 'Financial_Highlights', 'Valuation_Measures',
             'Executives', 'Description',
             'Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates',
             'stats', 'statements', 'reports',
             'Executives', 'Description', 'analysis', 'Summary',
             'balance', 'cash_flow', 'income']
    if name not in names:
        try:
            name = _path(name)
        except ValueError:
            raise ValueError(
                'Parameter "name" should be the name of the financial sheets, not a factor name...Use path method to find the location of a factor')
    path = _os.path.join(datapath, stock, stock)
    try:
        df = _pd.read_csv(path + '_' + name + '.csv')
    except FileNotFoundError:
        raise ValueError("There is no record of '" + stock + "' in database")
    _gc.collect()
    return df


def open_general(file):
    try:
        path = _os.path.join(datapath, 'general')
        p = _os.path.join(path, file)
        df = _pd.read_csv(p)
    except Exception as e:
        print("Something wrong in opening the stock list: "+str(e))
    return df


def open_dfs(ffactor):  # Not used yet, design for reduce IOs
    """return a generator"""
    p = '/Users/hanbo/Desktop/ML/QA/JAQK/database/'
    name = _path(ffactor)
    dirs = _os.listdir(p)
    d = [i for i in dirs if
         _os.path.isdir(_os.path.join(p, i)) and _os.path.exists(_os.path.join(p, i, i) + '_' + name + '.csv')]
    print(len(d))
    dfs = (open_file(i, name) for i in d)
    return dfs
