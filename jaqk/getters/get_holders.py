import pandas as pd
from pyquery import PyQuery as pq


def get_major_holders(html):
    """Getter for holders from yahoo finance"""
    doc = pq(html)
    tables = doc('#mrt-node-Col1-1-Holders table')  # parsing rule
    t1 = pq(tables.pop(0)).text().split('\n')
    t2 = [[t1[i + 1], t1[i]] for i in range(0, len(t1), 2)]  # formatting
    df = pd.DataFrame(t2)  # convert to pd dataframe
    df.columns = ['Category', 'Percentage']
    return df


def get_top_institutional_and_mutual_fund_holders(html):
    """Getter for other holders in yahoo finance"""
    doc = pq(html)
    tables = doc('#mrt-node-Col1-1-Holders table')  # parsing rule
    # formatting
    t = [pq(i).text().split('\n') for i in tables[1:]]
    t2 = [[t1[i:i + 4] for i in range(0, len(t1), 5)] for t1 in t]
    columns = [t.pop(0) for t in t2]
    df1, df2 = pd.DataFrame(t2[0]), pd.DataFrame(t2[1])  # convert to pd dataframe
    df1.columns = columns[0]
    df2.columns = columns[1]
    return (df1, df2)
