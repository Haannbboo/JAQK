import os as _os
# import pandas as pd
import numpy as _np
from scipy import stats as _Stats

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
    if not isinstance(Factor, str):
        raise TypeError("Parameter 'factors' should a string")
    if not isinstance(stock, str):
        raise TypeError("Parameter 'stock' should a string")
    p0 = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
    p = _os.path.join(p0, 'database')
    name = _path(Factor)
    dirs = _os.listdir(p)
    d = [i for i in dirs if _os.path.isdir(_os.path.join(p, i))]
    # return d
    # i+'_'+name in set(os.listdir(os.path.join(path,i))
    r = []
    for i in d:
        try:
            df = _open_file(i, name)
            f = _factor(df, Factor)
            if len(f) != 4:
                continue
            r.append(f)
        except Exception as e:
            # input('Exception: '+str(e))
            continue
    n = _np.stack(r)
    stock_value = _factor(_open_file(stock, name), Factor)
    result = [round(_Stats.percentileofscore(n[:, i], stock_value[i]), 4) for i in range(len(stock_value))]
    del n, r, d
    _gc.collect()
    return result


def percentile(Factor, percentage=80):
    """
    Factor - str
    percentile - int, percentage you want to check
    returns a list of companies with top percentile for the factor
    """
    if not isinstance(Factor, str):
        raise TypeError("Parameter 'factors' should a string")
    if not isinstance(percentage, int):
        raise TypeError("Parameter 'percentage' should a int")
    elif not 0 <= percentage <= 100:
        raise ValueError("Parameter 'percentage' should be between 0-100")
    p = _os.path.join(_os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir)), 'database')
    flag = False  # flag for using external factors
    try:
        name = _path(Factor)
    except ValueError:
        if Factor in _factor_dic.keys():
            flag = True
            name = _factor_dic[Factor]

        else:
            raise ValueError("No support for factor '" + Factor + "'")
    dirs = _os.listdir(p)
    d = [i for i in dirs if _os.path.isdir(_os.path.join(p, i))]
    r = []
    d2 = d[:]
    for i in d2:
        try:
            df = _open_file(i, name)
            if flag:
                f = eval(name + '._' + Factor + '(df)')  # call the function
            else:
                f = _factor(df, Factor)
            if len(f) != 4:
                d.remove(i)
                continue
            else:
                r.append(f)
                # input("Appended")
        except Exception as e:
            d.remove(i)
            # print(r)
            # input('Exception: '+str(e))
    n = _np.stack(r)
    assert len(n) == len(d)
    target = [_np.percentile(n[:, i], percentage) for i in range(4)]
    result = [[d[i] for i in range(len(n)) if n[i][j] >= target[j]] for j in range(len(target))]
    return result


def _CAGR(Factor, years):  # compound anual growth rate, not developed
    pass
