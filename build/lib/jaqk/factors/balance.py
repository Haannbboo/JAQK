from ..operations.Format import factor as _factor
from ..operations.Open import open_file as _open_file


def _IC(df):  # Balance
    """Invested Capital - following calculations on investopedia.com"""
    # No adjustments for cash-flow and off-balance sheet yet
    return Invested_Book_Capital(df)


def _NIBCLS(df):
    accounts_payable = _factor(df, 'Accounts Payable')  # Balance
    other_current_liabilities = _factor(df, 'Other Current Liabilities')  # Balance
    return accounts_payable + other_current_liabilities


def _Invested_Book_Capital(df):  # Balance
    total_assets = _factor(df, 'Total Assets')
    return total_assets - _NIBCLS(df)


def _CAGR():
    pass


def IC(stock):
    """
    Invested Capital - following calculations on investopedia.com
    stock - company name (e.g AAPL for apple inc.)
    """
    return Invested_Book_Capital(stock)


def Invested_Book_Capital(stock):
    """
    Invested Book Capital - a component for calculating invest capital
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'balance')
    return _Invested_Book_Capital(df)


def NIBCLS(stock):
    """
    NIBCLS - account payable + other current liabilities
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'balance')
    return _NIBCLS(df)


def Total_Assets(stock):
    """
    Total Assets - resource with economic value that the company owns with the expectation of its future benefit
    stock - company name (e.g AAPL for apple inc.)
    """
    return _factor(_open_file(stock, 'balance'), 'Total Assets')


# the following will be used for the class-base module
'''
class balance():
    def __init__(self,stock):
        self.__stock=stock
        self.__df=_open_file(stock,'balance')
    def Total_Assets(self):
        return _factor(self.__df, 'Total Assets')
    def Accounts_Payable(self):
        return _factor(self.__df, 'Accounts Payable')
    def Long_Term_Debt(self):
        return _factor(self.__df, 'Long Term Debt')
    def Total_Liabilities(self):
        return _factor(self.__df, 'Total Liabilities')
    def Net_Tangible_Assets(self):
        return _factor(self.__df, 'Net Tangible Assets')
    def Total_Stockholder_Equity(self):
        return _factor(self.__df, 'Total Stockholder Equity')
'''
