import sys as _sys
_sys.path.append('..') # add previous directory to model object

from operations.Format import _decimal


def total_assets(df): # Balance
    TA=_decimal(df[df['Period Ending'].isin(['Total Assets'])].values[0][1:])
    return TA

def Beta(df): # Valuation Measures
    bt=_decimal(df[df['0'].isin(['Beta (3Y Monthly)'])].values[0][1:])
    return bt
