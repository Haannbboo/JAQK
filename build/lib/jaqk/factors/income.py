from ..operations.Format import factor as _factor
from ..operations.Open import open_file as _open_file


def Total_Revenue(stock):
    """
    Total Revenue - total money received by a company
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'income')
    return _factor(df, 'Total Revenue')


def Cost_of_Revenue(stock):
    """
    Cost of Revenue - usually used with CoR/TR (total revenue), indicating stable financial health and possible strong sales
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'income')
    return _factor(df, 'Cost of Revenue')


def Gross_Profit(stock):
    """
    Gross Profit - profits company makes after deducting the costs associated with making and selling its products 
    stock - company name (e.g AAPL for apple inc.)
    """
    df = _open_file(stock, 'income')
    return _factor(df, 'Gross Profit')
