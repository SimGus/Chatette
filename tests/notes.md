# Description of the module
This module contains the tests for the `chatette` package (located in `../chatette`). All tests are intended to be executed using `pytest`.

Note that as the package is supposed to work for both *Python 2.7* and *Python 3.x*, you should run tests for using both `python2 -m pytest` and `python3 -m pytest`.

`unit-testing` contains the unit tests for all the modules in `chatette`; `system-testing` contains the system test (for `chatette` taken as a black-box).

# Problems with `pytest`?
If you get an `ImportError` (no module named `chatette.<anything>`), you should install the package as editable. To do this, go to the directory `..` (containing `setup.py`) and run `pip install --editable .`. The package will change when you change the code in `chatette`.

