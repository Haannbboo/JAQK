import requests
from pyquery import PyQuery as pq
import pandas as pd
# import re
import time
import datetime
import os

# asynchronous coroutine
import asyncio
import aiohttp

# memory
import gc as _gc

# Internal modules
from .basics.stocks import stock_list

from .getters.get_holders import get_major_holders, get_top_institutional_and_mutual_fund_holders
from .getters.get_financials import get_stats, get_statements, get_reports
from .getters.get_profile import get_executives, get_description
from .getters.get_analysis import get_analysis
from .getters.get_summary import get_summary
from .operations.Save import save_file, save_dfs, save_analysis
from .operations.Folder import create_folder, exist


# url='https://finance.yahoo.com/quote/BABA/analysis?p=BABA'
# html=getter(url)
# df1,df2=top_institutional_and_mutual_fund_holders(html)

async def getter(url, timeout=20, error=True, proxy=None, cnt=0):
    # main get function for all the website getter
    # it would support proxies, multiple user agent
    """
    url - target url
    timeout - default 10 second (recommend >10)
    error - Recursive error handler
    proxy - connnect to proxies, should be a dic containing both http/https proxies
    """
    if cnt == 1:
        return

    proxy = proxy  # Connecting to proxy pool
    UA = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 \
        Safari/537.36']
    headers = {
        'User-Agent': UA[0]  # Select user agent
    }
    try:
        async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            r = await session.get(url, timeout=timeout)
            html = await r.text()
        error = False
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        # bug in catcher
        # print("Exception in MAIN GETTET: "+str(e)) # all clean now
        error = True
    if error == False:
        return html
    else:
        await getter(url, timeout, error, cnt=cnt + 1)


async def parse(c, names, update=False, save_mode='w'):
    urls = ['https://finance.yahoo.com/quote/' + c + '/holders?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/financials?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/balance-sheet?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/cash-flow?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/key-statistics?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/profile?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/analysis?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '?p=' + c]

    try:
        # get summary needs changes - handle NAN
        # needs bug recorder
        create_folder(c)
        if not exist(c, 'Summary', update):
            try:
                html = await getter(urls[7])
                # input("Press enter to continue")
                save_file(get_summary(html, c), c, 'Summary', update)
                # print("Saved summary")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        if not exist(c, names[3:6], update):
            try:
                html = await getter(urls[4])
                save_dfs(get_stats(html), c, names[3:6])
                # print("Saved statistics")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        if not exist(c, names[0:3], update):
            try:
                html = await getter(urls[0])
                save_file(get_major_holders(html), c, names[0], update)
                save_dfs(get_top_institutional_and_mutual_fund_holders(html), c,
                         [names[1], names[2]])
                # print("Saved holders")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        if not exist(c, names[6:8], update):
            try:
                html = await getter(urls[5])
                save_dfs([get_executives(html), get_description(html)], c, names[6:8])
                # print("Saved executives and description")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        if not exist(c, names[8:14], update):
            try:
                html = await getter(urls[6])
                save_analysis(get_analysis(html), c)
                # print("Saved analysis")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        if not exist(c, 'income', update):
            try:
                html = await getter(urls[1])
                save_file(get_reports(html), c, 'income', update)
                # print("Saved income statement")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        if not exist(c, 'balance', update):
            try:
                html = await getter(urls[2])
                save_file(get_reports(html), c, 'balance', update)
                # print("Saved balance sheet")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        if not exist(c, 'cash_flow', update):
            try:
                html = await getter(urls[3])
                save_file(get_reports(html), c, 'cash_flow', update)
                # print("Saved cash flow statement")
                # input("Press enter to continue")
                del html
                await asyncio.sleep(0.27)
            except Exception:
                pass
        _gc.collect()
        # print("All saved for "+c)
    except Exception as e:
        bug = [[c, e]]
        # print("Exception on "+c+": ",e)


def get_all_stocks(exchange):  # Get all stocks required using the stock_list operation
    if not (exchange != 'NYSE' or exchange != 'NASDAQ'):
        raise ValueError("Exchange should be either NYSE or NASDAQ, not: '{}'".format(str(exchange)))
    s = stock_list(exchange)['Symbol'].tolist()
    return s


def main(stocks='NYSE', update=False, batch=64):
    """
    exchange -- either NYSE or NASDAQ
    """
    if stocks in ['NYSE', 'NASDAQ']:  # load all stocks
        stocks = get_all_stocks(stocks)
    assert isinstance(stocks, list)
    # stocks=['BABA'] #for testing
    # s=['BABA','AAPL','AMZN','JD','BIDU','WB','WFC','C','JPM','DPZ','BA','CVX','LUV'] # for sample testing
    NAMES = ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders',
             'Trading_Information', 'Financial_Highlights', 'Valuation_Measures',
             'Executives', 'Description',
             'Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates',
             'stats', 'statements', 'reports',
             'Executives', 'Description', 'analysis', 'Summary']  # things that'll be updated
    len_temp = int(len(stocks))
    if len_temp < batch:
        batch = len_temp
    for i in range(0, len_temp, batch):  # Yahoo Spyder main; async main loop
        # async in 3.6, different callings in 3.7
        t1 = time.time()
        tasks = [asyncio.ensure_future(parse(c, NAMES, update=update)) for c in stocks[i:i + batch]]  # async calling
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        t2 = time.time()
        print(str(i + batch) + "/" + str(len(stocks)) + " - Total Time: " + str(t2 - t1) + 's')
        # input("Cut point check")


# main()
'''
def _speedtestf():
    import shutil
    stock='NYSE'
    t=[]
    for i in range(16,256,8):
        companies=get_all_stocks(stock)[0:i]
        s=time.time()
        main(stock, batch=i)
        e=time.time()
        t.append(round((e-s)/i, 4))
        print("batch size {}: {}s".format(i, round((e-s)/i,3)))
        for c in companies:
            try:
                shutil.rmtree(os.path.join('./database',c))
            except FileNotFoundError:
                print('FileNotFoundError: '+c)
                continue
        #input('cut point check')
        gc.collect()
        time.sleep(1)
    return t
'''


def main_get(stocks='ALL', batch=32):
    """
    Main getter for client, MUST be runned after installation of the package (default update all stocks in NYSE and NASDAQ)
    stocks - str - default ALL, can be either NYSE or NASDAQ
    batch - default 32, batch size for loop (recommend to change based on interest status)
    """
    if stocks not in ['NYSE', 'NASDAQ', 'ALL']:
        raise ValueError("Parameter 'stocks' should be one of NYSE, NASDAQ, and ALL")
    main(stocks='NYSE', batch=batch)
    print("Updated NYSE data")
    main(stocks='NASDAQ', batch=batch)
    print("Updated NASDAQ data")


def _getBetweenDay(begin_date):  # tested
    # Got from csdn.com, minor changes have made
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    end_date = datetime.datetime.strptime(today, "%Y-%m-%d")
    print("Current date: " + today)
    while begin_date <= end_date:  # doesn't include today
        date_str = begin_date.strftime("%Y-%m-%d")
        yield date_str  # to reduce memory usage
        begin_date += datetime.timedelta(days=1)


def getLastUpdate():  # get last update date of the database
    # client can access this
    """
    get last update time
    prints out the date and returns the date(str)
    """
    last_update = open('datefile.txt').readlines()[0]
    print("Last update time: " + last_update)
    return last_update


async def update_getter(day):  # util
    url = 'https://finance.yahoo.com/calendar/earnings?from=2019-05-12&to=2019-05-18&day={}'
    html = await getter(url.format(day), timeout=15)
    updates = [i.text()
               for i in pq(html)('.simpTblRow a').items()
               ]
    df = pd.DataFrame(updates)
    df.to_csv('dates_temp.csv', mode='a', header=False)  # csv as a tranducer


# problem: the connection between async and normal functions
# update getter can't be connected well to the normal loop, and the current solution
# is to use a csv file as a transducer, but the method of running a singlar
# coroutine is not identified and developed, which needs to be done


async def update_stock_list(day):
    await update_getter(day)


def update_all_days():
    # Dates that need to be updated
    # Date format - YYYY-MM-DD

    # input('Cut-point check') # for checking
    # df.tolist() is depreciated... use df.values.tolist() instead
    updates = pd.read_csv('dates_temp.csv', index_col=0).values.tolist()  # read dates
    updates = set([i[j] for i in updates for j in range(len(i))])  # for set operation AND
    needs_update_list = list(updates.intersection(stocksss))
    company_list_length = len(needs_update_list)
    print("Total update companies: {}".format(company_list_length))
    if company_list_length == 0:
        return
    try:
        main(needs_update_list, update=True)  # no syntax error here
        # working smoothly now (not fast enough)
    except Exception as e:
        print("Exception in update each day: " + str(e))


def update():
    """
    update function for JAQK package
    this automatically catches days and companies need to be updated, and update
    recommend to update every day
    """
    df = pd.DataFrame()
    df.to_csv('dates_temp.csv')  # clear up cache
    global stocksss
    stocksss = set(os.listdir('./database'))  # set of stocks in database
    last_update = getLastUpdate()
    days = _getBetweenDay(last_update)
    tasks = [asyncio.ensure_future(update_stock_list(day)) for day in days]  # async calling
    temp = asyncio.get_event_loop()
    temp.run_until_complete(asyncio.wait(tasks))
    print("Company list retrieved")
    update_all_days()
    #    with open('datefile.txt', mode='w') as d:
    #        d.write(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    print("Update completed")
