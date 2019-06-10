import numpy as np

import sys as _sys
_sys.path.append('..') # add previous directory to model object

from operations.Format import factor as _factor
from operations.Open import open_file as _open_file

def FCF(stock): # Cash flow
    df=_open_file(stock,'cash_flow')
    OCF=_factor(df, 'Total Cash Flow From Operating Activities')
    CE=_factor(df, 'Capital Expenditures')
    
    return np.subtract(OCF,CE)




class cash_flow():
    def __init__(self,stock):
        self.__stock=stock
        self.__df=_open_file(stock,'cash_flow')
    def OCF(self):
        return _factor(self.__df, 'Total Cash Flow From Operating Activities')
    def CE(self):
        return _factor(self.__df, 'Capital Expenditures')
    def Net_Income(self):
        return _factor(self.__df, 'Net Income')
    def Depreciation(self):
        return _factor(self.__df, 'Depreciation')
    def Net_Borrowings(self):
        return _factor(self.__df, 'Net Borrowings')
