import numpy as _np

from ..operations.Format import factor as _factor
from ..operations.Open import open_file as _open_file


def FCF(stock):  # Cash flow
    """
    FCF - free cash flow, indicating companies 'real' cash, an important valuation measure
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'cash_flow')
    OCF = _factor(df, 'Total Cash Flow From Operating Activities')
    CE = _factor(df, 'Capital Expenditures')

    return _np.subtract(OCF, CE)


'''
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
'''
