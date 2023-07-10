.. _getModelInfophp:

getModelInfo
==================

This php file

This php file is called in:

- :ref:`GetModelInfoLibrary` function from the **Library.html** file

.. code-block:: php

    <?php
    $Exp=$_GET['Experiment'];
    $PID=$_GET['mID'];

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


    $sql="SELECT * from Models where ID=$PID;";
    $training_set="SELECT COUNT(*) from Training_Sets where Models_ID=$PID";
    $inference_set="SELECT COUNT(*) from AI_Plots_Top_Classification_View where Model_ID=$PID";
    $thresholds="SELECT Classification,Threshold,ThresholdMethod from Plot_Classifications as PC inner join ModelThresholds as MT on MT.Plot_Classification_ID=PC.ID inner join Models on MT.Model_ID=Models.ID where Models.ID=$PID";


    //echo $name . " " . $chunk_val . "<br>";

    //$sql="SELECT * from RunTime where DateTime > now() - interval 10 SECOND;";
    //echo $sql . "<br>";

    $result = $conn->query($sql);
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

    if (count($data)!=0)
    {
    //echo $training_set . "<br>";
    $countq=$conn->query($training_set);
    $countr=$countq->fetch_assoc();
    //echo $countr["COUNT(*)"];
    //echo "<br>";
    $data["train"]=$countr["COUNT(*)"];

    //echo $inference_set . "<br>";

    $infq=$conn->query($inference_set);
    $infr=$infq->fetch_assoc();

    $data["inference"]=$infr["COUNT(*)"];

    //echo $thresholds;
    //echo "<br>";
    $threshq=$conn->query($thresholds);
    $thld=array();
    if ($threshq->num_rows > 0) {
        // output data of each row
            while($row = $threshq->fetch_assoc()) {
                $thld[]=$row;
            //echo "id: " . $row["id"]. " - Run: " . $row["run"]. "<br>";
            }
        }
    $data["thresholds"]=$thld;

    }


    $conn->close();

    echo json_encode($data);
    return json_encode($data);
    ?>

Parameters
~~~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to configure parameters for.
- ``model_ID``: 
