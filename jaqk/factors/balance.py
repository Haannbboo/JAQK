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
