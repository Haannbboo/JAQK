import os as _os
import pandas as _pd

p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
global datapath
datapath = _os.path.join(p, 'database')


def save_file(df, stock, name, update=False):
    path = _os.path.join(datapath, stock, stock) + '_' + name + '.csv'

    if not update:
        pass
    elif update:
        try:
            d = _pd.read_csv(path)
            d = d[list(d)[1:]]
        except FileNotFoundError:
            d = _pd.DataFrame()
        try:
            first = df.iloc[0:, 0]
            df = _pd.concat([df[list(df)[1:]], d], axis=1)
            df = df.loc[:, ~df.columns.duplicated()]  # Drop duplicated column
        except Exception as e:
            print("Exception in save_file: " + str(e))
        try:
            columns_title = list(df)
            # temp=columns_title.pop(0)
            columns_title.sort(key=lambda x: x.split('/')[-1:-3:-1], reverse=True)  # Sort index by Y & M
            # columns_title.insert(0, temp)
            df = df.reindex(columns=columns_title)  # Swap columns
            df = _pd.concat((first, df), axis=1, ignore_index=False)
        except Exception as e:
            print("Exception in save_file: " + str(e))
    df.to_csv(path, index=False)


def save_analysis(dfs, stock):
    path = _os.path.join(_os.path.join(datapath, stock), stock)
    names = ['Earnings_Estimate', 'Revenue_Estimate', 'Ernings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates']
    for i in range(len(dfs)):
        dfs[i].to_csv(path + '_' + names[i] + '.csv', index=False)


def save_dfs(dfs, stock, names):
    path = _os.path.join(datapath, stock, stock)
    for i in range(len(dfs)):
        dfs[i].to_csv(path + '_' + names[i] + '.csv', index=False)


def save(df, name, file_type='.csv', mode='w', prt=True, test=False):
    """
    saver of financial sheets for client
    df - pandas dataframe to save
    name - desired name
    file_type - file type, need to add '.' (e.g - .csv / .xls)
    mode - recommend not change, default 'w' (create file if not exist, cover the data with each writes)
    prt - print out result or not - Saved dataframe to {}(path)
    test - for testing only
    """
    import PySimpleGUI as sg
    # path=input("Enter your path here: ")
    if '.' not in file_type:
        raise ValueError("Parameter file_type in save() should has '.' before the file format...")
    form_rows = [[sg.Text('Choose the save path')],
                 [sg.Text('Save path: ', size=(15, 1)), sg.InputText(key='save'), sg.FolderBrowse()],
                 [sg.Submit(), sg.Cancel()]]
    if test == False:
        window = sg.Window('Save to path')
        _, values = window.Layout(form_rows).Read()
        window.Close()
        path = values['save']
    elif test == True:
        window = sg.Window('Save to path')
        window.Close()
        path = _os.path.join(datapath, 'test')
    # path=values['save']
    if path == '' or None:
        print("You didn't choose a path for saving...")
        return
    try:
        p = _os.path.join(path, name + file_type)
        df.to_csv(p, mode=mode)
    except Exception as e:
        print("Exception in client saver: " + str(e))
        return
    if prt and (not test):
        print("Saved dataframe to " + p)
