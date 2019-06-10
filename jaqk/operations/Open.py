import os
import pandas as pd

import gc as _gc

import sys as _sys

_sys.path.append('..')  # add previous directory to model object
from operations.Path import path as _path

p = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

global datapath
datapath = os.path.join(p, 'database')


def open_file(stock, name):
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
    path = os.path.join(datapath, stock, stock)
    try:
        df = pd.read_csv(path + '_' + name + '.csv')
    except FileNotFoundError:
        raise ValueError("There is no record of '" + stock + "' in database")
    _gc.collect()
    return df


def open_general(file):
    path = os.path.join(datapath, 'general')
    p = os.path.join(path, file)
    df = pd.read_csv(p)
    return df


def open_dfs(ffactor):  # Not used yet, design for reduce IOs
    """return a generator"""
    p = '/Users/hanbo/Desktop/ML/QA/JAQK/database/'
    name = _path(ffactor)
    dirs = os.listdir(p)
    d = [i for i in dirs if
         os.path.isdir(os.path.join(p, i)) and os.path.exists(os.path.join(p, i, i) + '_' + name + '.csv')]
    print(len(d))
    dfs = (open_file(i, name) for i in d)
    return dfs
