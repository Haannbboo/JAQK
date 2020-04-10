# jaqk.update()


Update the database by:
1. Collect stock names that have been updated since the last update
2. Crawl stock data for the companies in step 1 (only those originally in database would be updated)
3. Concatenate new data to the old data in database.

It's strongly recommended to use [jaqk.test()](../installation/jaqk.test.md) after update.
This makes sure the `update()` function works as usual.


#### See also

[jaqk.main()](jaqk.main.md) : stock data crawler.

[jaqk.test()](../installation/jaqk.test.md) : test key functionality of the module.


#### Example

```python
>>> import jaqk
>>> jaqk.update()
```
This will take a well because there are intensive internet requests needed.
The ETA depends on the days that you need to check for update. 

If you see any exceptions or errors, please post a message on **[Issues](https://github.com/Haannbboo/JAQK/issues/new)** in GitHub.


###### Back to [index page](../index.md)
