import os as _os


#__author__=='Hanbo'
#__version__=='0.0.1'

#global datapath
datapath=_os.path.join(_os.path.dirname(__file__), 'database')


from .stock import financials, analysis, profile, prices
from .stock.profile import description as desc

from .basics.stocks import stock_list

from .factors.factors import get_factors

from .operations.Save import save # done
from .operations.Tools import database_count, factors_names, sheets_names, code_count
from .operations.Open import open_file

#from operations.Open import open_file, open_general

#from operations.Trans import translate



# calculation.key.Beta is not done

from .calculation import *
from .get import update, getLastUpdate, main_get # Connected well

from .operations.Path import path # not tested

if len(_os.listdir(datapath))-2<100:
    print("There is not sufficient data in the database. Use main_get() to retrieve data")



class test:
    # Not supporting deliberate handlers of errors
    def __init__(self,stock):
        self.stock=stock
    def test_financials(self):
        df=financials.stats(self.stock)
        df=financials.Valuation_Measures(self.stock)
        df=financials.Financial_Highlights(self.stock)
        df=financials.Trading_Information(self.stock)
        df=financials.Income(self.stock)
        df=financials.Balance(self.stock)
        df=financials.Cash_Flow(self.stock)
    def test_analysis(self):
        df=analysis.EPS_Revisions(self.stock)
        df=analysis.EPS_Trend(self.stock)
        df=analysis.Earnings_Estimate(self.stock)
        df=analysis.Earnings_History(self.stock)
        df=analysis.Growth_Estimates(self.stock)
        df=analysis.Revenue_Estimate(self.stock)
    def test_profile(self):
        df=profile.Key_Executives(self.stock)
        df=profile.description(self.stock)
        df=profile.description(self.stock, 'zh')
        df=profile.summary(self.stock)
    def test_trading(self):
        df=prices.daily('BABA')
        df=prices.daily('BABA','2017-01-01')
        df=prices.daily('BABA','2017-01-01','2018-09-09')
        df=prices.weekly('BABA')
        df=prices.weekly('BABA','2017-01-01')
        df=prices.weekly('BABA','2017-01-01','2018-09-09')
        df=prices.monthly('BABA')
        df=prices.monthly('BABA','2017-01-01')
        df=prices.monthly('BABA','2017-01-01','2018-09-09')
    def test_stocks_list(self):
        df=stock_list()
        assert len(list(df))==9
        df=stock_list('NYSE')
        assert len(list(df))==9
        df=stock_list('NASDAQ')
        assert len(list(df))==9
    def test_calculation(self):
        pass
    
