#from operations.Format import _decimal

#from operations.Path import path as _path


from calculations import rank

#from operations.Open import open_file as _open_file

from factors import cash_flow, income, balance, key, stats


def _factor(df, factor):
    f=_decimal(df[df['Statements'].isin([factor])].values[0][1:])
    return f



global _factor_dic
_factor_dic={'FCF':'cash_flow','IC':'balance','NIBCLS':'balance','Invested_Book_Capital':'balance'}




