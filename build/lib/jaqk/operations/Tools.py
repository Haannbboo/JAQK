import os as _os
import gc as _gc
import pandas as _pd
import numpy as _np

p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
global datapath
datapath = _os.path.join(p, 'database')




def database_count():
    '''
    prints out the total number of companies and sheets in database
    '''
    a=len(_os.listdir(datapath))-2
    b=_os.walk(datapath) # generator
    c=[1]
    c=len([c[0]+1 for root, dirs, files in b for name in files])-12
    print("Total number of companies contained: {}".format(a))
    print("Total number of detailed sheets: {}".format(c))
    _gc.collect()


        
def factors_names(sheet=None):
    if sheet is None:
        dfs=(_pd.read_csv(_os.path.join(datapath, 'AAPL', c)) for c in _os.listdir(_os.path.join(datapath, 'AAPL'))) # generator
        r=[df.iloc[0:-1,0].values[1:] for df in dfs]
        r=[i.tolist()[j] for i in r for j in range(len(i.tolist()))]+list(_pd.read_csv(_os.path.join(datapath, 'AAPL', 'AAPL_Summary.csv')))[1:]
        r=_np.array(r, dtype='str')
    else:
        if sheet not in sheets_names():
            raise ValueError('Parameter sheet is wrong, use sheets_names() to find all sheets names')
        file='AAPL_{}.csv'.format(sheet)
        if sheet=='Summary':
            r=_np.array(list(_pd.read_csv(_os.path.join(datapath, 'AAPL', 'AAPL_Summary.csv')))[1:])
        else:
            r=_pd.read_csv(_os.path.join(datapath, 'AAPL', file)).iloc[0:-1, 0].values[1:]
    _gc.collect()
    return r


def sheets_names():
    '''
    returns a list of ALL sheets names (not all companies have all of them)
    '''
    names = ['major_holders', 'top_institutional_holders', 'top_mutual_fund_holders',
             'Trading_Information', 'Financial_Highlights', 'Valuation_Measures',
             'Executives', 'Description',
             'Earnings_Estimate', 'Revenue_Estimate', 'Earnings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates',
             'stats', 'statements', 'reports',
             'Executives', 'Description', 'analysis', 'Summary',
             'balance', 'cash_flow', 'income']
    return names


def code_count():
    '''
    prints out some of the information of the this package
    '''
    
    path=_os.path.abspath('../')
    dirs=_os.listdir(path)
    dirs=[i for i in dirs if 'database' not in i] # get rid of database stuff
    #dirs.remove('__pycache__')
    count={}

    for d in dirs:
        cnt=0
        if '.py' in d:
            f=open(_os.path.join(path, d), mode='r')
            while True: # reduce memory usage
                try:
                    line=f.readline()
                except UnicodeDecodeError:
                    cnt+=1
                    continue
                if not line:
                    break
                else:
                    cnt+=1
            f.close()
        elif _os.path.isdir(_os.path.join(path, d)):
            for dd in _os.listdir(_os.path.join(path, d)):
                if '.py' in dd:
                    f=open(_os.path.join(path, d, dd), mode='r')
                    while True: # reduce memory usage
                        try:
                            line=f.readline()
                        except UnicodeDecodeError:
                            cnt+=1
                            continue
                        if not line:
                            break
                        else:
                            cnt+=1
                    f.close()
        if cnt!=0:
            count[d]=cnt
    return sum(count.values())
    
