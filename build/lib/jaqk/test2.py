# import os
import gc as _gc
import unittest as _unittest

from .stock.test_stock import test_stocks
from .factors.test_factors import test_factors
from .basics.test_basics import test_basics
from .calculations.test_calculations import test_calculations
from .operations.test_operations import test_operations


def test():
    # from .stock.test_stock import test_stocks
    """
    Client function for testing EVERY method in this package
    """
    _unittest.main(__name__)
    _gc.collect()
