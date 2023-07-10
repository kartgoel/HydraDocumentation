.. _getModelsphp:

getModels
=========================

This php file retrieves the appropriate AI models from the database based on the given experiment and plot type. 
It parses the plot type to handle chuncked plots and constructs the SQL query accordingly to fetch the appropriate AI models. 
After querying the database and storing the retrieved models and their active model ID , the database connection is closed. 
It encodes the response array as a JSON and returns it to the caller.  

This php file is called in:

- :ref:`GetModelsLibrary` function from the **Library.html** file.

.. code-block:: php

    <?php
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


    //echo $_GET['qs'] . " ---> " . $_GET['qe'];
    // Create connection
    $conn = mysqli_connect($servername, $username, $password, $dbname);
    // Check connection
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

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

    $result = $conn->query($sql);
    $to_return=array();
    $data = array();
    #var_dump($result);

    if ($result->num_rows > 0) {
    // output data of each row
        while($row = $result->fetch_assoc()) {
            $data[]=$row;
        //echo "id: " . $row["id"]. " - Run: " . $row["run"]. "<br>";
        }
    } 

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


    $conn->close();

    echo json_encode($to_return);
    return json_encode($to_return);
    ?>

Parameters
~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to configure parameters for.
- ``plotType``: A string representing the plot type for which AI models are being retrieved. 