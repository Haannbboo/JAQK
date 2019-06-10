import sys as _sys
_sys.path.append('..') # add previous directory to model object

from operations.Format import factor as _factor

# These are quite important and popular factors, so I list them out
# so my client can use it like ROE-ROA, instead of factor(ROE)-factor(ROA), which is quite werid
def ROE(df): # Financial Highlights
    return _factor(df, 'Return on Equity (ttm)')

def ROA(df): # Financial Highlights
    return _factor(df, 'Return on Assests (ttm)')


def EBITDA(df): # Financial Highlights
    return _factor(df, 'EBITDA')
