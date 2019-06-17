from pyquery import PyQuery as pq
import pandas as pd


def get_analysis(html):
    doc = pq(html)
    tables = doc('#Main table').items()
    t = [i.text().split('\n') for i in tables]
    t_df = [[tt[i:i + 4] for i in range(0, len(tt), 5)] for tt in t]
    columns = [i.pop(0) for i in t_df]
    dfs = [pd.DataFrame(i) for i in t_df]
    for i in range(len(dfs)):
        dfs[i].columns = columns[i]
    return dfs
