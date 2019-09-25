import asyncio

import time as _time
import random

from ..operations.Tools import sheet_names
from ..operations.Open import open_stock_list, open_general
from ..operations.Path import datapath
from .parse_main import parse


def main(stocks='SP100', sheets='financials', batch=32, update=False, exception=False, error_cache=False):
    """Main asynchronous coroutine loop.

    It creates async tasks and put them into async loop for parse() and prints out the progress.

    Args:
        stocks: str/list - 'NYSE' or 'NASDAQ' or list of tickets (e.g ['AAPL', 'AMZN', 'BABA']).
        sheets: list - passed in from main_get(), sheets that will be parsed.
        update: bool - identify if this parse() is used for update(), pass into parse(update=update).
        batch: int - batch size, passed in from main_get()
        exception: bool - prints out exception or not, pass into parse(exception=exception)

    Returns:
        None (but will save files to database and prints out the parsing progress)

    Raises:
        TypeError: check if param stocks is a list
    """
    name = stocks
    if stocks not in ['NYSE', 'NASDAQ', 'ALL', 'SP100'] and isinstance(stocks, str):
        # when stocks is nonesense
        t = type(stocks)
        stocks_error = stocks
        if len(stocks) > 10:
            stocks_error = ', '.join(stocks[0:4] + ['......'] + stocks[-2:])
        raise ValueError("Parameter 'stocks' should be one of SP100, NYSE, NASDAQ, and ALL, not {} object: {}"
                         .format(t.__name__, str(stocks_error)))
    if len(stocks) == 0:  # empty list
        raise ValueError("Parameter 'stocks' must have something in it.")

    if isinstance(sheets, str):
        sheets = [sheets]  # str - list
    if update is False:
        for i in sheets:  # avoid typo
            if i not in ['financials', 'key-statistics', 'summary', 'profile', 'analysis', 'holders', 'ALL']:
                msg = "Parameter 'sheets' should come from: financials, key-statistics, summary, profile, analysis, " \
                      "holders, not {} "
                raise ValueError(msg.format(i))
        if sheets[0] == 'ALL':
            sheets = sheet_names()  # all sheets
        else:
            d = {'financials': ['income', 'cash_flow', 'balance'],
                 'key-statistics': ['Financial_Highlights', 'Valuation_Measures', 'Trading_Information'],
                 'summary': ['Summary'], 'profile': ['Executives', 'Description'],
                 'analysis': ['Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History', 'EPS_Trend', 'EPS_Revisions',
                              'Growth_Estimates'],
                 'holders': ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders']}
            sheets = [d[i] for i in sheets]  # map webpages to sheets
            sheets = [i[j] for i in sheets for j in range(len(i))]  # squeeze
    elif update is True:
        sheets = sheets  # when update, sheet=['income', 'balance', etc.], not 'financials'
    print("Get includes: {}".format(str(sheets)))

    with open(datapath(False, 'Spyder', 'get_sheets_cache.txt'), 'w') as w:
        w.write(','.join(sheets))  # save param sheets to cache for update() to use

    if stocks in ['NYSE', 'NASDAQ', 'ALL']:
        stocks = open_stock_list(stocks)['Symbol'].tolist()  # NASDAQ or NYSE
        random.shuffle(stocks)
    if stocks == 'SP100':  # SP100 - default
        stocks = open_general('SP100')['Symbol'].tolist()  # read csv
    if not isinstance(stocks, list):
        raise TypeError('Parameter stocks should be a list, not a ' + type(stocks).__name__)

    names_of_sheets = sheet_names()  # things that'll be updated

    len_temp = len(stocks)
    if len_temp < batch:
        batch = len_temp
    for i in range(0, len_temp, batch):  # Main loop
        # async in 3.6
        t1 = _time.time()
        tasks = [asyncio.ensure_future(parse(c, names_of_sheets, sheets=sheets, update=update, exception=exception, error_cache=error_cache))
                 for c in stocks[i:i + batch]]  # create async tasks
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))  # async main loop
        t2 = _time.time()
        if i+batch > len_temp:
            a = len_temp
        else:
            a = i + batch
        print('{}/{} - Total Time: {}s'.format(a, len_temp, round(t2 - t1, 4)))
    print('Data collection for {} completed'.format(name))
