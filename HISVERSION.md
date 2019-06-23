## Historical Version for JAQK package

> Everything written are worth recording. They're stamps of growth, maturity, and development. Hope this will become part of memory...

#### 0.0.1 Frist update
- 12am, Jun.10th: Clone to Github
- 8pm, Jun.10th: Connect to PyPi
- 9am, Jun.12th: Update client function: save()
- 11am, Jun.12th: Update get.py to eliminate bug in core spyder, reduce default batch size to 32
- 12am, Jun.12th: Format all python files for pypi imports
- 1pm, Jun.12th: Add "help" to all client functions
#### 0.0.2 Jun.12th 2019
- 7pm, Jun.12th: Add client function: factors_name(), sheets_name()
- 9pm, Jun.12th: Add client function: code_count()
##### 0.0.2.1 Jun.13th 2019
- 8am, Jun.13th: Update to reduce bug for PyPi import
- 4pm, Jun.15th: Add client function: test() (test includes operations, basics, calculations, factors, stock)
##### 0.0.2.2 Jun.17th 2019
- 2pm, Jun.17th: Update client function: test() (resolve all Failures and Exceptions in unittests)
###### 0.0.2.2.1 Jun.17th 2019
- 2pm, Jun.17th: Add client function: database_clear()
- 9pm, Jun.17th: Add client function: load_stock_list()
###### 0.0.2.2.2 Jun.17th 2019
- 11pm, Jun.17th: Update to PyPI for client testing (using IDLE)
###### 0.0.2.2.3 Jun.18th 2019
- 3pm, Jun.18th: Resolve database PyPI installation problem; add client function: setup()
###### 0.0.2.2.4 Jun.18th 2019
- 5pm, Jun.18th: Update test(), setup(), create_folder(); debug for setup() and test()
###### 0.0.2.2.5 Jun.19th 2019
- 9am, Jun.19th: Add parameter "sheets" to main_get(), enables downloading parts of data
- 10am, Jun.19th: Add 'xlrd>=1.0.0' to setup
##### 0.0.2.3 Jun.23th 2019
- 4pm, Jun. 19th: Change main_get() default to S&P100; add client function jaqk.rank.best() and jaqk.rank.worst(); big structual change in jaqk.rank
