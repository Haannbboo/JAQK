from ..operations.Open import open_file as _open_file
from ..operations.Trans import _t_util, _translate


def Key_Executives(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet of Key Executives in yahoo finance for the company
    '''
    df=_open_file(stock, name='Executives')
    return df

def description(stock,language='en'):
    '''
    stock - a company's code (eg. AAPL)
    language - default English, choose your language (e.g zh for mandarin)
    returns the description of the company in yahoo finance
    '''
    df=_open_file(stock, name='Description')
    desc=df['Description'][0]
    if language!='en':
        desc=_translate(desc,language)
    return desc

def summary(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet of Summary of the company in yahoo finance
    '''
    df=_open_file(stock, name='Summary')
    return df
