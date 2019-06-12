import os
import pandas as pd


from ..operations.Open import open_file as _open_file


def daily(stock, start=None, end=None):
    '''
    get daily historical price
    start & end -> time, e.g 2017-01-01
    returns a csv sheet
    '''
    df=_open_file(stock, name='price_daily')
    if start is not None:
        df=df[df.Date >= start]
    if end is not None:
        df=df[df.Date <= end]
    return df

def weekly(stock, start=None, end=None):
    '''
    get weekly historical price
    start & end -> time, e.g 2017-01-01
    returns a csv sheet
    '''
    df=_open_file(stock, name='price_weekly')
    if start is not None:
        df=df[df.Date >= start]
    if end is not None:
        df=df[df.Date <= end]
    return df

def monthly(stock, start=None, end=None):
    '''
    get monthly historical price
    start & end -> time, e.g 2017-01-01
    returns a csv sheet
    '''
    df=_open_file(stock, name='price_monthly')
    if start is not None:
        df=df[df.Date >= start]
    if end is not None:
        df=df[df.Date <= end]
    return df




    
