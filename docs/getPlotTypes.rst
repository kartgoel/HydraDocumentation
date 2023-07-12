.. _getPlotTypesphp: 

getPlotTypes
=====================

This php file retrieves plot types that have a IsChunked value of 1 and an IgnorePlot value of 0.

This php file is called in:

- :ref:`BuildRunHTMLHydraRun` function from the **HydraRun.html** file. 


.. code-block:: php 

    $sql="SELECT * from Plot_Types where IsChunked=1 and IgnorePlot=0 Order by Active_Model_ID desc;";
    #echo $sql . "<br>";

