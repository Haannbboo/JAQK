from ..operations.Open import open_file as _open_file


def Earnings_Estimate(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet pf Earnings Estimate in yahoo finance's analysis
    '''
    df=_open_file(stock, name='Earnings_Estimate')
    return df

def Earnings_History(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet of Earnings History in yahoo finance's analysis
    '''
    df=_open_file(stock, name='Earnings_History')
    return df

def EPS_Revisions(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet of EPS Revisions in yahoo finance's analysis
    '''
    df=_open_file(stock, name='EPS_Revisions')
    return df

def EPS_Trend(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet of EPS Trend in yahoo finance's analysis
    '''
    df=_open_file(stock, name='EPS_Trend')
    return df

def Growth_Estimates(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet of Growth Estimates  in yahoo finance's analysis
    '''
    df=_open_file(stock, name='Growth_Estimates')
    return df

def Revenue_Estimate(stock):
    '''
    stock - a company's code (eg. AAPL)
    returns a csv sheet of Revenue Estimate in yahoo finance's analysis
    '''
    df=_open_file(stock, name='Revenue_Estimate')
    return df
