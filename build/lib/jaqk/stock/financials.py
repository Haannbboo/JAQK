import pandas as _pd

import math as _math


from ..operations.Open import open_file as _open_file


def stats(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet with all statistics in yahoo finance for the company
    '''
    a=Valuation_Measures(stock)
    b=Financial_Highlights(stock)
    c=Trading_Information(stock)
    df=_pd.concat([a,b,c],ignore_index=True)
    return df
    


def Valuation_Measures(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet with Valuation Measures in statstics
    '''
    df=_open_file(stock, name='Valuation_Measures')
    return df


def Financial_Highlights(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet with Financial Highlishts in statistics
    '''
    df=_open_file(stock, name='Financial_Highlights')
    return df

def Trading_Information(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet with Trading Information in statistics
    '''
    df=_open_file(stock, name='Trading_Information')
    return df

def Cash_Flow(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet with cash flow statements in yahoo finance
    '''
    df=_open_file(stock, name='cash_flow')
    return df

def Balance(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet with balance  statements in yahoo finance
    '''
    df=_open_file(stock, name='balance')
    return df

def Income(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet with income statements in yahoo finance
    '''
    df=_open_file(stock, name='income')
    return df
