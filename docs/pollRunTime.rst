.. _pollRunTimephp:

pollRunTime
======================

This php file selects plots from the RunTime queue. 

This php file is called in: 

- :ref:`pollRunTimeHydraRun` function from the **HydraRun.html** file. 


.. code-block:: php 

    #$sql="SELECT * from RunTime where DateTime > now() - interval 10 SECOND;";

    //DO CLEANUP

    //$cleansql="DELETE FROM RunTime where DateTime < now() - interval 1 hour";
    //$conn->query($cleansql);
    //$conn->commit();
    $sql="SELECT * from RunTime where ID in (SELECT MAX(ID) from RunTime GROUP by PlotType_ID) && DateTime > now() - interval 10 SECOND ORDER BY ID desc;";
    //$sql="SELECT * from RunTime where DateTime > now() - interval 10 SECOND;";
    #echo $sql . "<br>";
