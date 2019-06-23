import os as _os
import gc as _gc

# __author__=='Hanbo'
# __version__=='0.0.1'


from .stock import financials, analysis, profile, prices
# from .stock import financials
from .stock.profile import description as desc

from .basics.stocks import stock_list

from .factors.factors import get_factors

from .operations.Save import save  # done
from .operations.Tools import (database_count, database_clear, factors_names,
                               sheets_names, code_count)
from .operations.Open import open_file
# from .operations.Open import open_general as _open_general


# calculation.key.Beta is not done

#from .calculation import *
from .calculations import rank
from .factors import cash_flow, income, balance, key, stats
from .get import update, getLastUpdate, main_get, load_stock_list, setup, datapath

from .operations.Path import path  # not tested

from .test2 import test # unittest

'''
def datapath():
    try:
        from .get import setup_path
        datapath = setup_path
    except ImportError:
        datapath = _os.path.join(_os.path.dirname(__file__), 'database')
    return datapath
'''
    
if len(_os.listdir(datapath())) - 2 < 100:
    print("There is not sufficient data in the database. Use main_get() to retrieve data")


_gc.collect()
