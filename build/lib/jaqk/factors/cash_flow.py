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
