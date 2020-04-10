# jaqk.test()

Test key functionality of JAQK package. There are 15 tests in total, which takes around 2-3 seconds to finish.


#### These tests are:

Test name | what it does
--------- | ------------
**test_balance** | test balance statement figures calculations
**test_cash_flow** | test cash flow statement figures calculations
**test_income** | test income statement figures calculations
**test_stats** | test statistical figures
**test_key** | test the general figures calculations
**test_get_factors** | test the usage of factors getter [jaqk.get_factors]()
**test_rank** | test the calculation of ranking algorithms in [jaqk.percentile]()
**test_Folder** | test folder operations
**test_Format** | test formatting tools
**test_Open** | test content openers
**test_Path** | test path controller, including [jaqk.datapath()](../operations/jaqk.datapath.md)
**test_Save** | test content savers, including [jaqk.save()]()
**test_Tools** | test jaqk tools, including [jaqk.code_count()](), [jaqk.factors_names()](), etc.
**test_Trans** | test translation tools
**test_Get** | test sheet getter and sheet container, including [jaqk.get_sheet()]()


#### See also

[guidebook](guidebook.md) : what you can do with JAQK package.

[jaqk.main](../data-collection/jaqk.main.md) : stock data crawler (probably your next step).


#### Examples

```python
>>> import jaqk
>>> jaqk.test()
...............
----------------------------------------------------------------------
Ran 15 tests in 3.594s

OK
```

If you see `OK` in red, it means the JAQK package functions normally. If you see any `Errors` or `Failures`, 
please post a message on **[Issues](https://github.com/Haannbboo/JAQK/issues/new)** in GitHub.

----

###### Back to [index page](../index.md)