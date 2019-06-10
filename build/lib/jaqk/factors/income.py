import sys as _sys
_sys.path.append('..') # add previous directory to model object

from operations.Format import factor as _factor
from operations.Open import open_file as _open_file


class income:
    def __init__(self,stock):
        self.__stock=stock
        self.__df=_open_file(stock,'income')
    def Total_Revenue(self):
        return _factor(self.__df, 'Total_Revenue')
    def Cost_of_Revenue(self):
        return _factor(self.__df, 'Cost of Revenue')
    def Gross_Profit(self):
        return _factor(self.__df, 'Gross Profit')
    def Research_Development(self):
        return _factor(self.__df, 'Research Development')
    def Total_Operating_Expenses(self):
        return _factor(self.__df, 'Total Operating Expenses')
    def Interest_Expense(self):
        return _factor(self.__df, 'Interest Expense')
    def Income_Before_Tax(self):
        return _factor(self.__df, 'Income Before Tax')
    def Net_Income(self):
        return _factor(self.__df, 'Net Income')
    def Net_Income_Applicable_To_Common_Shares(self):
        return _factor(self.__df, 'Net Income Applicable To Common Shares')

def Total_Revenue(stock):
    df=_open_file(stock,'income')
    return _factor(df, 'Total_Revenue')

def Cost_of_Revenue(self):
    df=_open_file(stock,'income')
    return _factor(df, 'Cost of Revenue')

def Gross_Profit(self):
    df=_open_file(stock,'income')
    return _factor(df, 'Gross Profit')
