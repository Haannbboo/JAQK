# jaqk.datapath()

jaqk.datapath(database: bool = True, *sheet_param: string, **kwargs)

Path controller for JAQK. It gives correct **absolute path** within JAQK directory.


### Parameters:

- **database** **:** **bool, default True**
    
    Returns the path of database when **`database=True`**. 
    **`database=False`** to indicate the path of a file or folder outside database (within JAQK).
   
- **sheet_param** **:** **set of strings, default None**
    
    Indicate the path you want within JAQK or within your database.
    It follows `os.path.join(database, sheet_param1, sheet_param2, ...)`
    or `os.path.join(jaqk, sheet_param1, sheet_param2, ...)`.
 
- **kwargs** **:** **default None**
    
    - **setup** **:** **bool ,default False**
        
        Direct datapath() to the database directory within JAQK folder when **`setup=True`**.
        Direct datapath() to other JAQK files or to your pre-set database path by **`setup=False`**.


#### See also

[jaqk.test()](../installation/jaqk.test.md) : test key functionality of the module.

[jaqk.save()](./jaqk.save.md) : save a stock data sheet to any place. 

[jaqk.get_factor()](./jaqk.get_factor.md) : collect data of factors of companies from database.


#### Example

Path of database:
```python
>>> import jaqk
>>> database_path = jaqk.datapath()
>>> print(database_path)

../database/
```

Path of a company's sheet: 
```python
>>> import jaqk
>>> path = jaqk.datapath(True, 'AAPL', 'AAPL_income.csv')
>>> print(path)

../database/AAPL/AAPL_income.csv
```

Path of a file within JAQK:
```python
>>> import jaqk
>>> path = jaqk.datapath(False, 'Spyder', 'error_cache.txt')

../JAQK/Spyder/error_cache.txt
```

----

###### Back to [index page](../index.md)