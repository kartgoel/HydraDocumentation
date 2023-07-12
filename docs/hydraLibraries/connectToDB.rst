ConnectToDB
===================

This file includes the ``DBManager`` class, which provides functionality to establish a connection with the MySQL database, execute queries, and perform database operations. 


Initialization
----------------------------

The ``__init__`` method initializes the ``DBManager`` object and establishes a connection to the MySQL database. 

.. code-block:: python

    def __init__(self, configPath="../Hydra.cfg"):



Parameter
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``configPath``: An optional string representing the path to the configurations file. This contains the necessary database connection details. 

--------------------

FetchAll
------------------

This method executes the specified MySQL query and returns the results obtained from the query. 

.. code-block:: python 

     def FetchAll(self, query):
        try:
            self.dbcursor.execute(query)
            results = self.dbcursor.fetchall()
        except Exception as e:
            print("DB Error: ", e)
            print("with query: ", query)
            logging.error("DB error with query: "+str(query))
            logging.error(e)
            print("Trying to reconnect...")
            self.dbcnx.ping(True)
            if self.dbcnx.open:
                try:
                    self.dbcursor=self.dbcnx.cursor(MySQLdb.cursors.DictCursor)
                    self.dbcursor.execute(query)
                    results = self.dbcursor.fetchall()
                    return results
                except Exception as e:
                    print("DB error after re-establishing connection:", e)
                    print("with query: ", query)
                    logging.error("DB error with query: "+str(query))
                    logging.error(e)
            else:
                print("ping failed to connect")
            return []
            
        return results


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

This method executes MySQL queries if possible and updates the databse accordingly.
Errors are pinged and logged through the execution.

.. code-block:: python

    def Update(self, query):
        try:
            self.dbcursor.execute(query)
            self.dbcnx.commit()
        except:
            print("DB error with query: ", query)
            logging.error("DB error with query: "+str(query))
            print("Trying to reconnect...")
            self.dbcnx.ping(True)
            if self.dbcnx.open:
                try:
                    self.dbcursor=self.dbcnx.cursor(MySQLdb.cursors.DictCursor)
                    self.dbcursor.execute(query)
                    self.dbcnx.commit()
                except Exception as e:
                    print("DB error after re-establishing connection:", e)
                    print("with query: ", query)
                    logging.error("DB error with query: "+str(query))
                    logging.error(e)
            else:
                print("ping failed to connect")


Parameter
~~~~~~~~~~~~~~~~~~~~~

- ``query``: A string representing the MySQL query to be executed. 


Example Usage       
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

     DBConnector.Update(RunHistory_q)

------------------

Close
------------------

This method closes the cursor and connection to the database.

.. code-block:: python

    def Close(self):
        print("closing cursor")
        self.dbcursor.close()
        print("closing connection")
        self.dbcnx.close()
        print("closed"
