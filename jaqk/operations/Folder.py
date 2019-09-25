import os as _os
import pandas as _pd

from .Path import datapath


def create_folder(stock, path='default', setup=False):
    if path == 'default':
        ppath = datapath(True, stock) # jaqk/database/AAPL
    else:
        if setup is True:
            ppath = _os.path.join(path, stock) # setup_path/AAPL
        elif setup is False:
            ppath = datapath(True, path, stock) # jaqk/path/AAPL
    if _os.path.isdir(ppath):  # If dir existed
        pass
    else:
        _os.makedirs(ppath)  # Create directory


def exist(stock, file, update=False, error=None):
    p1 = datapath(True, stock, stock)
    # if it needs update，then view it as not existing
    # and the save_file func handles the duplication
    if update:
        return False
    
    if isinstance(file, str):
        path = p1 + '_' + file + '.csv'
        return _os.path.exists(path)
    elif isinstance(file, list):
        paths = [p1 + '_' + f + '.csv' for f in file]
        r = '&'.join([str(_os.path.exists(pp)) for pp in paths])
        return eval(r)
    else:
        raise TypeError("Parameter 'file' should be either a string or a list of strings")


def is_full(company):
    return len(_os.listdir(datapath(True, company)))>=18


class error_record(object):

    def __init__(self,  activate=True):
        self.activate = activate
        self.path = datapath(False, 'Spyder', 'error.csv')
        self.tolerance_factor = 3
        try:
            self.csv = _pd.read_csv(self.path)
        except FileNotFoundError:
            self.csv = _pd.DataFrame()

    def is_failed(self, company, sheet):
        if self.activate is False:
            return False
        name = '{}_{}'.format(company, sheet)
        
        try:
            error_piece = self.csv[self.csv['Error'] == name]
        except KeyError:
            error_piece = _pd.DataFrame()
            
        flag_failed = len(error_piece)==1
        flag_empty_csv = len(self.csv) != 0
        flag_tolerance = error_piece.get('Tolerance', True)
        if flag_tolerance is True:
            pass
        else:
            flag_tolerance = flag_tolerance.squeeze()>=self.tolerance_factor
        return flag_failed and flag_empty_csv and flag_tolerance

    def save_failed(self, company, sheet, exception):
        if exception is None:
            return
        if self.activate is False:
            return
        
        name = '{}_{}'.format(company, sheet)

        flag_empty_csv = len(self.csv) != 0  # csv empty or not
        try:
            df = self.csv[self.csv['Error'] == name]
        except KeyError:
            df = _pd.DataFrame([[name, exception, 0]])
            
        if len(df) == 0:
            df = _pd.DataFrame([[name, exception, 0]])
            flag_error_exist = False
        else:
            flag_error_exist = True
            
        if flag_error_exist is True:
            index = df.index.values[0]
            self.csv['Tolerance'][index] += 1
            self.csv.to_csv(self.path, header=True, mode='w', index=False)
        elif flag_error_exist is False: 
            if len(self.csv) == 0:
                df.columns = ['Error', 'Info', 'Tolerance']
                header = True
            else:
                header = False

            df.to_csv(self.path, header=header, mode='a+', index=False)
