#from getters.getter import getter
#from operations.Save import save_file
import json
from pyquery import PyQuery as pq
import requests
import pandas as pd
import time

import aiohttp
import asyncio

url='https://finance.yahoo.com'


def setproxy(p):
    proxies={
        'http' : 'http://'+p,
        'https' : 'https://'+p
        }
    return proxies

async def getter(url,proxies,timeout=10):
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    #s=time.time()
    try:
        async with aiohttp.ClientSession(headers=headers,connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            # Mistake here
            try:
                r = await session.get(url,proxy=proxies['http'],timeout=timeout)
                n = r.status
            except Exception:
                raise ValueError
            finally:
                await session.close()
            
            #e=time.time()
    except (aiohttp.client_exceptions.ClientProxyConnectionError, ValueError) as e:
        n=0
    if n==200:
        return True
    else:
        return False

'''
async def proxytest(ip):
    proxies=setproxy(ip)
    url='https://httpbin.org/get'
    r= await getter(url,proxies=proxies)
    return r
'''

async def test(ip):
    url='http://www.baidu.com'
    if not isinstance(ip,str):
        return
    proxies=setproxy(ip)
    s=time.time()
    r= await getter(url,proxies=proxies)
    if r:
        e=time.time()
        #result.append([ip,str(e-s)])
        #print("Proxy working "+ip)
        result.append([ip,str(round(e-s,3))])
    #else:
#        print("Proxy failed "+ip)
        

def main(ips):
    global result
    result=[]
    url='https://www.baidu.com'
    #df=pd.read_csv('/Users/hanbo/Desktop/ML/QA/JAQK/database/proxies/kuai.csv')
    #ips=df['IP']
    tasks=[asyncio.ensure_future(test(ip)) for ip in ips for _ in range(5)]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    df=pd.DataFrame(result)
    df.columns=['IP','Speed']
    df=df.drop_duplicates('IP')
    return df


df=pd.read_csv('/Users/hanbo/Desktop/ML/QA/JAQK/database/proxies/kuai.csv')
ips=df['IP']
d=main(ips)
#main()
