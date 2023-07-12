.. _getModelsphp:

getModels
=========================

This php file retreives active model IDs for models based upon their chunked status. 

This php file is called in:

- :ref:`GetModelsLibrary` function from the **Library.html** file.

.. code-block:: php


    #$sql="SELECT * from RunTime where DateTime > now() - interval 10 SECOND;";

    //DO CLEANUP

    //$cleansql="DELETE FROM RunTime where DateTime < now() - interval 1 hour";
    //$conn->query($cleansql);
    //$conn->commit();
    $parts = explode("_", $PT);
    $chunked = array_pop($parts);
    $chunk_val=0;
    $name = implode("_", $parts);
    if($chunked=="Chunks")
    {
        $chunk_val=1;
        $sql="SELECT Models.ID,Models.Name from Models inner join Plot_Types as PT where (Models.PlotType_ID=PT.ID and PT.Name='$name' and PT.IsChunked=$chunk_val) or (Models.ID=PT.Active_Model_ID and PT.Name='$name' and PT.IsChunked=$chunk_val)";
        $active_model_ID="SELECT Active_Model_ID from Plot_Types where Name='$name' and IsChunked=$chunk_val";
    }
    else
    {
        $chunk_val=0;
        $name=$PT;
        $sql="SELECT Models.ID,Models.Name from Models inner join Plot_Types as PT where (Models.PlotType_ID=PT.ID and PT.Name='$name' and (PT.IsChunked=$chunk_val or PT.IsChunked is NULL)) or (Models.ID=PT.Active_Model_ID and PT.Name='$name' and (PT.IsChunked=$chunk_val or PT.IsChunked is NULL))";
        $active_model_ID="SELECT Active_Model_ID from Plot_Types where Name='$name' and (IsChunked=$chunk_val or IsChunked is NULL)";
    }


    //echo $name . " " . $chunk_val . "<br>";

    //$sql="SELECT * from RunTime where DateTime > now() - interval 10 SECOND;";
    //echo $sql . "<br>";

    //var_dump($data);
    //echo "<br>";
    //echo count($data);
    //echo "<br>";
    $to_return["models"]=$data;

    if (count($data)!=0)
    {

        $active_model_ID=$conn->query($active_model_ID);
        $active_model_ID=$active_model_ID->fetch_assoc();
        $to_return["activeID"]=$active_model_ID["Active_Model_ID"];
        
    }


Parameter
~~~~~~~~~~~~~

- ``plotType``: A string representing the plot type for which AI models are being retrieved. 