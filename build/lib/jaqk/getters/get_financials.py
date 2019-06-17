from pyquery import PyQuery as pq
import re
import pandas as pd


def get_stats(html):
    # parser for statistics in yahoo finance
    doc = pq(html)
    tables = doc('#YDC-Col1 table').items()  # parsing rule
    # formatting to the clean format
    t = [i.text().split('\n') for i in tables]
    t = [t[0]] + [[i[j] for i in t[1:6] for j in range(len(i))]] + [[i[j] for i in t[7:9] for j in range(len(i))]]
    assert (len(t) == 3)
    t = [[i[j:j + 2] for j in range(0, len(i), 2)] for i in t]
    for i in t:  # formatting
        for j in i:
            j[0] = re.compile(' [0-9]$').sub('', j[0])
    assert (len(t) == 3)
    dfs = [pd.DataFrame(i) for i in t]
    return dfs


def get_statements(html):
    # Not done yet, needs to format and pd
    doc = pq(html)
    items = doc('#mrt-node-Col1-1-Financials table tr').items()  # Parser, will be seperated
    result = [i.text().split('\n') for i in items if len(i.text().split('\n')) > 1]
    df = pd.DataFrame(result)
    return df


def get_reports(html):  # parser for income, cash_flow, and balance sheets
    doc = pq(html)
    items = doc('#mrt-node-Col1-1-Financials table tr').items()  # Parsing rule
    result = [i.text().split('\n') for i in items if len(i.text().split('\n')) > 1]  # formatting
    columns = result.pop(0)
    columns[0] = 'Statements'  # eliminate unnecessary info
    df = pd.DataFrame(result)
    df.columns = columns
    return df
