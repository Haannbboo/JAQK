# asynchronous coroutine
import asyncio
import aiohttp

import datetime as _dtime
import gc as _gc
import os as _os
import pandas as _pd
import time as _time

from pyquery import PyQuery as _pq

# Internal modules
from .basics.stocks import stock_list

from .getters.get_holders import get_major_holders, get_top_institutional_and_mutual_fund_holders
from .getters.get_financials import get_stats, get_reports
from .getters.get_profile import get_executives, get_description
from .getters.get_analysis import get_analysis
from .getters.get_summary import get_summary

from .operations.Save import save_file, save_dfs, save_analysis
from .operations.Folder import create_folder, exist
from .operations.Open import open_file, open_general

global main_path
main_path = _os.path.abspath(_os.path.dirname(__file__))


async def getter(url, timeout=20, error=True, retry=0, cnt=0):
    """Main get function for most the website crawler

    It uses asynchronous coroutine and asynchronous request sessions (aiohttp)

    Args:
        url: str - target url
        timeout: int - timeout set for each request, default 10 second (recommend >10)
        error: bool - Recursive error handler, identify state of request
        retry: int - time of retry
        cnt: int - count time of retry

    Returns:
        if successfully requested, returns html information in string
        else, returns None
    """
    if cnt >= retry:
        return

    UA = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 \
        Safari/537.36',]
    headers = {
        'User-Agent': UA[0],  # User agent
    }
    
    try:
        # aiohttp client request session, asynchronous request library
        async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            r = await session.get(url, timeout=timeout)
            html = await r.text()
        error = False
    except (aiohttp.ClientTimeout, aiohttp.ClientConnectionError):
        error = True
        
    if not error:
        return html
    else:  
        await getter(url, timeout, error, cnt=cnt+1)  # retry


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
            except Exception as e:
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
        print("Exception on {}: ".format(c, e))


def get_all_stocks(exchange):  # Get all stocks required using the stock_list operation
    if not (exchange != 'NYSE' or exchange != 'NASDAQ' or exchange != True):
        raise ValueError("Exchange should be either NYSE or NASDAQ, not: '{}'".format(str(exchange)))
    s = stock_list(exchange)['Symbol'].tolist()
    return s


def main(stocks, sheets, update=False, batch=64, exception=False):
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
    if stocks in ['NYSE', 'NASDAQ']:  # load all stocks if needed
        stocks = get_all_stocks(stocks)
    if not isinstance(stocks, list):
        raise TypeError('Parameter stocks should be a list, not a '+type(stocks).__name__)

    NAMES = ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders',
             'Trading_Information', 'Financial_Highlights', 'Valuation_Measures',
             'Executives', 'Description',
             'Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates',
             'stats', 'statements', 'reports',
             'Executives', 'Description', 'analysis', 'Summary',
             'income', 'balance', 'cash_flow']  # things that'll be updated

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


def main_get(stocks='SP100', sheets='financials', batch=32, exception=False):
    """
    Main getter for client, MUST be runned after installation of the package (default update all stocks in NYSE and NASDAQ)
    stocks - str - default SP100, can be ALL, NYSE, NASDAQ, list of tickets, load_stock_list() (for client only)
    sheets - list/str - default financials (income, balance, cash_flow), use "ALL" to indicate all sheets; choices include: financials, key-statistics, summary, profile, analysis, holders
    batch - default 32, batch size for loop (recommend to change based on interest status)
    """
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
    for i in sheets:  # avoid typo
        if i not in ['financials', 'key-statistics', 'summary', 'profile', 'analysis', 'holders', 'ALL']:
            msg = "Parameter 'sheets' should come from: financials, key-statistics, summary, profile, analysis, holders, not {}"
            raise ValueError(msg.format(i))
    if sheets[0] == 'ALL':
        sheets = ['income', 'cash_flow', 'balance', 'Financial_Highlights', 'Valuation_Measures', 'Trading_Information',
                  'Sumary', 'Executives', 'Description', 'Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History',
                  'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates',
                  'major_holders', 'top_institutional_holders', 'top_mutual_fund_holders']
    else:
        d = {'financials': ['income', 'cash_flow', 'balance'],
             'key-statistics': ['Financial_Highlights', 'Valuation_Measures', 'Trading_Information'],
             'summary': ['Summary'], 'profile': ['Executives', 'Description'],
             'analysis': ['Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History', 'EPS_Trend', 'EPS_Revisions',
                          'Growth_Estimates'],
             'holders': ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders']}
        sheets = [d[i] for i in sheets]  # map webpages to sheets
        sheets = [i[j] for i in sheets for j in range(len(i))]  # squeeze
    print("Get includes: ......")
    print(str(sheets))
    with open(_os.path.join(main_path, 'get_sheets_cache.txt'), 'w') as w:
        w.write(','.join(sheets))  # save param sheets to cache for update() to use
    if stocks == 'SP100':  # S&P 100 <- default
        stocks = open_general('SP100')['Symbol'].tolist()  # read csv
        main(stocks=stocks, sheets=sheets, batch=batch, exception=exception)

    elif stocks == 'ALL':
        main(stocks='NYSE', sheets=sheets, batch=batch, exception=exception)
        print("Updated NYSE data")
        main(stocks='NASDAQ', sheets=sheets, batch=batch, exception=exception)
        print("Updated NASDAQ data")
    else:
        main(stocks=stocks, sheets=sheets, batch=batch, exception=exception)  # updated for sheets
        if len(stocks) > 10:
            stocks = str(stocks[0:4] + ['......'] + stocks[-2:])  # avoid printing too much
        print("Updated all data for" + str(stocks))


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
    html = await getter(url.format(day), timeout=15)
    updates = [i.text()
               for i in _pq(html)('.simpTblRow a').items()
               ]
    df = _pd.DataFrame(updates)
    df.to_csv('dates_temp.csv', mode='a', header=False)  # csv of firms


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
    needs_update_list = list(updates.intersection(stocksss))  # set operation AND
    company_list_length = len(needs_update_list)
    print("Total update companies: {}".format(company_list_length))
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
    global stocksss
    stocksss = set(_os.listdir(datapath()))  # set of stocks already in database
    last_update = getLastUpdate()
    days = _getBetweenDay(last_update)  # days need to be checked
    tasks = [asyncio.ensure_future(update_stock_list(day)) for day in days]  # async loop
    temp = asyncio.get_event_loop()
    temp.run_until_complete(asyncio.wait(tasks))  # get companies that were updated in these days
    print("Company list retrieved")
    update_all_days()  # set operation & main get loop
    with open('datefile.txt', mode='w') as d:
        d.write(time.strftime('%Y-%m-%d', time.localtime(time.time())))  # update last update record
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


def setup():
    """
    setup the database; this should be done before anything;
    choose the directory to place the database (~100M)
    """
    assert _is_global() == True

    # choose a specific path for database folders
    import PySimpleGUI as sg
    form_rows = [[sg.Text('Choose the setup path')],
                 [sg.Text('Setup path: ', size=(15, 1)), sg.InputText(key='setup'), sg.FolderBrowse()],
                 [sg.Submit(), sg.Cancel()]]  # layout design
    window = sg.Window('Choose a path for setup database')
    _, values = window.Layout(form_rows).Read()  # callback
    window.Close()
    setup_path = values['setup']
    with open(_os.path.join(main_path, 'setup_cache.txt'), mode='w') as w:
        w.write(setup_path)  # setup cache file for setup directory

    # setup starts
    companies = ['AAPL', 'AMZN']
    [create_folder(i, setup_path, True) for i in companies]  # create new folders
    dirs = [_os.listdir(_os.path.join(datapath(setup=False), c)) for c in companies]
    dirs2 = dirs[:]
    del dirs
    try:
        [dirs2[i].remove('__init__.py') for i in range(2)]  # remove __init__.py
    except ValueError:
        pass
    if '.py' in ''.join(dirs2[0]) + ''.join(dirs2[1]):  # AAPL and AMZN
        # convert .py into .csv
        [open_file(companies[c], dirs2[c][d], setup=True).to_csv(
            _os.path.join(setup_path, companies[c], dirs2[c][d].split('.')[0] + '.csv'), index=False)
         for c in range(len(companies)) for d in range(len(dirs2[c]))
         if dirs2[c][d] != '__init__.py' and dirs2[c][d] != '__pycache__']

        # delete original .py files
        [_os.remove(_os.path.join(datapath(setup=False), companies[i], dirs2[i][j]))
         for i in range(len(companies)) for j in range(len(dirs2[i]))
         if dirs2[i][j] != '__init__.py' and ('.csv' not in dirs2[i][j]) and dirs2[i][j] != '__pycache__']

    # setup general stock lists
    dirs_general2 = _os.listdir(_os.path.join(datapath(setup=False), 'general'))
    dirs_general = dirs_general2[:]  # avoid mutable list
    del dirs_general2
    try:
        dirs_general.remove('__init__.py')  # list_dir for 'general'
    except ValueError:
        pass

    if '.py' in ''.join(dirs_general):  # NYSE and NASDAQ
        # setup stock_list general
        exc = ['NYSE', 'NASDAQ', 'SP100']
        create_folder('general', setup_path, True)
        [open_general(ex, setup=True).to_csv(_os.path.join(setup_path, 'general', ex + '.csv'), index=False)
         for ex in exc]
        [_os.remove(_os.path.join(datapath(setup=False), 'general', ex + '.py')) for ex in exc]

    if 'dates_temp.py' in _os.listdir(main_path):  # dates_temp
        _pd.read_csv(_os.path.join(main_path, 'dates_temp.py')).to_csv(_os.path.join(main_path, 'dates_temp.csv'),
                                                                       index=False)
        _os.remove(_os.path.join(main_path, 'dates_temp.py'))  # delete original\

    if 'datefile.py' in _os.listdir(main_path):  # datefile
        with open(_os.path.join(main_path, 'datefile.py')) as d:
            d = d.read()  # read
        with open(_os.path.join(main_path, 'datefile.txt'), mode='w') as w:
            w.write(d)  # write
        _os.remove(_os.path.join(main_path, 'datefile.py'))  # delete

    _gc.collect()
    print("Database has been setup on path: {}".format(setup_path))


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


def datapath(setup=True):
    """
    The global datapath for all other file.
    It sets your selected path in jaqk.setup() as the main datapath,
    and all data will be added/deleted from there.
    """
    try:
        with open(_os.path.join(main_path, 'setup_cache.txt')) as w:
            path = w.read()
        if setup == True:
            return path
        else:
            return _os.path.join(_os.path.dirname(__file__), 'database')
    except FileNotFoundError:
        return _os.path.join(_os.path.dirname(__file__), 'database')
