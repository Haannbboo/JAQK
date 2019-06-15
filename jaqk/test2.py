#import os
import gc as _gc

# __author__=='Hanbo'
# __version__=='0.0.1'

#global datapath
#datapath=os.path.join(os.path.dirname(__file__), 'database')

###########################
import unittest as _unittest

from .stock.test_stock import test_stocks
from .factors.test_factors import test_factors
from .basics.test_basics import test_basics
from .calculations.test_calculations import test_calculations
from .operations.test_operations import test_operations
'''
class MainTest(unittest.Testcase):
    def setUp(self):
        self.datapath=os.path.join(os.path.dirname(__file__), 'database')
    def financials_test(self):
        pass
    def annalysis_test(self):
        pass


if __name__=='__main__':
    unittest.main()
'''

def test():
    #from .stock.test_stock import test_stocks
    _unittest.main(__name__)
    _gc.collect()

