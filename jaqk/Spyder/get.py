# asynchronous coroutine
import asyncio

import datetime as _dtime
import gc as _gc
import os as _os
import pandas as _pd
import time as _time

from pyquery import PyQuery as _pq

# Internal modules
from .parsers import *
from .getter import getter

from ..operations.Save import save_file, save_dfs, save_analysis
from ..operations.Folder import create_folder, exist
from ..operations.Open import open_general, open_stock_list
from ..operations.Path import datapath
from ..operations.Tools import sheet_names

from ..exceptions import GetterRequestError  # exceptions

global main_path
main_path = _os.path.abspath(_os.path.dirname(__file__))


async def parse(c, names, sheets, update=False, exception=False):
    """Main parser of the Spyder that wraps up individual parsing rules.

    It calls the async getter function and pass the html to parser (get_summary() etc.),
    and call saver (save_file() etc.) for saving the result in csv format.

    Args:
        c: str - company ticket name, such as AAPL for Apple Inc., only accept ONE ticket.
        names: list - names of ALL sheets, passed in through main().
        sheets: list - sheets that will be saved, passed in through main().
        update: bool - identify if this parse() is used for update(),
            which has different save rules which will be passed to saver (save_file(update=update) etc.).
        exception: bool - print out the exception or not.

    Returns:
        None
    """
    urls = ['https://finance.yahoo.com/quote/' + c + '/holders?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/financials?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/balance-sheet?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/cash-flow?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/key-statistics?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/profile?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/analysis?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '?p=' + c]

    if isinstance(sheets, str):
        sheets = [sheets]  # double check

    exception_msg = "Exception on {} for {}: {}"

    try:
        # Since each individual parser may has different param and save methods,
        # I separated each of them rather than put them into a function.

        create_folder(c)
        if not exist(c, 'Summary', update) and _is_active('Summary', sheets):
            # update summary
            try:
                html = await getter(urls[7])  # async request
                save_file(get_summary(html, c), c, 'Summary', update)  # save + parse

                del html  # save memory since len(html) is about 500,000
                await asyncio.sleep(0.27)
            except Exception as e:
                if exception:
                    print(exception_msg.format('summary', c, e))
        if not exist(c, names[3:6], update) and _is_active(names[3:6], sheets):
            # update key-statistics
            try:
                html = await getter(urls[4])
                save_dfs(get_stats(html), c, names[3:6])

                del html
                await asyncio.sleep(0.27)
            except Exception as e:
                if exception:
                    print(exception_msg.format('key-statistics', c, e))
        if not exist(c, names[0:3], update) and _is_active(names[0:3], sheets):
            # update holders
            try:
                html = await getter(urls[0])
                save_file(get_major_holders(html), c, names[0], update)
                save_dfs(get_top_institutional_and_mutual_fund_holders(html), c,
                         [names[1], names[2]])

                del html
                await asyncio.sleep(0.27)
            except Exception as e:
                if exception:
                    print(exception_msg.format('holders', c, e))
        if not exist(c, names[6:8], update) and _is_active(names[6:8], sheets):
            # update profile
            try:
                html = await getter(urls[5])
                save_dfs([get_executives(html), get_description(html)], c, names[6:8])

                del html
                await asyncio.sleep(0.27)
            except Exception as e:
                if exception:
                    print(exception_msg.format('profile', c, e))
        if not exist(c, names[8:14], update) and _is_active(names[8:14], sheets):
            # update analysis
            try:
                html = await getter(urls[6])
                save_analysis(get_analysis(html), c)

                del html
                await asyncio.sleep(0.27)
            except Exception as e:
                if exception:
                    print(exception_msg.format('analysis', c, e))
        if not exist(c, 'income', update) and _is_active('income', sheets):
            # update income
            try:
                html = await getter(urls[1])
                save_file(get_reports(html), c, 'income', update)

                del html
                await asyncio.sleep(0.27)
            except Exception as e:
                if exception:
                    print(exception_msg.format('income', c, e))
        if not exist(c, 'balance', update) and _is_active('balance', sheets):
            # update balance
            try:
                html = await getter(urls[2])
                save_file(get_reports(html), c, 'balance', update)

                del html
                await asyncio.sleep(0.27)
            except IndexError as e:
                if exception:
                    print(exception_msg.format('balance-sheet', c, e))
        if not exist(c, 'cash_flow', update) and _is_active('balance', sheets):
            # update cash-flow
            try:
                html = await getter(urls[3])
                save_file(get_reports(html), c, 'cash_flow', update)

                del html
                await asyncio.sleep(0.27)
            except Exception as e:
                if exception:
                    print(exception_msg.format('cash-flow', c, e))
        _gc.collect()
    except Exception as e:
        print("Exception on {}: {}".format(c, e))


def get_all_stocks(exchange):  # Get all stocks required using the stock_list operation
    if not (exchange != 'NYSE' or exchange != 'NASDAQ' or exchange != True):
        raise ValueError("Exchange should be either NYSE or NASDAQ, not: '{}'".format(str(exchange)))
    s = open_stock_list(exchange)['Symbol'].tolist()
    return s


def main(stocks='SP100', sheets='financials', batch=32, update=False, exception=False):
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
        if len(stocks) > 10:
            stocks = str(stocks[0:4] + ['......'] + stocks[-2:])
        raise ValueError("Parameter 'stocks' should be one of SP100, NYSE, NASDAQ, and ALL, not {} object: {}"
                         .format(t.__name__, str(stocks)))
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

    with open(_os.path.join(main_path, 'get_sheets_cache.txt'), 'w') as w:
        w.write(','.join(sheets))  # save param sheets to cache for update() to use

    if stocks in ['NYSE', 'NASDAQ']:
        stocks = get_all_stocks(stocks)  # NASDAQ or NYSE
    if stocks == 'SP100':  # SP100 - defaul
        stocks = open_general('SP100')['Symbol'].tolist()  # read csv
    if not isinstance(stocks, list):
        raise TypeError('Parameter stocks should be a list, not a '+type(stocks).__name__)

    NAMES = sheet_names()  # things that'll be updated

    len_temp = int(len(stocks))
    if len_temp < batch:
        batch = len_temp
    for i in range(0, len_temp, batch):  # Main loop
        # async in 3.6
        t1 = _time.time()
        tasks = [asyncio.ensure_future(parse(c, NAMES, sheets=sheets, update=update, exception=exception))
                 for c in stocks[i:i + batch]]  # create async tasks
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))  # async main loop
        t2 = _time.time()
        print('{}/{} - Total Time: {}s'.format(str(i + batch), str(len(stocks)), str(t2 - t1)))
    print('Data collection for {} completed'.format(name))


def _getBetweenDay(begin_date):
    """Get dates between two days using datatime.timedelta

    Args:
        begin_date: str - YY-MM-DD

    Returns:
        generator with dates
    """
    begin_date = _dtime.datetime.strptime(begin_date, "%Y-%m-%d") + _dtime.timedelta(days=1)
    today = _time.strftime('%Y-%m-%d', _time.localtime(_time.time()))
    end_date = _dtime.datetime.strptime(today, "%Y-%m-%d")  # format dates
    print("Current date: " + today)
    while begin_date <= end_date:  # doesn't include today
        date_str = begin_date.strftime("%Y-%m-%d")
        yield date_str  # to reduce memory usage
        begin_date += _dtime.timedelta(days=1)


def getLastUpdate():  # get last update date of the database
    # client can access this
    """
    get last update time
    prints out the date and returns the date(str)
    """
    last_update = open(_os.path.join(main_path, 'datefile.txt')).readlines()[0]
    print("Last update time: " + last_update)
    return last_update


async def update_getter(day):  # util
    url = 'https://finance.yahoo.com/calendar/earnings?from=2019-05-12&to=2019-05-18&day={}'

    try:
        html = await getter(url.format(day), timeout=25)
    except GetterRequestError:
        html = None
    try:
        updates = [i.text() for i in _pq(html)('.simpTblRow a').items()]
        df = _pd.DataFrame(updates)
        df.to_csv('dates_temp.csv', mode='a', header=False)  # csv of firms
    except TypeError:
        pass


# problem: the connection between async and normal functions
# update getter can't be connected well to the normal loop, and the current solution
# is to use a csv file as a transducer, but the method of running a singlar
# coroutine is not identified and developed, which needs to be done


async def update_stock_list(day):
    await update_getter(day)


def update_all_days():
    # Get updated-needed firms and perform updates
    try:
        with open(_os.path.join(main_path, 'get_sheets_cache.txt'), mode='r') as w:
            sheets = w.read().split(',')  # read parameter sheets
    except FileNotFoundError:
        print("Exception FileNotFoundError")
        
    updates = _pd.read_csv('dates_temp.csv', index_col=0).values.tolist()  # read dates
    updates = set([i[j] for i in updates for j in range(len(i))])
    stocks = set(_os.listdir(datapath()))  # set of stocks already in database
    needs_update_list = list(updates.intersection(stocks))  # set operation AND
    company_list_length = len(needs_update_list)
    print("Total update companies: {}\n".format(company_list_length))
    if company_list_length == 0:
        return
    try:
        main(needs_update_list, sheets=sheets, update=True)  # call main get function
        # update=True to identify different save operations
    except Exception as e:
        print("Exception in update each day: " + str(e))


def update():
    """Update database

    It first gets the dates that need to be updated, then go to Yahoo finance
    to find companies that were updated in these days. It then perform set
    operation AND on those companies and companies already in the database.
    It then calls the main get function to collect data, and save to database
    with save mode 'a' instead of 'w'.

    Returns:
        prints out success message
        updates database
    """
    df = _pd.DataFrame()
    df.to_csv('dates_temp.csv')  # clear up cache

    last_update = getLastUpdate()
    days = _getBetweenDay(last_update)  # days need to be checked
    print("\nCollecting companies that need to be updated")
    tasks = [asyncio.ensure_future(update_stock_list(day)) for day in days]  # async loop
    temp = asyncio.get_event_loop()
    temp.run_until_complete(asyncio.wait(tasks))  # get companies that were updated in these days
    print("Company list retrieved")
    print("\nUpdating these companies")
    update_all_days()  # set operation & main get loop
    with open('datefile.txt', mode='w') as d:
        d.write(_time.strftime('%Y-%m-%d', _time.localtime(_time.time())))  # update last update record
    print("Update completed")


def load_stock_list():
    """
    for specific stock_list only (client's stock list: KWHS Investment Competition Approved Securities)
    """
    import PySimpleGUI as sg
    form_rows = [[sg.Text('Choose the excel path')],
                 [sg.Text('Choose path: ', size=(15, 1)), sg.InputText(key='Choose'),
                  sg.FileBrowse(file_types=(('Excel Spreadsheet', '*.xlsx'), ('Excel Spreadsheet', '*.xls')))],
                 [sg.Submit(), sg.Cancel()]]
    window = sg.Window('Choose excel from path')
    _, values = window.Layout(form_rows).Read()
    window.Close()
    path = values['Choose']  # file path chosen

    import openpyxl as xl
    wb = xl.load_workbook(path)
    sheet_names = wb.get_sheet_names()  # openpyxl for getting all sheet_names

    r = [_pd.read_excel(path, i)['TICKER'].tolist()
         for i in sheet_names]  # header of stocks is TICKER in client's stock list
    r = [i[j] for i in r for j in range(len(i))]
    return r


def _is_global():  # resolve datapath scrope problem
    try:
        type(datapath())
        return True
    except NameError:
        return False


def _is_active(names, sheets):
    if isinstance(names, str):
        names = [names]
    return set(names).issubset(set(sheets))  # [] in [] regardless of order


def _progress_print(t, msg='main_get'):
    if msg == 'main_get':
        msg = '\r Retrieving data from Yahoo Finance: {} / {} - eta {}s'
    total = 87152
    with open(_os.path.join(datapath(False), 'cnt.txt')) as r:
        n = r.read()
        if n == '':
            n = 0
        else:
            n = int(n)
    with open(_os.path.join(datapath(False), 'cnt.txt'), 'w') as w:
        w.write(str(n + 1))
    eta = str(_dtime.timedelta(seconds=round((total - n // 10 * 10) * t)))
    print(msg.format(n, total, eta), end='')
