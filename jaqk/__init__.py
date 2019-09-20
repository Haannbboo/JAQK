import os as _os
import gc as _gc

# __author__=='Hanbo'
# __version__=='0.0.1'


from .stock import financials, analysis, profile, prices

from .stock.profile import description as desc

from .factors.factors import get_factors

from .operations.Save import save
from .operations.Tools import (database_count, database_clear, factors_names,
                               sheets_names, code_count, clean)
from .operations.Open import open_file, open_stock_list

from .calculations import *
from .factors import cash_flow, income, balance, key, stats
from .get import update, getLastUpdate, main_get, load_stock_list, datapath

from .setup import setup

from .operations.Path import path

from .test2 import test # unittest

    
if len(_os.listdir(datapath())) - 2 < 100:
    print("There is not sufficient data in the database. Use main_get() to retrieve data")


_gc.collect()
