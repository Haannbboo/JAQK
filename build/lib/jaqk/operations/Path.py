import pandas as _pd
import os as _os


def datapath(database=True, *sheet_param):  # database
    """
    The global datapath for all other file. It sets your selected path in jaqk.setup() as the main datapath,
    and all data will be added/deleted from there.
    """
    main_path = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
    sheet_param = ['"{}"'.format(i) for i in sheet_param]
    if database is True:
        try:
            with open(_os.path.join(main_path, 'setup_cache.txt')) as w:
                database_path = w.read()
        except FileNotFoundError:
            database_path = _os.path.join(main_path, 'database')
        return eval('_os.path.join(database_path, {})'.format(', '.join(sheet_param)))  # jaqk/folder

    elif database is False:
        return eval('_os.path.join(main_path, {})'.format(', '.join(sheet_param)))


def path(factor):
    """
    factor - str - factor name (use names() to find out all factor names included)
    returns the file name of the factor (e.g path('Total Assets') gives 'balance')
    """
    # can be a loop or sommething
    # Still in abs path, need changes
    # p = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir))
    # path = _os.path.join(p, 'database')
    if factor in ['price_daily', 'price_monthly', 'price_weekly']:
        return factor

    if factor == 'Summary':
        factors = list(_pd.read_csv(_os.path.join(datapath(), 'AAPL', 'AAPL_Summary.csv')))
        if factor in factors:
            return 'Summary'

    for name in ['balance', 'income', 'cash_flow', 'Trading_Information',
                 'Financial_Highlights', 'Valuation_Measures']:
        try:
            factors = _pd.read_csv(_os.path.join(datapath(), 'AAPL', 'AAPL_{}.csv'.format(name)))['Statements'].tolist()
        except KeyError:
            factors = _pd.read_csv(_os.path.join(datapath(), 'AAPL', 'AAPL_{}.csv'.format(name)))['0'].tolist()

        if factor in factors:
            return name

    raise ValueError("Factor '{}' not in database, use jaqk.factors_names() to find all all factors' names".format
                     (factor))
