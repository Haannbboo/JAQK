import pandas as _pd
# import os as _os
import numpy as _np

from collections import Iterable as _iter

from ..operations.Open import open_file as _open_file
from ..operations.Path import path as _path
from ..operations.Format import factor as _factor
from ..operations.Format import year_convert


def get_factors(companies, factors, year='NEWEST'):
    # not handling year now
    """
    companies - list of companies
    factors - list of factors
    year - default NEWEST, list of years
    companies, factors, year - maximum two of them can be
    """
    if isinstance(companies, str):
        companies = [companies]  # string - list
    elif not isinstance(companies, _iter):
        raise TypeError("Parameter 'companies' should be iterable, not "
                        + type(companies).__name__)  # iterable -> for later listcamp
    if year != True and not isinstance(year, _iter):
        raise TypeError("Parameter 'year' should be one of 'NEWEST', True, or [year, year], not "
                        + type(year).__name__)
    if isinstance(factors, list) and isinstance(year, list):
        if len(year) != 1 and len(factors) != 1 and len(companies) != 1:
            raise ValueError(
                "When you want sheet for multiple factors with multiple companies, only a specific year is supported")
    if year != True and year != 'NEWEST' and (year[0] not in [2015, 2016, 2017, 2018, 2019]):
        raise TypeError("Parameter 'year' should be [int, int, ...] with int being a year")
    if isinstance(factors, str):
        factors = [factors]  # string - list
    paths = [_path(f) for f in factors]  # things below is for drop duplicates
    d = {}
    for i in range(len(paths)):  # Avoid crowded IO
        if d.get(paths[i], 'no') == 'no':
            d[paths[i]] = [factors[i]]
        else:
            d[paths[i]] += [factors[i]]
    # for c in companies:
    #       a=_np.concatenate(tuple([_factor(_open_file(c, k), v, False) for k, v in d.items()]),
    #                         axis = 1)
    if year != 'NEWEST' and len(factors) > 1:
        if len(companies) != 1:
            raise ValueError(
                "When you want sheet for multiple factors with multiple years, only ONE specific company is supported")
        a = _np.concatenate(tuple([_np.concatenate(
            [_factor(_open_file(companies[0], k), v, year) for k, v in d.items()]
        )]), axis=1)
    else:
        a = _np.concatenate(tuple([_np.concatenate(tuple(
            [_factor(_open_file(c, k), v, year) for k, v in d.items()]
        ), axis=1) for c in companies]))

    if year != 'NEWEST':
        # year=True or [2018, 2017]
        dff = _open_file(companies[0], list(d.keys())[0])
        if year == True:
            # year=True
            years = list(dff)[1:]
            df = _pd.DataFrame(a, index=factors)
            df.columns = years
            return df
        else:
            # year=[2018, 2017]
            years = year_convert(year, list(dff))
            df = _pd.DataFrame(a, index=factors)
            df.columns = years
            return df
    else:
        # year='NEWEST'
        df = _pd.DataFrame(a, index=companies)
        df.columns = factors
        return df
    if len(factors) > 1 and len(years) > 1:
        # multiple factors and 
        df = _pd.DataFrame(a, index=factors)
        df.columns = years
        return df

    # problem here
    # df.columns=factors # when only one factor is here, the columns name should be date rather than factors
