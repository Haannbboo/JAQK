import os

p = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
global datapath
datapath = os.path.join(p, 'database')


def create_folder(stock):
    path = os.path.join(datapath, stock)
    if os.path.isdir(path):  # If dir existed
        pass
    else:
        os.makedirs(path)  # Create directory


def exist(stock, file, update=False):
    p1 = os.path.join(datapath, stock, stock)
    # if it needs update，then view it as not existing
    # and the save_file func handles the duplication
    if update:
        return False

    if isinstance(file, str):
        path = p1 + '_' + file + '.csv'
        return os.path.exists(path)
    elif isinstance(file, list):
        paths = [p1 + '_' + f + '.csv' for f in file]
        r = '&'.join([str(os.path.exists(p)) for p in paths])
        return eval(r)
