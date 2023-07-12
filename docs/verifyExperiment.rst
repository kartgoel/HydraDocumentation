Verifying Experiment
===================

This configures connections to the database and server based on the experiment. 

.. code-block:: php 

    $Exp=$_GET['Experiment'];
    $PT=$_GET['PT'];

    if($Exp=="GlueX")
    {
        $servername = "hallddb";
        $username = "aimon";
        $password = "";
        $dbname = "hydra";
    }
    else if($Exp=="SBS")
    {
        $servername = "epscidb";
        $username = "sbsuser";
        $password = "";
        $dbname = "SBS_Hydra";
    }
    else if($Exp=="CLAS")
    {
        $servername = "epscidb";
        $username = "clasuser";
        $password = "";
        $dbname = "CLAS_Hydra";
    }

Configurations
~~~~~~~~~~~~~~~~

- ``servername``: A string representing the server name. 
- ``username``: A string representing the username used to connect to the database. 
- ``password``: A string representing the password for the database user. 
- ``dbname``: A string representing the name of the database. 

Parameter 
~~~~~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to configure parameters for. 
