Establish Database Connection
======================

This code segment attempts to establish a connection to the MySQL database.

.. code-block:: python

    try:
        dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
        dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("ERROR: CANNOT CONNECT TO DATABASE")
        exit(1)


- ``MySQLdb.connect()``: Establishes a connection to the MySQL database using the provided host, username, and database namme.
- ``MySQLdb.cursors.DictCursor``: Creates a cursor that returns query results. 
- An error message is printed and the program exits if the connection is unsuccessful. 