import pandas as _pd

import math as _math

import sys as _sys
_sys.path.append('..') # add previous directory to model object

from operations.Open import open_file as _open_file


def stats(stock):
    a=Valuation_Measures(stock)
    b=Financial_Highlights(stock)
    c=Trading_Information(stock)
    df=_pd.concat([a,b,c],ignore_index=True)
    return df


def Valuation_Measures(stock):
    df=_open_file(stock, name='Valuation_Measures')
    return df


def Financial_Highlights(stock):
    df=_open_file(stock, name='Financial_Highlights')
    return df

def Trading_Information(stock):
    df=_open_file(stock, name='Trading_Information')
    return df

def Cash_Flow(stock):
    df=_open_file(stock, name='cash_flow')
    return df

def Balance(stock):
    df=_open_file(stock, name='balance')
    return df

def Income(stock):
    df=_open_file(stock, name='income')
    return df
