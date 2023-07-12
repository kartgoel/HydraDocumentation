hydra_cleaner
==============

This file cleans the queue for runtime by deleting rows in the RunTime table which have a timestamp of more than 1 hour ago.

.. code-block:: python

   def main(argv):
    #wake up and clean
    clean_q="DELETE from RunTime where DateTime < now() - interval 1 HOUR;"
    dbcursor.execute(clean_q)
    dbcnx.commit()

    if __name__ == "__main__":
        main(sys.argv[1:])

