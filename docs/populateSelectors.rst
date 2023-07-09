populate_selectors
=======================

This php file retrieves data from the Hydra database based on the specified experiment and selector. 
It connects to the database, executes the SQL query, and returns the result in JSON format. 

This php file is called in the :ref:'labeler:PopulateSelector' function from the **labeler.html** file. 

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
    //echo $_GET['qs'] . " ---> " . $_GET['qe'];
    // Create connection
    $conn = mysqli_connect($servername, $username, $password, $dbname);
    // Check connection
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }


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
~~~~~~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to pull data for. 