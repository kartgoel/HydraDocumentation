.. _populateSelectors:

populate_selectors
=======================

This php file retrieves plots to insert into selectors. 

This php file is called in:

- :ref:`PopulateSelectorLabeler` function from the **labeler.html** file. 
- :ref:`PopulateSelectorLibrary` function from the **Library.html** file.


.. code-block:: php

    if($_GET["Selector"]=="Plot_Type")
    {
        $sql="SELECT Name,IsChunked,ID FROM Plot_Types where IgnorePlot=0";
    }
    else if($_GET["Selector"]=="Palette-Holder")
    {
        $plot_name=$_GET["SelectedPlot"];
        $plot_parse=explode("_Chunk",$plot_name);
        if (sizeof($plot_parse) == 1)
        {
            $sql="SELECT Classification from Plot_Classifications where ID in (SELECT Plot_Classifications_ID from Valid_Classifications where Plot_Types_ID in (SELECT ID FROM Plot_Types where IgnorePlot=0 and Name=\"" . $plot_name . "\"));";
        }
        else
        {
            $sql="SELECT Classification from Plot_Classifications where ID in (SELECT Plot_Classifications_ID from Valid_Classifications where Plot_Types_ID in (SELECT ID FROM Plot_Types where IgnorePlot=0 and IsChunked=1 && Name=\"" . $plot_parse[0] . "\"));";
        }
    }

Parameter
~~~~~~~~~~~~~~~~~~

- ``Selector``: A string to determine what SQL query is performed. 
