import os as _os
import gc as _gc

# __author__=='Hanbo'
# __version__=='0.0.1'

# global datapath
datapath = _os.path.join(_os.path.dirname(__file__), 'database')

from .stock import financials, analysis, profile, prices
# from .stock import financials
from .stock.profile import description as desc

from .basics.stocks import stock_list

from .factors.factors import get_factors

from .operations.Save import save  # done
from .operations.Tools import database_count, factors_names, sheets_names, code_count
from .operations.Open import open_file

# from operations.Open import open_file, open_general

# from operations.Trans import translate


# calculation.key.Beta is not done

from .calculation import *
from .get import update, getLastUpdate, main_get  # Connected well

from .operations.Path import path  # not tested

from .test2 import test


if len(_os.listdir(datapath)) - 2 < 100:
    print("There is not sufficient data in the database. Use main_get() to retrieve data")

_gc.collect()
