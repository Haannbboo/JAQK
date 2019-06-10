from pyquery import PyQuery as pq
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

import asyncio
import aiohttp

def getter(url, timeout=10, error=True):
    # main get function for all the website getter
    # it would support proxies, multiple user agent
    # it should raise errors when failure
    # Potential problems
    proxies=None
    UA = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 \
        Safari/537.36']
    headers = {
        'User-Agent': UA[0]  # Select user agent
    }
    try:
        html = requests.get(url,timeout=timeout).text
        error=False
    except Exception as e:
        print("Exception: ",e)
        error=True
    time.sleep(0.27)
    if error==False:
        return html
    else:
        getter(url,timeout,error)

def parse_kuai(html):
    doc=pq(html)
    a=doc('#content table').text().split('\n')[7:]
    a=[a[i:i+7] for i in range(0,len(a),7)]
    for b in a:
        b.insert(0,b.pop(0)+':'+b.pop(0))
        b[4]=float(b[4][:-1])
    df=pd.DataFrame(a)
    try:
        df.columns=['IP','Secret','Type','Location','Speed','Time']
    except ValueError:
        print("ValueError")
    return df

def parse_xici(html):
    doc=pq(html)
    a=doc('#ip_list tr').items()
    b=[i.text().split('\n') for i in a][1:]
    for i in b:
        i.insert(0,i.pop(0)+':'+i.pop(0))
    c=[[j[0]]+j[-4:] for j in b]
    assert (len(c)==len(b))
    temp={1:'b[i][1:-4]',0:'[None]'}
    c=[c[i]+eval(temp[len(b[i][1:-4])]) for i in range(len(c))]
    df=pd.DataFrame(c)
    df.columns=['IP','Secret','Type','Survive','Time','Location']
    return df
    
def parse_89(html):
    doc=pq(html)
    a=doc('table tbody tr').items()
    b=[i.text().split('\n') for i in a]
    for i in b:
        i.insert(0,i.pop(0)+':'+i.pop(0))
    df=pd.DataFrame(b)
    df.columns=['IP','Location','Network','Time']
    return df

def parse_66(urls): # This has different format than other parsers
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    w=webdriver.Chrome(chrome_options=chrome_options)
    try:
        dfs=[]
        for url in urls:    
            w.get(url)
            a=w.find_element_by_css_selector('#main table').text.split('\n')[1:]
            a=[i.split(' ')[:-1] for i in a]
            for i in a:
                i.insert(0,i.pop(0)+':'+i.pop(0))
            df=pd.DataFrame(a)
            df.columns=['IP','Location','Secret','Time']
            # Could be stored seperately
            dfs.append(df)
    except Exception as e:
        print("Exception: ",e)
    finally:
        w.quit()
    return pd.concat(dfs)

def parse_ihuan(url):
    # Not usable
    # Anti spydered
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    w=webdriver.Chrome(chrome_options=chrome_options)
    w.get(url)
    number=w.find_element_by_css_selector(".panel-body.form-horizontal form input[name='num']")
    number.clear()
    number.send_keys('3000')
    Type=Type=w.find_element_by_css_selector(".panel-body.form-horizontal form div select[name='anonymity'] option[value='2'")
    Type.click()
    s=w.find_element_by_css_selector(".panel-body.form-horizontal form div select[name='sort'] option[value='1']")
    s.click()
    
def parse_qy(html):
    doc=pq(html)
    a=doc('.container table tbody tr').items()
    b=[i.text().split('\n') for i in a]
    for i in b:
        i.insert(0,i.pop(0)+':'+i.pop(0))
    df=pd.DataFrame(b)
    df.columns=['IP','Secret','Type','Location','Speed','Time']
    return df

def parse_3366(html): # yun daili
    doc=pq(html)
    a=doc('#container #list table tbody tr').items()
    b=[i.text().split('\n') for i in a]
    for i in b:
        i.insert(0,i.pop(0)+':'+i.pop(0))
        i[1]='高匿代理IP'
        i.pop(3)
        i[3]=float(i[3][:-2])
    df=pd.DataFrame(b)
    df.columns=['IP','Secret','Type','Speed','Time']
    return df
    
def save(df,name):
    p='/Users/hanbo/Desktop/ML/QA/JAQK/Database/proxies/'+name+'.csv'
    try:
        df0=pd.read_csv(p)
    except FileNotFoundError:
        df0=pd.DataFrame() # possibly error
    df1=pd.concat([df,df0],ignore_index=True,sort=False).drop_duplicates(subset='IP',keep='first')
    #df2=df1.sort_values('Time',ascending=False)
    df1.to_csv(p,index=False)

def main0():
    urls=[
        'https://www.kuaidaili.com/free/inha/1/', #done
        'https://www.xicidaili.com/nn/1', #done
        'http://ip.zdaye.com/dayProxy/2019/4/1.html', # Selenium &architecture
        'http://www.89ip.cn/', #done
        'http://www.feiyiproxy.com/', # No histrocial data, needs refreshing
        'http://www.66ip.cn/1.html', #done
        'https://ip.ihuan.me/ti.html', # not usable
        'http://www.qydaili.com/free/?action=china&page=1', #done #friend link from 89ip
        'http://www.ip3366.net/free/?stype=1&page=1', # friend link of 89ip
        ]


def save_kuai():
    urls='https://www.kuaidaili.com/free/inha/'
    try:
        for i in range(1,2805):
            html= getter(urls+str(i)+'/')
            save(parse_kuai(html),'kuai')
            print("Saved "+str(i))
            #input("Press enter to continue")
    except Exception as e:
        print("Exception in main saver: ",e)
    finally:
        p='/Users/hanbo/Desktop/ML/QA/JAQK/Database/proxies/'+'kuai'+'.csv'
        df0=pd.read_csv(p)
        df1=df0.sort_values('Time',ascending=False)
        df1.to_csv(p,index=False)

def save_xici():
    url='https://www.xicidaili.com/nn/', #done
    # url+str(i)
    try:
        for i in range(1,3648):
            html=getter(url+str(i))
            save(parse_xici(html),'xici')
            print("Saved "+str(i))
    except Exception as e:
        print("Exception in main saver: ",e)
    finally:
        p='/Users/hanbo/Desktop/ML/QA/JAQK/Database/proxies/'+'xici'+'.csv'
        df0=pd.read_csv(p)
        df1=df0.sort_values('Time',ascending=False)
        df1.to_csv(p,index=False)
    
    
def main():
    '''
    for i in range(0,32,32):
        tasks=[asyncio.ensure_future(save_kuai(ii)) for ii in range(i,i+32)]
        loop=asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
    '''
    pass
    
