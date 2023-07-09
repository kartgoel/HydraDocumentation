getLeaderBoard
=========================

This php file retrieves data from the Hydra database based on the specified experiment, plot, and selector. 
It connects to the database, executes the SQL query, and returns the results in JSON format. 

This php file is called in the :ref:'labeler:GetLeader' function from the **labeler.html** file. 

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
~~~~~~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to configure parameters for. 
- ``Plot``: A string representing which plot the SQL query is performed with. 
