import pandas as _pd
from .Open import open_file
from ..operations.Trans import _translate


class get_sheet(object):

    def __init__(self, companies, sheets, **kwargs):
        self.company = companies
        self.sheet = sheets

        self._reformat_sheet(kwargs)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, name):
        return self.__dict__.get(name, None)

    def _reformat_sheet(self, kwargs):
        if isinstance(self.company, str):
            self.company = [self.company]
        if isinstance(self.sheet, str):
            self.sheet = [self.sheet]

        for c in self.company:
            dfs_container = _sheet_container(c, self.sheet, **kwargs)
            self.__setitem__(c, dfs_container)


class _sheet_container(object):

    def __init__(self, c, sheet, **kwargs):
        self.c = c
        self.sheet = sheet
        self.start = kwargs.get('start', None)
        self.end = kwargs.get('end', None)
        self.mydict = {}

        self._collect_sheet()

    def _collect_sheet(self):
        for s in self.sheet:
            if s == 'stats':
                df = _pd.concat([open_file(self.c, s)
                                 for s in ['Valuation_Measures', 'Financial_Highlights', 'Trading_Information']],
                                ignore_index=True)
            else:
                df = open_file(self.c, name=s)
                if 'price' in s:
                    if self.start is not None:
                        df = df[df.Date >= self.start]
                    if self.end is not None:
                        df = df[df.Date <= self.end]
            self.mydict.update({s: df})

    def __getitem__(self, name):
        return self.mydict.get(name, None)


def get_desc(company, language='en'):
    """
    stock - a company's code (eg. AAPL)
    language - default English, choose your language (e.g zh for mandarin)
    returns the description of the company in yahoo finance
    """
    df = open_file(company, name='Description')
    desc = df['Description'][0]  # get description
    if language != 'en':
        desc = _translate(desc, language)  # translate
    return desc
