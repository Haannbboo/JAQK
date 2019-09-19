import pandas as _pd

from ..operations.Open import open_general as _open_general


def stock_list(exchange=True):
    """Read the stock list in database.

    Open stock list files in database using open_general() function.

    Args:
        exchange: str - default True (all stocks), or either NYSE or NASDAQ.

    Returns:
        a csv format file with ticket names (rows) vs [Open, Close, High, Close, Adj. Close, Vol] (columns)

    Raises:
        ValueError: error assessing exchange param.
    """

    if exchange not in ['NYSE', 'NASDAQ'] and exchange != True:
        raise ValueError("Parameter 'exchange' should either NYSE or NASDAQ")

    if exchange is True:  # all tickets
        c1 = _open_general('NASDAQ')
        c2 = _open_general('NYSE')
        df = _pd.concat([c1, c2], ignore_index=True).drop('Unnamed: 9', axis=1)  # drop duplicated column
    else:
        _csv = _open_general(exchange)
        df = _csv.drop('Unnamed: 9', axis=1)
    return df
