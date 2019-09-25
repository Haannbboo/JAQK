import os as _os
import gc as _gc

# __author__=='Hanbo'
# __version__=='0.0.1'


from .factors.factors import get_factors

from .operations.Save import save
from .operations.Tools import (database_count, database_clear, factors_names,
                               sheet_names, code_count, clean, success_rate)
from .operations.Open import open_stock_list
from .operations.Get import get_sheet, get_desc
from .operations.Path import datapath

from .calculations import *
from .factors import cash_flow, income, balance, key, stats
from .Spyder.update_main import update, get_last_update, load_stock_list
from .Spyder.main_loop import main

from .setup import setup


from .operations.Path import path

from .test2 import test # unittest


# if len(_os.listdir(datapath(True))) - 2 < 100:
#     print("There is not sufficient data in the database. Use main() to retrieve data")


_gc.collect()
