# jaqk.main()


jaqk.main(stocks='SP100', sheets='financials', batch: integer = 32, update: bool = False, exception: bool = False, error_cache: bool = False)

**Stock data crawler**. Targeting Yahoo Finance, using asynchronous requests. Automatically save to database.


**NOTE: THIS TAKES A WHILE.** Each site is approx 700KB, each company is around 8 site --> each company takes 5 MB. 
There are over 6000 companies in total, so around 30 GB of traffic.


### **Parameters:**
- **stocks** **:** **{'NYSE', 'NASDAQ', 'SP100', Iterable}, default 'SP100'**
    - **NYSE** **:** all companies in New York Stock Exchange
    - **NASDAQ** **:** all companies in NADAQ index
    - **Iterable** **:** stocks you want to get. *e.g ['AAPL', 'AMZN', 'BABA']*.
   
- **sheets** **:** **{'financials', 'key-statistics', 'summary', 'profile', 'analysis', 'holders', 'ALL'}, default 'financials'**
    - **financials** **:** financial report of the company, including income statement, balance statement, and cash-flow statement. *Recommended to use financials*
    - **key-statistics** **:** statistical record of the company, including Valuation Measures, Financial Highlights, and Trading Information
    - **summary** **:** a summary to the company's information
    - **profile** **:** information about key executives and a description of the company
    - **analysis** **:** institutions' analysis summary, such as earnings estimate, revenue estimate, etc.
    - **holders** **:** shareholders' information, including major holders, institutional holders, and mutual fund holders
    - **ALL** **:** collect **ALL INFORMATION** about the company.
   
 - **batch** **:** **integer, default 32**
    
    Number of companies collected at a time. *Recommend to set to 32*. The poorer the internet ability the lower the batch size.

- **update** **:** **bool, default False**

    Update the database when **`update=True`** (concatenate new data to the sheet in database),
    collect new data from Yahoo Finance when **`update=False`**.
    
- **exception** **:** **bool, default False**
    
    Print exception messages when **`exception=True`**.

- **error_cache** **:** **bool, default False**

    When **`error_cache=True`**, save errors in crawler in a file, and won't collect these companies the next time using crawler.
    
    
#### See also: 
[jaqk.update()](./jaqk.update.md) : update the database.

[jaqk.setup()](../installation/jaqk.setup.md) : setup the database. Need to be done before using jaqk.main()

[jaqk.test()](../installation/jaqk.test.md) : test key functionality of the module.


#### Examples
Collect financial sheets of S&P100 companies: 
```python
>>> import jaqk
>>> jaqk.main()  
```
This takes around 300 web-pages with **ETA 60 seconds** (depending on your internet).

----

Collect all sheets of S&P100 companies: **ETA 120 seconds.**
```python
>>> import jaqk
>>> jaqk.main(sheets='ALL')
```

----

Collect financial sheets of all companies, with batch size of 16 and using error cache file: **ETA 3600 seconds.**
```python
>>> import jaqk
>>> jaqk.main('ALL', batch=16, error_cache=True)
```
Note that this creates an error file at *.../jaqk/Spyder/error_cache*

----

###### Back to [index page](../index.md)