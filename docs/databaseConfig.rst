Database Configurations
========================

This configuration connects to the MySQL database.

.. code-block:: python 

    dbhost = "hallddb.jlab.org"
    dbuser = 'aimon'
    dbpass = ''
    dbname = 'hydra'
    dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
    dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)


- ''dbhost'': The host address (in this case of the MySQL database).
- ''dbuser'': The username used to connect to the database.
- ''dbpass'': The password for the database user.
- ''dbname'': The name of the database to connect to.