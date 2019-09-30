import gc as _gc
import numpy as _np
import os as _os
import pandas as _pd
import time as _time

from ..operations.Format import factor as _factor
from ..operations.Open import open_file as _open_file
from ..operations.Path import path as _path
from ..operations.Path import datapath


def factor_percentile(Factor, stock, prt_time=False):
    """Get the percentile ranking of a factor of a stock.

    Opens all files containing param Factor in database,
    rank the Factor of given stock, save the data in a cache csv file.

    Args:
        Factor: str - One factor in database.
        stock: str - A ticket names.

    Returns:
        A list of floats with length = years contained in database
        and value of the ranked percentage.

    Raises:
        TypeError: assess type of param Factor and stock.
    """
    s = _time.time()
    _instance_check(Factor, str)  # raise TypeError
    _instance_check(stock, str)

    df = _get_df(Factor)

    result = df.rank().loc[stock] / len(df)
    result = [round(i, 5) for i in result.tolist()]

    e = _time.time()
    if prt_time is True:
        print("Time taken for <jaqk.rank.factor_percentile> with <{} companies> is {}s".format(len(df), round((e-s)/5, 4)))
    _gc.collect()
    return result


def percentile(Factor, percentage=80):
    """Get the upper percentile companies.

    Opens all files containing param Factor in database,
    rank the Factor of given stock, save the data in a cache csv file.

    Args:
        Factor: str - One factor in database.
        percentage: int - upper percentile companies of a factor.

    Returns:
        a numpy 2D array (shape=(4, 1)) of tickets that are above percentage in all companies of the factor

    Raises:
        TypeError: assess type of param Factor and percentage
        ValueError: assess if param percentage within [0, 100]
    """

    _instance_check(Factor, str)  # TypeError
    _instance_check(percentage, int)
    _value_check(percentage)  # ValueError

    df = _get_df(Factor)  # get DataFrame from setup path

    target = df[df >= df.quantile(percentage / 100.0)].dropna(thresh=1)  # select percentile group
    result = [_np.array(target[i].dropna().index.tolist()) for i in list(df)]  # get satisfied tickets

    _gc.collect()
    return _np.array(result)


def best(Factor):
    """Get the BEST performing company of a factor.

    Args:
        Factor: str - One factor in database.

    Returns:
        a numpy 2D array (shape=(4,1)) of BEST performing company.

    Raises:
        TypeError: assess type of param Factor.
    """
    _instance_check(Factor, str)  # raise TypeError

    df = _get_df(Factor)
    _gc.collect()
    return _np.array(df.idxmax(), dtype=str)  # df.idxmax()


def worst(Factor):
    """Get the WORST performing company of a factor.

    Args:
        Factor: str - One factor in database.

    Returns:
        a numpy 2D array (shape=(4,1)) of WORST performing company

    Raises:
        TypeError: assess type of param Factor.
    """
    _instance_check(Factor, str)  # raise TypeError

    df = _get_df(Factor)
    _gc.collect()
    return _np.array(df.idxmin(), dtype=str)


def _get_df(Factor):
    """Opens the factor data cache csv file

    Opens the factor data csv, get if update in stocks in database exists from _is_updated()
    call database cache update if needed.

    Args:
        Factor: str - One factor in database.

    Returns:
        a pandas DataFrame with ticket names (rows) vs ['0', '1', '2', '3'] (columns name).
    """
    # NOT THE SAME as jaqk.open_file or jaqk.open_general
    try:
        # using cache
        df = _pd.read_csv(_os.path.join(_datapath(), 'general', '_'.join(Factor.split(' ')) + '.csv'), index_col=0)
        b, diff = _is_updated(df) # check update, b -> boolean
        if b is False:
            pass
        else:
            df_new = _percentile_core(Factor, diff, update=b)
            df = _update_old_one(df_new, df, Factor)  # perform update on cache csv file
    except FileNotFoundError:
        df = _percentile_core(Factor) # indicate factor has no cache in database
    return df


def _percentile_core(Factor, diff=None, update=False):
    """Gets factor data when factor cache doesn't exist

    Iterate through company list, opens corresponding report and locate the factor,
    put factor data of each company in one row of final pandas DataFrame file.

    Args:
        Factor: str - One factor in database.
        diff: set/list - tickets that need update, passed into _needs_update().
        update: bool - is there tickets update or not, update factor data cache if yes.

    Returns:
        a pandas DataFrame with tickets (rows) vs ['0', '1', '2', '3'] (columns),
        contains number of the param Factor of each company in database.

    Raises:
        ValueError: check if Factor is in either database or calculations.
    """
    # NOT STABLE YET; EMPTY STACK OCCURS OCCASIONALY

    flag = False
    # _factor_dic: all calculated factors that are not in the original csv sheets
    _factor_dic = {'FCF': 'cash_flow', 'IC': 'balance', 'NIBCLS': 'balance', 'Invested_Book_Capital': 'balance'}

    try:
        name = _path(Factor)
    except ValueError:
        if Factor in _factor_dic.keys():  # calculated factors
            flag = True
            name = _factor_dic[Factor]
        else:
            msg = "No support for factor '{}'"
            raise ValueError(msg.format(Factor))

    d = _needs_update(diff)  # tickets needed to to iterate through
    r = []
    d2 = d[:]
    for i in d2:
        try:
            if flag:  # calculated factors
                exec('from ..factors.{} import {} as {}'.format(name, Factor, Factor))  # call calculations functions
                f = eval(Factor + '(i)')
            else:
                df = _open_file(i, name)
                f = _factor(df, Factor)
            if len(f) != 4 and name in ['income', 'balance', 'cash_flow']:
                d.remove(i)
                continue
            else:
                r.append(f)
        except Exception as e:  # drops the company with whatever problem
            d.remove(i)
            _write_error(i)  # record the error in a txt file

    if len(r) == 0:
        return None

    n = _np.stack(r)
    assert len(n) == len(d)
    df = _pd.DataFrame(n, index=d)
    df.columns = [str(i) for i in list(df)]
    if not update:  # if cache not exist
        _save_csv(df, Factor)
    del d, r, d2, n
    _gc.collect()
    return df


def _is_updated(df):  # only for rankings
    """Check if there's any updated tickets in database.

    Read the index (tickets) of df, compare it with database tickets.

    Args:
        df: pandas DataFrame of factor data cache in database.

    Returns:
        bool: whether there's update or not.
        diff: set - the new tickets name in database.
    """
    index = df.index.tolist()
    try:
        # Read error txt (baby version of log), record into a list
        f = open(_os.path.join(_datapath(), 'general', 'error_cache.txt'))
        er = f.read().split('\n')
        f.close()
    except FileNotFoundError:
        er = []
    index = set(index + er)  # original database
    dirs = set(_os.listdir(_datapath()))  # current database
    diff = dirs.difference(index)  # finding differences
    if len(diff) == 0:
        return False, {}
    else:
        return True, diff  # returns a set


def _write_error(i):
    """Record the companies with errors so in future such tickets won't be updated agrain

    Read erorrs into a list, then write the new error ticket

    Args:
        i: int - the counter in for loop in _percentile_core()

    Returns:
        None
    """
    path = _os.path.join(_datapath(), 'general', 'error_cache.txt')
    try:
        with open(path) as w:
            f = set(w.readlines())
    except FileNotFoundError:
        f = set()
    f.update({i})  # update as set([i])
    with open(path, 'w+') as e:
        e.write('\n'.join(f))


def _needs_update(diff):
    """Get the tickets that need to be updated with factors data in factors data cache.

    Args:
        diff: set - tickets that need update from _is_updated(), passed in through _percentile_core().

    Returns:
        list of ticket names that need to be updated
    """
    if diff is None:
        dirs = _os.listdir(_datapath())  # update everything
        d = [i for i in dirs if _os.path.isdir(_os.path.join(_datapath(), i))]  # eliminate non-directory files
    else:
        d = list(diff)
    return d


def _update_old_one(df_new, df_old, Factor):
    """Update the existing factors data cache in database.

    Call _save_csv() to save the new DataFrame.

    Args:
        df_new: new DataFrame generated in _percentile_core().
        df_old: old DataFrame derived from database.
        Factor: str - One factor in database.

    Returns:
        pandas DataFrame with all companies updated for param Factor
    """
    # print('_update_old_one')
    df = _pd.concat((df_old, df_new), sort=False)
    _save_csv(df, Factor)
    return df


def _save_csv(df, Factor):
    """Save DataFrame into csv file in database.

    Args:
        df: pandas DataFrame.
        Factor: str - One factor in database.

    Returns:
        None
    """
    df.to_csv(_os.path.join(_datapath(), 'general', '_'.join(Factor.split(' ')) + '.csv'))


def _datapath(setup=True):
    """
    The global datapath for all other file. It sets your selected path in jaqk.setup() as the main datapath, and all data will be added/deleted from there.
    """
    try:
        p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
        with open(_os.path.join(p, 'setup_cache.txt')) as w:
            path = w.read()
        if setup is True:
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
    msg = "Parameter 'percentage' should be in the interval [0, 100]. Try {} instead."
    if 0 < p < 1:
        m = 100 if p * 100 > 100 else p * 100
        raise ValueError(msg.format(m))
    elif p > 100:
        m = 100 if p / 100 > 100 else round(p / 100, 2)
        raise ValueError(msg.format(m))


def _CAGR(Factor, years):  # compound anual growth rate, not developed
    pass
