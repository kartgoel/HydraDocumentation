.. _getLeaderBoardphp:

getLeaderBoard
=========================

This php file retrieves the leaderboard depending on the plot.

This php file is called in:

- :ref:`getLeaderLabeler` function from the **labeler.html** file


.. code-block:: php 

    $plot_parse=explode("_Chunks",$_GET["Plot"]);
    #var_dump($plot_parse);
    if(sizeof($plot_parse)==1)
    {
        $sql="SELECT DISTINCT User,COUNT(*) as maxCount FROM Users_Plots where Plot_ID in (SELECT ID FROM Plots where Plot_Types_ID in (SELECT ID FROM Plot_Types where Name=\"" . $_GET["Plot"] . "\")) GROUP BY User ORDER BY maxCount desc LIMIT 1;";
    }
    else
    {
        $sql="SELECT DISTINCT User,COUNT(*) as maxCount FROM Users_Plots where Plot_ID in (SELECT ID FROM Plots where Plot_Types_ID in (SELECT ID FROM Plot_Types where Name=\"" . $plot_parse[0] . "\" && IsChunked=1)) GROUP BY User ORDER BY maxCount desc LIMIT 1;";
    }


Parameters
~~~~~~~~~~~~~~~~~~

- ``Plot``: A string representing which plot the SQL query is performed with. 
