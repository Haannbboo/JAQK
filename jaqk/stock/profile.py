import sys as _sys
_sys.path.append('..') # add previous directory to model object


from operations.Open import open_file as _open_file
from operations.Trans import _t_util, _translate


def Key_Executives(stock):
    df=_open_file(stock, name='Executives')
    return df

def description(stock,language='en'):
    df=_open_file(stock, name='Description')
    desc=df['Description'][0]
    if language!='en':
        desc=_translate(desc,language)
    return desc

def summary(stock):
    df=_open_file(stock, name='Summary')
    return df
