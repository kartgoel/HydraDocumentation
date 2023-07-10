.. _loginphp:

login
====================

This php file

This This php file is called in:

- :ref:`loginFuncLabeler` function from the **labeler.html** file. 
- :ref:`loginFuncLibrary` function from the **Library.html** file.

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


    $sql="SELECT Name, IsChunked from Plot_Types where ID in (SELECT Plot_Type_ID from User_Permissions where UserName=\"". $_SERVER['PHP_AUTH_USER'] ."\");";


    $result = $conn->query($sql);
    $data = array();
    if ($result->num_rows > 0) {
    // output data of each row
        while($row = $result->fetch_assoc()) {
            $name=$row["Name"];
            if($row["IsChunked"]==1)
            {
                $name=$name . "_Chunks";
            }
            $data[]=$name;
        //echo "id: " . $row["id"]. " - Run: " . $row["run"]. "<br>";
        }
    } 
    $conn->close();

    echo json_encode($data);
    return json_encode($data);
    ?>

Parameter
~~~~~~~~~~~~~~

- ``Experiment``: A string representing which experiment to configure parameters for. 