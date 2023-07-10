.. _pollRunTimephp:

pollRunTime
======================

This php file retrieves the appropriate AI models from the database based on the given experiment and plot type. 
It parses the plot type to handle chuncked plots and constructs the SQL query accordingly to fetch the appropriate AI models. 
It encodes the response array as a JSON and returns it to the caller. 

This php file is called in: 

- :ref:`pollRunTimeHydraRun` function from the **HydraRun.html** file. 


.. code-block:: php 

    <?php
    $Exp=$_GET['Experiment'];

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
    $sql="SELECT * from RunTime where ID in (SELECT MAX(ID) from RunTime GROUP by PlotType_ID) && DateTime > now() - interval 10 SECOND ORDER BY ID desc;";
    //$sql="SELECT * from RunTime where DateTime > now() - interval 10 SECOND;";
    #echo $sql . "<br>";

    $result = $conn->query($sql);
    $data = array();
    #var_dump($result);

    if ($result->num_rows > 0) {
    // output data of each row
        while($row = $result->fetch_assoc()) {
            $data[]=$row;
        }
    } 
    $conn->close();

    echo json_encode($data);
    return json_encode($data);
    ?>

Parameter
~~~~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to configure parameters for.