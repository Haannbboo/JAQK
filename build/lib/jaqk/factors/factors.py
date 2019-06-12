import pandas as _pd
import os as _os
import numpy as _np

from collections import Iterable as _iter


from ..operations.Open import open_file as _open_file
from ..operations.Path import path as _path
from ..operations.Format import factor as _factor


def get_factors(companies, factors, year='NEWEST'):
    # not handling year now
    '''
    companies - list of companies
    factors - list of factors
    year - default NEWEST, list of years
    companies, factors, year - maximum two of them can be 
    '''
    if isinstance(companies, str):
        companies=[companies] # string - list
    elif not isinstance(companies, _iter):
        raise TypeError("Parameter 'companies' should be iterable, not "
                        +type(companies).__name__) # iterable -> for later listcamp
    if isinstance(factors, list) and isinstance(year, list):
        if len(year)!=1 and len(factors)!=1 and len(companies)!=1:
            raise ValueError("When you want sheet for multiple factors with multiple companies, only a specific year is supported")
    if isinstance(factors, str):
        factors=[factors] # string - list
    paths = [_path(f) for f in factors] # things below is for drop duplicates
    d = {}
    for i in range(len(paths)):  # Avoid crowded IO
        if d.get(paths[i], 'no') == 'no':
            d[paths[i]] = [factors[i]]
        else:
            d[paths[i]] += [factors[i]]
    #for c in companies:
 #       a=_np.concatenate(tuple([_factor(_open_file(c, k), v, False) for k, v in d.items()]),
 #                         axis = 1)

    
    a=_np.concatenate(tuple
                      (
                          [_np.concatenate
                           (tuple
                            (
                                [_factor
                                 (_open_file(c, k), v, year) for k, v in d.items()
                                 ]
                                ),
                            axis = 1
                            )
                           for c in companies]
                          )
                      )
                     
    df=_pd.DataFrame(a, index=companies)
    # problem here
    df.columns=factors # when only one factor is here, the columns name should be date rather than factors
    return df


        
        


''' for debugging
factors=['Net Income','Total Assets','Total Revenue','Gross Profit']
paths = [_path(f) for f in factors]
d={}
for i in range(len(paths)):  # Avoid crowded IO
    if d.get(paths[i], 'no') == 'no':
        d[paths[i]] = [factors[i]]
    else:
        d[paths[i]] += [factors[i]]
df=_open_file('AAPL','income')
'''
