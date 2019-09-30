from pyquery import PyQuery as pq
import re
import pandas as pd


# Analysis
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


# Financial
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


# Holders
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
    df1, df2 = pd.DataFrame(t2[0]), pd.DataFrame(t2[1])  # convert to pd DataFrame
    df1.columns = columns[0]
    df2.columns = columns[1]
    return df1, df2


# Profile
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


# Summary
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


# Update page
def get_update(html):
    try:
        updates = [i.text() for i in pq(html)('.simpTblRow a').items()]
        df = pd.DataFrame(updates)
        df.to_csv('dates_temp.csv', mode='a', header=False)  # csv of firms
    except TypeError:
        pass
