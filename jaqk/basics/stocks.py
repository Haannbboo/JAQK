import pandas as _pd

from ..operations.Open import open_general as _open_general


def stock_list(exchange=True):
    """
    exchange - str - default True (all), either NYSE or NASDAQ
    returns a csv sheet with all statistics in yahoo finance for the company
    """
    if exchange not in ['NYSE', 'NASDAQ'] and exchange != True:
        raise ValueError("Parameter 'exchange' should either NYSE or NASDAQ")
    if exchange:
        c1 = _open_general('NASDAQ.csv')
        c2 = _open_general('NYSE.csv')
        df = _pd.concat([c1, c2], ignore_index=True).drop('Unnamed: 9', axis=1)  # drop duplicated column
    else:
        _csv = _open_general(exchange + '.csv')
        df = _csv.drop('Unnamed: 9', axis=1)
    return df
