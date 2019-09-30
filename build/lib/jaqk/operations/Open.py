import os as _os
import pandas as _pd

import gc as _gc

from ..operations.Path import path as _path
from ..operations.Path import datapath


def open_file(stock, name, setup=False):
    """
    opener for opening sheets for client
    stock - company name (e.g AAPL for apple inc.)
    name - name of the sheet (e.g 'income' / 'balace'), use sheets_names() to see all names
    returns a csv sheet of the sheet of the company
    """
    if not isinstance(stock, str):
        raise TypeError("Parameter 'stock' should be a string, not a "
                        + type(stock).__name__)
    if setup is True:  # when setup, name is "AAPL_income.csv", not "income"
        # path = _os.path.join(datapath(setup=False), stock, name)
        path = datapath(True, stock, name)
        df = _pd.read_csv(path)
        _gc.collect()
        return df
    # not setup, normal open_file
    names = ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders',
             'Trading_Information', 'Financial_Highlights', 'Valuation_Measures',
             'Executives', 'Description',
             'Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates',
             'stats', 'statements', 'reports',
             'Executives', 'Description', 'analysis', 'Summary',
             'balance', 'cash_flow', 'income']
    if name not in names:
        try:
            name = _path(name)  # when client mistakenly input factor instead of sheet name
        except ValueError:
            raise ValueError(
                'Parameter "name" should be the name of the financial sheets, not a factor name...Use path method to '
                'find the location of a factor')
    path = datapath(True, stock, stock)
    try:
        df = _pd.read_csv(path + '_' + name + '.csv')
        _gc.collect()
    except FileNotFoundError:
        _gc.collect()
        if _os.path.exists(datapath(True, stock)):
            raise ValueError("There is no sheet - {} - for company {}. Use main_get to retrieve the sheet".format
                             (name, stock))
        else:
            raise ValueError("There is no record of '" + stock + "' in database")
    return df


def open_general(file, setup=False):
    """Read CSV in folder "general" in database. Also used in setup.py

    Args:
        file: str - file name, need '.csv'.
        setup: bool - setup flag, indicate usage by setup or not.

    Returns:
        df - dataframe of stock list
        if FileNotFound, print out suggestions
    """
    try:
        if setup is False:
            p = datapath(True, 'general', file)
            df = _pd.read_csv(p + '.csv')
        elif setup is True:
            p = datapath(True, 'general', file)
            df = _pd.read_csv(p + '.py')
        else:
            df = None  # not tested here
        return df
    except FileNotFoundError as e:
        print("There is no record of {} in your database. Go to your chosen setup path to check, if not there go to "
              "Github and download the missing sheet".format(file))
        return None


def open_stock_list(exchange='ALL'):
    """Read the stock list in database, a wrap up of open_general.

    Open stock list files in database using open_general() function.

    Args:
        exchange: str - default True (all stocks), or either NYSE or NASDAQ.

    Returns:
        a csv format file with ticket names (rows) vs [Open, Close, High, Close, Adj. Close, Vol] (columns)

    Raises:
        ValueError: error assessing exchange param.
    """
    if exchange not in ['NYSE', 'NASDAQ'] and exchange != 'ALL':
        raise ValueError("Parameter 'exchange' should either NYSE or NASDAQ")

    if exchange == 'ALL':  # all tickets
        c1 = open_general('NASDAQ')
        c2 = open_general('NYSE')
        df = _pd.concat([c1, c2], ignore_index=True).drop('Unnamed: 9', axis=1)  # drop duplicated column
    else:
        _csv = open_general(exchange)
        df = _csv.drop('Unnamed: 9', axis=1)
    return df

