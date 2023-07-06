schema_sync
===================

This file initiates schema sync through backing up the database. 
It retrieves the list of tables in each database and compares the schemas between databases A and B. 
It proceeds to synch schemas between the two databases if possible and establishes an auto increment if necessary. 