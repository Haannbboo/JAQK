import os as _os
# import pandas as pd
import numpy as _np
from scipy import stats as _Stats
import pandas as _pd

import gc as _gc

from ..operations.Format import factor as _factor
from ..operations.Path import path as _path
from ..operations.Open import open_file as _open_file


# from factors import _balance, cash_flow, key, stats

global _factor_dic
_factor_dic = {'FCF': 'cash_flow', 'IC': 'balance', 'NIBCLS': 'balance', 'Invested_Book_Capital': 'balance'}


def factor_percentile(Factor, stock):
    """
    Factor - str
    stock - company you want to check
    returns the percentile of the factor of the stock - a list of floats
    """

    _instance_check(Factor, str) # raise ValueError
    _instance_check(stock, str)
    
    df = _get_df(Factor)
    
    result = df.rank().loc[stock].tolist() # result
    #stock_value = _factor(_open_file(stock, name), Factor)
    #result = [round(_Stats.percentileofscore(n[:, i], stock_value[i]), 4) for i in range(len(stock_value))]
    _gc.collect()
    return result


def percentile(Factor, percentage=80):
    """
    Factor - str
    percentile - int, percentage you want to check
    returns a list of companies with top percentile for the factor
    """
    # error control
    _instance_check(Factor, str)
    _instance_check(percentage, int)
    _value_check(percentage)

    df = _get_df(Factor) # get dataframe from setup path
    
    target = df[df>=df.quantile(percentage/100.0)].dropna(thresh=1) # select percentile group
    result = [target[i].dropna().index.tolist() for i in list(df)] # choose notna group
    _gc.collect()
    return _np.array(result)

def best(Factor):
    df = _get_df(Factor)
    _gc.collect()
    return _np.array(df.idxmax(), dtype=str) # df.idxmax()

def worse(Factor):
    df = _get_df(Factor)
    _gc.collect()
    return _np.array(df.idxmin(), dtype=str)


def _get_df(Factor): # wrap up (lots of work below)
    # NOT THE SAME as jaqk.open_file
    try:
        df = _pd.read_csv(_os.path.join(_datapath(), 'general', '_'.join(Factor.split(' '))+'.csv'), index_col=0)
        b, diff = _is_updated(df)
        if b == False:
            pass
        else:
            df_new = _percentile_core(Factor, diff, update=b)
            df = _update_old_one(df_new, df, Factor)
    except FileNotFoundError:
        df = _percentile_core(Factor)
    return df


def _percentile_core(Factor, diff=None, update=False):
    # print('_percentile_core')
    flag = False
    _factor_dic = {'FCF': 'cash_flow', 'IC': 'balance', 'NIBCLS': 'balance', 'Invested_Book_Capital': 'balance'}
    try:
        name = _path(Factor)
    except ValueError:
        if Factor in _factor_dic.keys(): # calculated factors
            flag = True
            name = _factor_dic[Factor]
        else:
            msg="No support for factor '{}'"
            raise ValueError(msg.format(Factor))
    d = _needs_update(diff)
    r = []
    d2 = d[:]
    for i in d2:
        try:
            if flag: #
                exec('from ..factors.{} import {} as {}'.format(name, Factor, Factor))
                f = eval(Factor + '(i)')  # call the function from calculation
            else:
                df = _open_file(i, name)
                f = _factor(df, Factor)
            if len(f) < 4 and name in ['income', 'balance', 'cash_flow']:
                d.remove(i)
                continue
            else:
                r.append(f)
        except Exception as e: # handles filenontfound, wrong dir, etc.
            d.remove(i)
            _write_error(i)
            # print(r)
            # input('Exception: '+str(e))
    n = _np.stack(r)
    assert len(n) == len(d)
    df = _pd.DataFrame(n, index=d)
    df.columns = [str(i) for i in list(df)]
    if not update:
        _save_csv(df, Factor)
    del d, r, d2, n
    _gc.collect()
    return df


def _is_updated(df): # only for rank
    # print('_is_updated')
    index = df.index.tolist()
    try:
        f = open(_os.path.join(_datapath(), 'general', 'error_cache.txt'))
        er = f.read().split('\n')
        f.close()
    except FileNotFoundError:
        er = []
    index = set(index + er)
    dirs = set(_os.listdir(_datapath()))
    diff = dirs.difference(index)
    if len(diff)==0:
        return False, {}
    else:
        return True, diff
    

def _write_error(i):
    path = _os.path.join(_datapath(),'general', 'error_cache.txt')
    try:
        f = set(open(path).readlines())
    except FileNotFoundError:
        f = set()
    f.update(set([i]))
    with open(path, 'w') as e:
        e.write('\n'.join(f))

def _needs_update(diff):
    # print('_needs_update')
    if diff is None:
        dirs = _os.listdir(_datapath()) # update everything
        d = [i for i in dirs if _os.path.isdir(_os.path.join(_datapath(), i))] # avoid files
    else:
        d = list(diff)
    return d

def _update_old_one(df_new, df_old, Factor):
    # print('_update_old_one')
    df = _pd.concat([df_old, df_new])
    _save_csv(df, Factor)
    return df

def _save_csv(df, Factor):
    # print('_save_csv')
    # input("Check point")
    df.to_csv(_os.path.join(_datapath(), 'general', '_'.join(Factor.split(' '))+'.csv'))

def _datapath(setup=True):
    """
    The global datapath for all other file. It sets your selected path in jaqk.setup() as the main datapath, and all data will be added/deleted from there.
    """
    try:
        p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
        with open(_os.path.join(p, 'setup_cache.txt')) as w:
            path = w.read()
        if setup==True:
            return path
        else:
            return _os.path.join(p, 'database')
    except FileNotFoundError:
        return _os.path.join(p, 'database')

def _instance_check(param, dtype):
    msg = "Parameter '{}' should a string, not a {}."
    if not isinstance(param, dtype):
        dtype = type(param).__name__
        raise TypeError(msg.format(str(param), dtype))

def _value_check(p):
    # print("_check_percentage")
    msg="Parameter 'percentage' should be in the interval [0, 100]. Try {} instead."
    if 0<p<1:
        m = 100 if p*100>100 else p*100
        raise ValueError(msg.format(m))
    elif p>100:
        m = 100 if p/100>100 else round(p/100, 2)
        raise ValueError(msg.format(m))

    
        
    
def _CAGR(Factor, years):  # compound anual growth rate, not developed
    pass
