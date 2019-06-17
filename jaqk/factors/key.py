from ..operations.Open import open_file as _open_file
from ..operations.Format import _decimal


def Beta(stock):  # Valuation Measures
    """
    Beta coefficient - a measure of the volatility of a company compared to entire market, popularly used in capital asset pricing model (CAPM)
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'Valuation_Measures')

    bt = _decimal(df[df['0'].isin(['Beta (3Y Monthly)'])].values[0][1:])
    return bt
