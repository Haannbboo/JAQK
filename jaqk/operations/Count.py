import os as _os
import gc as _gc

p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
global datapath
datapath = _os.path.join(p, 'database')


def database_count():
    a=len(_os.listdir(datapath))-2
    b=_os.walk(datapath) # generator
    c=[1]
    c=len([c[0]+1 for root, dirs, files in b for name in files])-12
    print("Total number of companies contained: {}".format(a))
    print("Total number of detailed sheets: {}".format(c))
    _gc.collect()
