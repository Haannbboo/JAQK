# Installation

JAQK is a Python package, and you need to install it before using it.

## Usual pip install?

JAQK is available through the usual pip install. Simply go to Command-Line or Terminal and type in:
```
pip install jaqk
```
This downloads not only the JAQK package but also all dependencies. After this, go to your favourite Python IDE, and try to import it:
```python
import jaqk
```
If this doesn't give any exceptions, installation is successful. Now you need to do the setup work before accessing key functionalities.

## Prefer setup.py?

Alternatively, you can use setup.py to install JAQK. 
1. Download JAQK from Github by clicking the green **Clone or download** button -> **Download Zip** -> 
2. Open cmd or terminal
3. Go to the folder in step 1 and run setup.py
	```
	cd PATH_OF_JAQK_FROM_STEP_1
	python setup.py
	```
4. Wait for the process to finish.
5. Go to a Python IDE and try to import.
6. If an error like "numpy is not defined" occur, that means one of the dependencies is not installed. Try to install the dependency by:
	```
	pip install A_DEPENDENCY_NOT_INSTALLED
	```

## Can't install?

Don't panic. This happens everyday, and it can be easily fixed. **Just follow the steps below.**
1. Make sure the exception in Python IDE is an **import error**.
2. Go to cmd or terminal again:
	```
	pip show jaqk
	```
	Find the information about **Location**, which is the current path of JAQK. Copy the path.
3. Now go to **Finder** (for Mac users) or **Documents** (for Windows users). 
	- Mac: press **Shift+Command+G**, paste the path from step 2, press **return**.
	- Windows: directly past the path from step 2.
	Find the folder, copy the entire folder.
4. In the same Python IDE, find the *site-packages directory** by entering:
	```python
	import sys
	print(sys.path)
	```
	Normally this will give a list that contains lots of paths. Now look from back to front, **find the 1st path that ends with ".../site-packages/"**. Copy this path.
5. Same as step 3, go to the path copied in step 4. Paste the folder in step 3 to the path.
6. Now try to import in Python.
