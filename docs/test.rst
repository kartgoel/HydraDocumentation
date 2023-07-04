Model analysis
=====================

Dependencies
---------------

The following dependencies are required to run this code segment:

numpy (imported as np)
MySQLdb
random

Make sure these dependencies are installed and accessible before running the code.

Database Connection Configuration
-------------------------------

Before using the functions, the database connection configuration needs to be set. Modify the following variables to match your MySQL database credentials and host information

.. code-block:: python
    dbhost = "hallddb.jlab.org"
    dbuser = 'aimon'
    dbpass = ''
    dbname = 'hydra'
------------

Function 1
--------------------

Parameters
~~~~~~~~~~~~~~~

- runPeriodSubstring (string): A substring used to filter the run periods in the database. Only run periods that contain this substring will be considered.
- Trainingfraction (float): The fraction of data to be used for training. The remaining fraction will be used for testing.

Usage
~~~~~~~~~~

1. Call the function RandomTrainingTestingSplit with the desired parameters.
2. The function will randomly split the data into training and testing sets based on the provided run period substring and training fraction.
3. The function will update the TrainingWeight column in the MySQL database accordingly.
4. The function does not return any value.


