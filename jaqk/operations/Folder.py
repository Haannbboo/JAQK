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

    def __init__(self):
        self.path = datapath(False, 'Spyder', 'error.csv')
        try:
            self.csv = _pd.read_csv(self.path)
            self.errors = self.csv['Error'].values
        except FileNotFoundError:
            self.csv = _pd.DataFrame()
            self.errors = self.csv.values

    def is_failed(self, company, sheet):
        name = '{}_{}'.format(company, sheet)
        flag_failed = name in self.errors
        flag_empty_csv = len(self.csv) != 0
        return flag_failed and flag_empty_csv

    def save_failed(self, company, sheet, exception):
        name = '{}_{}'.format(company, sheet)
        # df = _pd.concat((self.csv, _pd.DataFrame([[name, exception]])), ignore_index=True)
        df = _pd.DataFrame([[name, exception]])
        df.columns = ['Error', 'Info']

        df.to_csv(self.path, header=False, mode='a')
