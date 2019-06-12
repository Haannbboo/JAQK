import numpy as _np
import re


def _decimal(array):  # eliminate ',' in numbers
    d = _np.vectorize(lambda x: float(re.compile(',').sub('', x)))
    return d(array)


def money_digits(array): # not done, probably not useful
    digits = [i[-1] for i in array]
    d = '|'.join([str(i in ['B', 'M', 'K']) for i in digits])
    t = {'B': 1000000000, 'M': 1000000, 'K': 1000}
    if eval(d):
        for i in range(len(array)):
            array[i] = array[i] * t[array[i][-1]]
            pass


def factor(df, factor, year=True):
    # dimensions of f are different for 'factor' and ['factor']
    if isinstance(factor, str):
        if year == True:  # all years
            f = _decimal(df[df['Statements'].isin([factor])].values[0][1:])
        else:  # single factor with specified years
            temp = lambda x, y: [i for j in x for i in y if str(j) in i]  # map 2016 to '9/26/2016'
            years = temp(year, list(df))
            f = _decimal(df.loc[df.Statements == factor, years])
    elif isinstance(factor, list):

        if year == True:
            f = _decimal(_np.array([d[1:] for d in df[df['Statements'].isin(factor)].values]))
        elif year == 'NEWEST':  # multiple factors with the newest year
            f = _decimal(_np.array([[d[1] for d in df[df['Statements'].isin(factor)].values]]))
        else:
            temp = lambda x, y: [i for j in x for i in y if str(j) in i]
            years = temp(year, list(df))
            f = _decimal([df.loc[df.Statements == fac, years].values for fac in factor])
        # big bug here, not handling specific year list, eg. [2018, 2017]
    return f
