from ..operations.Format import factor as _factor
from ..operations.Open import open_file as _open_file


# These are quite important and popular factors, so I list them out
# so my client can use it like ROE-ROA, instead of factor(ROE)-factor(ROA), which is quite werid
def ROE(stock):  # Financial Highlights
    """
    Return on Equity - a measure of financial performance calculated by Net Income / Shareholders' Equity
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'Financial_Highlights')
    return _factor(df, 'Return on Equity (ttm)')


def ROA(stock):  # Financial Highlights
    """
    Return on Assets - an indicator of how profitable a company is relative to its total assets
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'Financial_Highlights')
    return _factor(df, 'Return on Assets (ttm)')


def EBITDA(stock):  # Financial Highlights
    """
    Earnings before Interest Taxes Depreciation Amortization - a measure of a company's overall financial performance and is used as an alternative to simple earnings or net income
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'Financial_Highlights')
    return _factor(df, 'EBITDA')
