# asynchronous coroutine
import asyncio

import datetime as _dtime
import os as _os
import pandas as _pd
import time as _time

# Internal modules
from .getter import getter
from .main_loop import main
from .parsers import get_update

from ..operations.Path import datapath

from ..exceptions import GetterRequestError  # exceptions


def _get_between_days(begin_date):
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


def get_last_update():  # get last update date of the database
    # client can access this
    """
    get last update time
    prints out the date and returns the date(str)
    """
    last_update = open(datapath(False, 'Spyder', 'datefile.txt')).readlines()[0]
    print("Last update time: " + last_update)
    return last_update


async def update_getter(day):  # util
    url = 'https://finance.yahoo.com/calendar/earnings?from=2019-05-12&to=2019-05-18&day={}'

    try:
        html = await getter(url.format(day), timeout=25)
    except GetterRequestError:
        html = None
    get_update(html)


# problem: the connection between async and normal functions
# update getter can't be connected well to the normal loop, and the current solution
# is to use a csv file as a transducer, but the method of running a singlar
# coroutine is not identified and developed, which needs to be done


# async def update_stock_list(day):
#     await update_getter(day)


def update_all_days():
    # Get updated-needed firms and perform updates
    try:
        with open(datapath(False, 'get_sheets_cache.txt'), mode='r') as w:
            sheets = w.read().split(',')  # read parameter sheets
    except FileNotFoundError:
        print("Exception FileNotFoundError")
        
    updates = _pd.read_csv('dates_temp.csv', index_col=0).values.tolist()  # read dates
    updates = set([i[j] for i in updates for j in range(len(i))])
    stocks = set(_os.listdir(datapath(True)))  # set of stocks already in database
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

    last_update = get_last_update()
    days = _get_between_days(last_update)  # days need to be checked
    print("\nCollecting companies that need to be updated")
    tasks = [asyncio.ensure_future(update_getter(day)) for day in days]  # async loop
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
    sheets_names = wb.get_sheet_names()  # openpyxl for getting all sheet_names

    r = [_pd.read_excel(path, i)['TICKER'].tolist()
         for i in sheets_names]  # header of stocks is TICKER in client's stock list
    r = [i[j] for i in r for j in range(len(i))]
    return r


def _progress_print(t, msg='main_get'):
    if msg == 'main_get':
        msg = '\r Retrieving data from Yahoo Finance: {} / {} - eta {}s'
    total = 87152
    with open(datapath(False, 'cnt.txt')) as r:
        n = r.read()
        if n == '':
            n = 0
        else:
            n = int(n)
    with open(datapath(False, 'cnt.txt'), 'w') as w:
        w.write(str(n + 1))
    eta = str(_dtime.timedelta(seconds=round((total - n // 10 * 10) * t)))
    print(msg.format(n, total, eta), end='')
