import sys as _sys
_sys.path.append('..') # add previous directory to model object

from operations.Open import open_file as _open_file


def Earnings_Estimate(stock):
    df=_open_file(stock, name='Earnings_Estimate')
    return df

def Earnings_History(stock):
    df=_open_file(stock, name='Earnings_History')
    return df

def EPS_Revisions(stock):
    df=_open_file(stock, name='EPS_Revisions')
    return df

def EPS_Trend(stock):
    df=_open_file(stock, name='EPS_Trend')
    return df

def Growth_Estimates(stock):
    df=_open_file(stock, name='Growth_Estimates')
    return df

def Revenue_Estimate(stock):
    df=_open_file(stock, name='Revenue_Estimate')
    return df
