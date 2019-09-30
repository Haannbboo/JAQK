import os as _os
import gc as _gc
import pandas as _pd
import numpy as _np

from .Path import datapath


def database_count():
    """
    prints out the total number of companies and sheets in database
    """
    a = len(_os.listdir(datapath(True))) - 3
    b = _os.walk(datapath(True))  # generator
    c = [1]
    c = len([c[0] + 1 for root, dirs, files in b for _ in files]) - 6
    print("Total number of companies contained: {}".format(a))
    print("Total number of detailed sheets: {}".format(c))
    _gc.collect()


def success_rate(target):
    companies = _os.walk(datapath(True))
    cnt = 0
    s_cnt = 0
    for _, _, files in companies:
        cnt +=1
        if len(files)>=target:
            s_cnt +=1 
    return round(s_cnt/cnt, 5)
    

def database_clear(path='datapath'):
    """
    clear all data in database (use cautiously)
    """
    if path == 'datapath':
        d = datapath(True)
    else:
        d = path
    files = (i for i in _os.listdir(d))
    for f in files:  # file name
        if f not in ['__init__.py', '.DS_Store', 'AAPL', 'AMZN', 'general', 'test']:
            dd = _os.path.join(d, f)
            try:
                for ff in _os.listdir(dd):
                    _os.remove(_os.path.join(dd, ff))
                _os.removedirs(dd)
            except (NotADirectoryError, FileNotFoundError):
                _os.remove(dd)
    print("Sucessfully clear all data in database")
    _gc.collect()


def database_reset():
    """
    reset database to the original state
    convert package database directory to its original state
    """
    pass
 

def factors_names(sheet=None):
    if sheet is None:
        fil = _os.listdir(datapath(True, 'AAPL'))
        files = fil[:]
        try:
            files.remove('__init__.py')
            files.remove('__pycache__')
        except ValueError:
            pass
        dfs = (_pd.read_csv(datapath(True, 'AAPL', c)) for c in files)  # generator
        r = [df.iloc[0:, 0].values[1:] for df in dfs if len(df) < 48]
        r = [i.tolist()[j] for i in r for j in range(len(i.tolist()))] + list(
            _pd.read_csv(datapath(True, 'AAPL', 'AAPL_Summary.csv')))[1:]
        # names = [i[5:-4] for i in files]
        # r = {names[i]: r[i].tolist() for i in range(len(r))}
            #
        r = _np.array(r, dtype='str')
    else:
        if sheet not in sheet_names():
            raise ValueError('Parameter sheet is wrong, use sheets_names() to find all sheets names')
        file = 'AAPL_{}.csv'.format(sheet)
        if sheet == 'Summary':
            r = _np.array(list(_pd.read_csv(datapath(True, 'AAPL', 'AAPL_Summary.csv')))[1:])
        else:
            r = _pd.read_csv(datapath(True, 'AAPL', file)).iloc[0:-1, 0].values[1:]
    _gc.collect()
    return r


def sheet_names():
    """
    returns a list of ALL sheets names (not all companies have all of them)
    """
    names = ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders',
             'Trading_Information', 'Financial_Highlights', 'Valuation_Measures',
             'Executives', 'Description',
             'Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates',
             'stats',
             'Executives', 'Description', 'analysis', 'Summary',
             'balance', 'cash_flow', 'income']
    _gc.collect()
    return names


def code_count(what='lines', detail=False):
    """
    prints out some of the information of the this package
    what - str - count what, default output everything - supporting -> lines, defs, chars
    detail - True / False - whether return count for each file or not
    """
    if what not in ['lines', 'defs', 'chars']:
        raise ValueError('Input parameter "what" must be one of lines, defs, chars, '
                         'not {}'.format(what))

    path = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
    dirs = _os.listdir(path)
    dirs = [i for i in dirs if 'database' not in i]  # get rid of database stuff
    # dirs.remove('__pycache__')
    count = {}
    count_def = {}
    count_char = {}

    for d in dirs:
        cnt = 0
        cnt_def = 0
        cnt_char = 0
        if '.py' in d and ('pyc' not in d):
            f = open(_os.path.join(path, d), mode='r')
            while True:  # reduce memory usage
                try:
                    line = f.readline()
                except UnicodeDecodeError:
                    cnt += 1
                    continue
                if not line:
                    break
                else:
                    cnt += 1
                    cnt_def += line.count('def')
                    cnt_char += len(line)

            f.close()
        elif _os.path.isdir(_os.path.join(path, d)):
            for dd in _os.listdir(_os.path.join(path, d)):
                if '.py' in dd:
                    f = open(_os.path.join(path, d, dd), mode='r')
                    while True:  # reduce memory usage
                        try:
                            line = f.readline()
                        except UnicodeDecodeError:
                            cnt += 1
                            continue
                        if not line:
                            break
                        else:
                            cnt += 1
                            cnt_def += line.count('def')
                            cnt_char += len(line)
                    f.close()
        if cnt != 0:
            count[d] = cnt
        if cnt_def != 0:
            count_def[d] = cnt_def
        if cnt_char != 0:
            count_char[d] = cnt_char
    _gc.collect()

    if what == 'lines':
        if detail:
            return count
        else:
            return sum(count.values())
    elif what == 'defs':
        if detail:
            return count_def
        else:
            return sum(count_def.values())
    elif what == 'chars':
        if detail:
            return count_char
        else:
            return sum(count_char.values())


def clean():
    """
    clear up the unused memory in IDE (trying to)
    using gc.collect()
    """
    _gc.collect()
