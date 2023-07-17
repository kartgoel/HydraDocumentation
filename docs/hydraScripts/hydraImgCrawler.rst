hydra_imgCrawler
=================

This file scans and processes image files, interacting with the MySQL database to query and update information related to the plots. 

ScanLocations 
----------------

This method scans and processes image files, iterating through locations and performing specific actions based on the location type ("Run" or "sim"). 
For each location, it retrieves the list of files and their information and inserts the file information into the database if it hasn't already been inserted.

.. code-block:: python 

    # Extended code available on Github
    def ScanLocations(locations):


Parameters 
~~~~~~~~~~~~~~~~~~~~

- ``locations``: A list containing the specific locations to scan for image files. 


Example Usage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    ScanLocations(root_loc, locations_to_scan)


