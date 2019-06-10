import os
import pandas as _pd

p = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
global datapath
datapath = os.path.join(p, 'database')


def save_file(df, stock, name):
    path = os.path.join(datapath, stock, stock) + '_' + name + '.csv'
    try:
        d = _pd.read_csv(path)
        d = d[list(d)[1:]]
    except FileNotFoundError:
        d = _pd.DataFrame()
    try:
        df = _pd.concat([df, d], axis=1)
        df = df.loc[:, ~df.columns.duplicated()]  # Drop duplicated column
    except Exception as e:
        print("Exception in save_file: " + str(e))
    try:
        columns_title = list(df)[1:]
        columns_title.sort(key=lambda x: x.split('/')[-1:-3:-1], reverse=True)  # Sort index by Y & M
        columns_title.insert(0, 'Statements')
        df = df.reindex(columns=columns_title)  # Swap columns
    except Exception as e:
        print("Exception in save_file: " + str(e))
    df.to_csv(path, index=False)


def save_analysis(dfs, stock):
    path = os.path.join(os.path.join(datapath, stock), stock)
    names = ['Earnings_Estimate', 'Revenue_Estimate', 'Ernings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates']
    for i in range(len(dfs)):
        dfs[i].to_csv(path + '_' + names[i] + '.csv', index=False)


def save_dfs(dfs, stock, names):
    path = os.path.join(datapath, stock, stock)
    for i in range(len(dfs)):
        dfs[i].to_csv(path + '_' + names[i] + '.csv', index=False)

def save(df, path, name='temp', file_type='csv',mode='w'):
    #path=input("Enter your path here: ")
    cnt=0
    while True:
        try:
            df.to_csv(path+name+'.'+file_type, index=False)
            break
        except FileNotFoundError:
            path=input("File not right, enter your path here: ")
        cnt+=1
        if cnt==3:
            print("Please check your path, it should be something like: ",end='')
            path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))        
