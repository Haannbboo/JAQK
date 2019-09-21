import os as _os
import pandas as _pd

from .Path import datapath


def save_file(df, stock, name, update=False):
    """Main saver, save file to database

    If it's for update, it will open the old sheet and concatenate new data into the correct columns.

    Args:
        df: pandas DataFrame to be saved
        stock: str - which stock does df belongs to
        name: str - which sheet is df
        update: bool - identify if it's for update or not
    """
    path = datapath(True, stock, stock + '_' + name + '.csv')

    if not update:
        pass
    elif update:
        try:
            d = _pd.read_csv(path)  # open old
            d = d[list(d)[1:]]
        except FileNotFoundError:
            d = _pd.DataFrame()
        try:
            first = df.iloc[0:, 0]  # first column
            df = _pd.concat([df[list(df)[1:]], d], axis=1)
            df = df.loc[:, ~df.columns.duplicated()]  # Drop duplicated column
        except Exception as e:
            print("Exception in save_file: " + str(e))
        try:
            columns_title = list(df)
            # Sort column by Year&Month
            columns_title.sort(key=lambda x: x.split('/')[-1:-3:-1], reverse=True) 
            df = df.reindex(columns=columns_title)  # Swap columns
            df = _pd.concat((first, df), axis=1, ignore_index=False)
        except Exception as e:
            print("Exception in save_file: " + str(e))
    df.to_csv(path, index=False)


def save_analysis(dfs, stock):
    path = datapath(True, stock, stock)
    names = ['Earnings_Estimate', 'Revenue_Estimate', 'Ernings_History',
             'EPS_Trend', 'EPS_Revisions', 'Growth_Estimates']
    for i in range(len(dfs)):
        dfs[i].to_csv(path + '_' + names[i] + '.csv', index=False)


def save_dfs(dfs, stock, names):
    path = datapath(True, stock, stock)
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
    if test is False:
        window = sg.Window('Save to path')
        _, values = window.Layout(form_rows).Read()
        window.Close()
        path = values['save']
    elif test is True:
        window = sg.Window('Save to path')
        window.Close()
        path = datapath(False, 'database', 'test')
    # path=values['save']
    if path == '' or path is None:
        print("You didn't choose a path for saving... Please choose one.")
        return
    try:
        p = _os.path.join(path, name + file_type)
        df.to_csv(p, mode=mode)
    except Exception as e:
        print("Exception in client saver: " + str(e))
        return
    if prt and (not test):
        print("Saved data sheet to " + p)
