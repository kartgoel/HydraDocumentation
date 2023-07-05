ConnectToDB
===================

This file includes the ``DBManager`` class, which provides functionality to establish a connection with the MySQL database, execute queries, and perform database operations. 


Initialization
----------------------------

The ``__inut__`` method initializes the ``DBManager`` object and establishes a connection to the MySQL database. 

.. code-block:: python

    def __init__(self, configPath="../Hydra.cfg"):


Parameter
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``configPath``: An optional string representing the path to the configurations file. This contains the necessary database connection details. 


-----------------------------------------------------

FetchAll
------------------

This method executes the specified MySQL query and returns the results obtained from the query. 

.. code-block:: python 

     def FetchAll(self, query):


Parameter
~~~~~~~~~~~~~~~~~

- ``query``: A string representing the MySQL query to be executed. 


Example Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    Plots_list= dbcursor.fetchall()


--------------------------------------------------------

Update
------------------

This method 

.. code-block:: python

    def Update(self, query):


Parameter
~~~~~~~~~~~~~~~~~~~~~

- ``query``: A string representing the MySQL query to be executed. 


Example Usage       
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

     DBConnector.Update(RunHistory_q)
