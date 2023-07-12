.. _getLogphp: 

getLog 
============

This php file retrieves the MonitoringLog for the past 700 hours. 

.. code-block:: php 

    $sql="SELECT * from MonitoringLog where DateTime > now() - interval 700 HOUR;";