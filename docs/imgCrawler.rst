imgCrawler
=================

This file scans and processes image files, interacting with the MySQL database to query and update information related to the plots. 


----------------------------------------------

ScanLocations 
----------------

This method scans and processes image files, iterating through locations and performing specific actions based on the location type ("Run" or "sim"). 
For each location, it retrieves the list of files and their inofrmation and inserts the file information int othe database if it hasn't already been inserted.

.. code-block:: python 

    def ScanLocations(root_loc, locations):


Parameters 
~~~~~~~~~~~~~~~~~~~~

- ``root_loc``: A string representing the location where the image files are stored. 
- ``locations``: A list that contains the specific locations to scan for image files. 


Example Usage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    ScanLocations(root_loc, locations_to_scan)


