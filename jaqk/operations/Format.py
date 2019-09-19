import numpy as _np
import re


def _decimal(array):
    """Eliminate ',' in numbers, e.g. 10,000 to 10000

    Using numpy vectorization to map filter to the input array

    Args:
        array: list/np.ndarray - array that needs to be formated
    """
    d = _np.vectorize(lambda x: float(re.compile(',').sub('', x)))
    return d(array)


def _money_digits(array):  # map to all
    f = _np.vectorize(_is_wrong_digit)
    return f(array)


def _is_wrong_digit(digit):  # convert money digit into values
    t = {'B': 1000000000, 'M': 1000000, 'K': 1000, '%': 0.01}
    if isinstance(digit, str):
        last = digit[-1]  # last digit
        if last == '-':
            return '0.0'
        if last in ['B', 'M', 'K', '%']:
            new = str(eval(''.join(re.findall('[0-9]', digit))) * t[last])
            return new
        else:
            return digit


def year_convert(year, df):
    temp = lambda x, y: [i for j in x for i in y if str(j) in i]
    r = temp(year, list(df))
    return r


def factor(df, factor, year=True):
    # dimensions of f are different for 'factor' and ['factor']
    if len(df) > 5 and ('2018' not in ''.join(list(df))) and year != True:
        raise ValueError("Parameter year can only be used when factor is in non-financial sheets")
    # factor-str is probably just non-sense, because get_factors() already converts str->list
    if isinstance(factor, str):
        if year == True:  # all years
            f = _decimal(_money_digits(df[df.iloc[0:, 0].isin([factor])].values[0][1:]))
        elif year == 'NEWEST':
            f = _decimal(_money_digits(_np.array([d[1] for d in df[df.iloc[0:, 0].isin([factor])].values])))
        else:  # single factor with specified years
            years = year_convert(year, df)
            # problematic here
            f = _decimal(_money_digits(df.loc[df.Statements == factor, years].values))
    elif isinstance(factor, list):
        if year == True:
            f = _decimal(_money_digits(_np.array([d[1:] for d in df[df.iloc[0:, 0].isin(factor)].values])))
        elif year == 'NEWEST':  # multiple factors with the newest year
            f = _decimal(_money_digits(_np.array([[d[1] for d in df[df.iloc[0:, 0].isin(factor)].values]])))
        else:
            years = year_convert(year, df)
            # problematic here
            f = _decimal(_money_digits([df.loc[df.Statements == fac, years].values[0] for fac in factor]))
    return f
