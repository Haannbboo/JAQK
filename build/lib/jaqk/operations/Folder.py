import os as _os

p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
global datapath
datapath = _os.path.join(p, 'database')


def create_folder(stock):
    path = _os.path.join(datapath, stock)
    if _os.path.isdir(path):  # If dir existed
        pass
    else:
        _os.makedirs(path)  # Create directory


def exist(stock, file, update=False):
    p1 = _os.path.join(datapath, stock, stock)
    # if it needs update，then view it as not existing
    # and the save_file func handles the duplication
    if update:
        return False

    if isinstance(file, str):
        path = p1 + '_' + file + '.csv'
        return _os.path.exists(path)
    elif isinstance(file, list):
        paths = [p1 + '_' + f + '.csv' for f in file]
        r = '&'.join([str(_os.path.exists(p)) for p in paths])
        return eval(r)
