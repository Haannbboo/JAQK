from pyquery import PyQuery as pq
import pandas as pd


def get_summary(html, stock):
    doc = pq(html)
    tables = doc('#quote-summary table').items()
    t = [i.text().split('\n') for i in tables]
    t = [i[j] for i in t for j in range(len(i))]
    columns = [t[i] for i in range(0, len(t), 2)]
    data = [[t[i] for i in range(1, len(t), 2)]]
    data[0].insert(0, stock)
    columns.insert(0, 'Stock')
    del t
    df = pd.DataFrame(data)
    df.columns = columns
    return df


def get_news(html):
    doc = pq(html)
    pass
