import requests
import time as _time
import random

from ..operations.Tools import sheet_names
from ..operations.Open import open_stock_list, open_general
from ..operations.Path import datapath


def test_main(stocks='SP100', sheets='financials', batch=32, update=False, exception=False, error_cache=True, greater=-1):

    name = stocks
    if stocks not in ['NYSE', 'NASDAQ', 'ALL', 'SP100'] and isinstance(stocks, str):
        # when stocks is nonesense
        t = type(stocks)
        stocks_error = stocks
        if len(stocks) > 10:
            stocks_error = ', '.join(stocks[0:4] + ['......'] + stocks[-2:])
        raise ValueError("Parameter 'stocks' should be one of SP100, NYSE, NASDAQ, and ALL, not {} object: {}"
                         .format(t.__name__, str(stocks_error)))
    if isinstance(stocks, list):
        if len(stocks) == 0:  # empty list
            raise ValueError("Parameter 'stocks' must have something in it.")
        stocks = [s.upper() for s in stocks]

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
            
    for i in range(0, len_temp, 10):  # Main loop
        t1 = _time.time()
        for j in range(0, 10):
            parse(c=stocks[i+j], names=names_of_sheets, sheets=sheets, exception=exception, error_cache=error_cache, greater=greater)
            if j%10 == 9:
                t2 = _time.time()
                print('{}/{} - Total Time: {}s'.format(i+10, len_temp, round(t2 - t1, 4)))

    print('Data collection for {} completed'.format(name))

import gc as _gc

from .parsers import *
from ..operations.Save import save_file, save_dfs, save_analysis
from ..operations.Folder import create_folder, exist, error_record
from ..operations.Folder import is_full as _is_full


def parse(c, names, sheets, update=False, exception=False, error_cache=True, greater=-1):
    if '^' in c:
        return
    
    urls = ['https://finance.yahoo.com/quote/{}/holders?p={}'.format(c, c),
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

    errors = error_record(activate=error_cache)


    try:

        # Since each individual parser may has different param and save methods,
        # I separated each of them rather than put them into a function.

        create_folder(c)
        if not exist(c, 'Summary', update) and _is_active('Summary', sheets) and not errors.is_failed(c, 'Summary'):
            # update summary
            try:
                html = getter(urls[7])  # async request
                save_file(get_summary(html, c), c, 'Summary', update)  # save + parse

                del html  # save memory since len(html) is about 500,000
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'Summary', e)
            except Exception as e:
                if exception:
                    print(exception_msg.format('summary', c, e))
        if not exist(c, names[3:6], update) and _is_active(names[3:6], sheets) and not errors.is_failed(c, 'stats'):
            # update key-statistics
            try:
                html = getter(urls[4])
                save_dfs(get_stats(html), c, names[3:6])

                del html
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'stats', e)
            except Exception as e:
                # errors.save_failed(c, 'stats', e)
                if exception:
                    print(exception_msg.format('key-statistics', c, e))
        if not exist(c, names[0:3], update) and _is_active(names[0:3], sheets) and not errors.is_failed(c, 'holders'):
            # update holders
            try:
                html = getter(urls[0])
                save_file(get_major_holders(html), c, names[0], update)
                save_dfs(get_top_institutional_and_mutual_fund_holders(html), c,
                         [names[1], names[2]])

                del html
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'holders', e)
            except Exception as e:
                # errors.save_failed(c, 'holders', e)
                if exception:
                    print(exception_msg.format('holders', c, e))
                    
        if not exist(c, names[6:8], update) and _is_active(names[6:8], sheets) and not errors.is_failed(c, 'profile'):
            # update profile
            try:
                html = getter(urls[5])
                save_dfs([get_executives(html), get_description(html)], c, names[6:8])

                del html
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'profile', e)
            except Exception as e:
                # errors.save_failed(c, 'profile', e)
                if exception:
                    print(exception_msg.format('profile', c, e))
        if not exist(c, names[8:14], update) and _is_active(names[8:14], sheets) and not errors.is_failed(c, 'analysis'):
            # update analysis
            try:
                html = getter(urls[6])
                # save_analysis(get_analysis(html), c)
                save_dfs(get_analysis(html), c, names[8:14])

                del html
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'analysis', e)
            except Exception as e:
                # errors.save_failed(c, 'analysis', e)
                if exception:
                    print(exception_msg.format('analysis', c, e))
        if not exist(c, 'income', update) and _is_active('income', sheets) and not errors.is_failed(c, 'income'):
            # update income
            try:
                html = getter(urls[1])
                save_file(get_reports(html), c, 'income', update)

                del html
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'income', e)
            except Exception as e:
                # errors.save_failed(c, 'income', e)
                if exception:
                    print(exception_msg.format('income', c, e))
        if not exist(c, 'balance', update) and _is_active('balance', sheets) and not errors.is_failed(c, 'balance'):
            # update balance
            try:
                html = getter(urls[2])
                save_file(get_reports(html), c, 'balance', update)

                del html
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'balance', e)
            except Exception as e:
                # errors.save_failed(c, 'balance', e)
                if exception:
                    print(exception_msg.format('balance-sheet', c, e))
        if not exist(c, 'cash_flow', update) and _is_active('balance', sheets) and not errors.is_failed(c, 'cash_flow'):
            # update cash-flow
            try:
                html = getter(urls[3])
                save_file(get_reports(html), c, 'cash_flow', update)

                del html
                _time.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'cash_flow', e)
            except Exception as e:
                # errors.save_failed(c, 'cash_flow', e)
                if exception:
                    print(exception_msg.format('cash-flow', c, e))
        _gc.collect()
    except Exception as e:
        errors.save_failed(c, 'main', e)
        # print("Exception on {}: {}".format(c, e))


def _is_active(names, sheets):
    if isinstance(names, str):
        names = [names]
    return set(names).issubset(set(sheets))  # [] in [] regardless of order


def getter(url, timeout=20, error=True, retry=0, cnt=0):

    if cnt > retry:
        return
        # error = "Failed to request data from url {}".format(url)
        # raise GetterRequestError(error)

    user_agent = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 \
        Safari/537.36', ]
    headers = {
        'User-Agent': user_agent[0],  # User agent
    }

    try:
        r = requests.get(url, timeout=timeout, headers=headers)
        html = r.text
        error = False
    # except (aiohttp.ClientTimeout, aiohttp.ClientConnectionError) as e:
    except Exception:
        error = True
    except TimeoutError:
        error = True

    if not error:
        return html
    else:
        getter(url, timeout, error=error, cnt=cnt+1)  # retry

