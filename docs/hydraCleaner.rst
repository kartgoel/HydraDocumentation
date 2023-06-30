hydra_cleaner
==============

This file cleans the queue for runtime. 

.. code-block:: python

   def main(argv):
    #wake up and clean
    clean_q="DELETE from RunTime where DateTime < now() - interval 1 HOUR;"
    dbcursor.execute(clean_q)
    dbcnx.commit()
-----------------------
