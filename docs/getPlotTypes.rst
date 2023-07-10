.. _getPlotTypesphp: 

getPlotTypes
=====================

This php file 

This php file is called in:

- :ref:`BuildRunHTMLHydraRun` function from the **HydraRun.html** file. 


.. code-block:: php 

    <?php
    $Exp=$_GET['Experiment'];

    if($Exp=="GlueX")
    {
        $servername = "hallddb-ext";
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

    $sql="SELECT * from Plot_Types where IsChunked=1 and IgnorePlot=0 Order by Active_Model_ID desc;";
    #echo $sql . "<br>";

    $result = $conn->query($sql);
    $data = array();
    if ($result->num_rows > 0) {
    // output data of each row
        while($row = $result->fetch_assoc()) {
            $data[]=$row;
        //echo "id: " . $row["id"]. " - Run: " . $row["run"]. "<br>";
        }
    } 
    $conn->close();

    echo json_encode($data);
    return json_encode($data);
    ?>

Parameter
~~~~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to configure parameters for.