import pandas as pd
import os

def path(factor):
    # Still in abs path, need changes
    p=os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    path=os.path.join(p,'database')
    balance=set(pd.read_csv(path+'/AAPL/AAPL_balance.csv')['Statements'].tolist())
    if factor in balance:
        return 'balance'
    del balance
    income=set(pd.read_csv(path+'/AAPL/AAPL_income.csv')['Statements'].tolist())
    if factor in income:
        return 'income'
    del income
    cash_flow=set(pd.read_csv(path+'/AAPL/AAPL_cash_flow.csv')['Statements'].tolist())
    if factor in cash_flow:
        return 'cash_flow'
    del cash_flow
    trading=set(pd.read_csv(path+'/AAPL/AAPL_Trading_Information.csv')['0'].tolist())
    if factor in trading:
        return 'Trading_Information'
    del trading
    financial=set(pd.read_csv(path+'/AAPL/AAPL_Financial_Highlights.csv')['0'].tolist())
    if factor in financial:
        return 'Financial_Hightlights'
    del financial
    valuation=set(pd.read_csv(path+'/AAPL/AAPL_Valuation_Measures.csv')['0'].tolist())
    if factor in valuation:
        return 'Valuation_Measures'
    del valuation
    summary=set(list(pd.read_csv(path+'/AAPL/AAPL_Summary.csv')))
    if factor in summary:
        return 'Summary'
    del summary
    raise ValueError("Factor '"+factor+"' not in database")
