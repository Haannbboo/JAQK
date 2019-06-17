import pandas as pd
from pyquery import PyQuery as pq


def get_executives(html):
    doc = pq(html)
    text = doc('#Main table').text().split('\n')
    t = [text[i:i + 5] for i in range(0, len(text), 5)]
    columns = t.pop(0)
    df = pd.DataFrame(t)
    df.columns = columns
    return df


def get_description(html):
    doc = pq(html)
    text = doc('.quote-sub-section p').text()
    df = pd.DataFrame([text])
    df.columns = ['Description']
    return df
