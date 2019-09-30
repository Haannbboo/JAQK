import os as _os
import gc as _gc
import pandas as _pd
from .operations.Folder import create_folder
from .operations.Open import open_general, open_file
from .operations.Path import datapath


def setup():
    """
    setup the database; this should be done before anything;
    choose the directory to place the database (~100M)
    """
    main_path = _os.path.abspath(_os.path.dirname(__file__))

    # choose a specific path for database folders
    import PySimpleGUI as sg
    form_rows = [[sg.Text('Choose the setup path')],
                 [sg.Text('Setup path: ', size=(15, 1)), sg.InputText(key='setup'), sg.FolderBrowse()],
                 [sg.Submit(), sg.Cancel()]]  # layout design
    window = sg.Window('Choose a path for setup database')
    _, values = window.Layout(form_rows).Read()  # callback
    window.Close()
    setup_path = values['setup']
    with open(_os.path.join(main_path, 'setup_cache.txt'), mode='w') as w:
        w.write(setup_path)  # setup cache file for setup directory

    # setup starts
    companies = ['AAPL', 'AMZN']
    [create_folder(i, setup_path, True) for i in companies]  # create new folders
    dirs = [_os.listdir(datapath(True, c)) for c in companies]
    dirs2 = dirs[:]
    del dirs
    try:
        [dirs2[i].remove('__init__.py') for i in range(2)]  # remove __init__.py
    except ValueError:
        pass
    if '.py' in ''.join(dirs2[0]) + ''.join(dirs2[1]):  # AAPL and AMZN
        # convert .py into .csv
        [open_file(companies[c], dirs2[c][d], setup=True).to_csv(
            _os.path.join(setup_path, companies[c], dirs2[c][d].split('.')[0] + '.csv'), index=False)
            for c in range(len(companies)) for d in range(len(dirs2[c]))
            if dirs2[c][d] != '__init__.py' and dirs2[c][d] != '__pycache__']

        # delete original .py files
        [_os.remove(datapath(True, companies[i], dirs2[i][j]))
         for i in range(len(companies)) for j in range(len(dirs2[i]))
         if dirs2[i][j] != '__init__.py' and ('.csv' not in dirs2[i][j]) and dirs2[i][j] != '__pycache__']

    # setup general stock lists
    dirs_general2 = _os.listdir(datapath(True, 'general'))
    dirs_general = dirs_general2[:]  # avoid mutable list
    del dirs_general2
    try:
        dirs_general.remove('__init__.py')  # list_dir for 'general'
    except ValueError:
        pass

    if '.py' in ''.join(dirs_general):  # NYSE and NASDAQ
        # setup stock_list general
        exc = ['NYSE', 'NASDAQ', 'SP100']
        create_folder('general', setup_path, True)
        [open_general(ex, setup=True).to_csv(_os.path.join(setup_path, 'general', ex + '.csv'), index=False)
         for ex in exc]
        [_os.remove(datapath(True, 'general', ex + '.py')) for ex in exc]

    if 'dates_temp.py' in _os.listdir(_os.path.join(main_path, 'Spyder')):  # dates_temp
        _pd.read_csv(_os.path.join(main_path, 'Spyder', 'dates_temp.py')).to_csv(_os.path.join(main_path, 'dates_temp.csv'),
                                                                       index=False)
        _os.remove(_os.path.join(main_path, 'Spyder', 'dates_temp.py'))  # delete original\

    if 'datefile.py' in _os.listdir(_os.path.join(main_path, 'Spyder')):  # datefile
        with open(_os.path.join(main_path, 'Spyder', 'datefile.py')) as d:
            d = d.read()  # read
        with open(_os.path.join(main_path, 'Spyder', 'datefile.txt'), mode='w') as w:
            w.write(d)  # write
        _os.remove(_os.path.join(main_path, 'Spyder', 'datefile.py'))  # delete

    _gc.collect()
    print("Database has been setup on path: {}".format(setup_path))
