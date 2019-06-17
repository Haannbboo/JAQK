import pandas as _pd
import os as _os


def path(factor):
    """
    factor - str - factor name (use names() to find out all factor names included)
    returns the file name of the factor (e.g path('Total Assets') gives 'balance')
    """
    # can be a loop or sommething
    # Still in abs path, need changes
    p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
    path = _os.path.join(p, 'database')
    if factor in ['price_daily', 'price_monthly', 'price_weekly']:
        return factor
    balance = set(_pd.read_csv(path + '/AAPL/AAPL_balance.csv')['Statements'].tolist())
    if factor in balance:
        return 'balance'
    del balance
    income = set(_pd.read_csv(path + '/AAPL/AAPL_income.csv')['Statements'].tolist())
    if factor in income:
        return 'income'
    del income
    cash_flow = set(_pd.read_csv(path + '/AAPL/AAPL_cash_flow.csv')['Statements'].tolist())
    if factor in cash_flow:
        return 'cash_flow'
    del cash_flow
    trading = set(_pd.read_csv(path + '/AAPL/AAPL_Trading_Information.csv')['0'].tolist())
    if factor in trading:
        return 'Trading_Information'
    del trading
    financial = set(_pd.read_csv(path + '/AAPL/AAPL_Financial_Highlights.csv')['0'].tolist())
    if factor in financial:
        return 'Financial_Hightlights'
    del financial
    valuation = set(_pd.read_csv(path + '/AAPL/AAPL_Valuation_Measures.csv')['0'].tolist())
    if factor in valuation:
        return 'Valuation_Measures'
    del valuation
    summary = set(list(_pd.read_csv(path + '/AAPL/AAPL_Summary.csv')))
    if factor in summary:
        return 'Summary'
    del summary
    raise ValueError("Factor '" + factor + "' not in database")
