import pandas as _pd


from ..operations.Open import open_general as _open_general


def stock_list(exchange=None):
    if exchange is not None:
        _csv=_open_general(exchange+'.csv')
        df=_csv.drop('Unnamed: 9',axis=1)
    else:
        c1=_open_general('NASDAQ.csv')
        c2=_open_general('NYSE.csv')
        df=_pd.concat([c1,c2],ignore_index=True).drop('Unnamed: 9',axis=1) # drop redundant column
    return df

