import os as _os

global p
p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
# global datapath
# datapath = _os.path.join(p, 'database')

def datapath(setup=True):
    try:
        with open(_os.path.join(p, 'setup_cache.txt')) as w:
            path = w.read()
        if setup==True:
            return path
        else:
            return _os.path.join(p, 'database')
    except FileNotFoundError:
        return _os.path.join(p, 'database')



def create_folder(stock, path='default', setup=False):
    if path == 'default':
        ppath = _os.path.join(datapath(), stock) # jaqk/database/AAPL
    else:
        if setup == True:
            ppath = _os.path.join(path, stock) # setup_path/AAPL
        elif setup == False:
            ppath = _os.path.join(p, path, stock) # jaqk/path/AAPL
    if _os.path.isdir(ppath):  # If dir existed
        pass
    else:
        _os.makedirs(ppath)  # Create directory


def exist(stock, file, update=False):
    p1 = _os.path.join(datapath(), stock, stock)
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
