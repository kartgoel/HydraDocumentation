.. _record_labelsphp:

record_labels
=============

This php file retrieves the user's labels and inserts them into the user's plot history. 

This php file is called in:

- :ref:`RecordLabelsLabeler` function from the **labeler.html** file

.. code-block:: php

    $DATA = json_decode($_GET["Labels"],true);

    $plot_name=$DATA["plotType"];
    //echo $plot_name;
    //echo "<br>";
    $plot_parse=explode("_Chunk",$plot_name);

    //var_dump($plot_parse);
    $get_type_num_q="SELECT ID FROM Plot_Types where Name=\"" . $plot_parse[0] ."\";";

    if (sizeof($plot_parse) == 2)
    {
        $get_type_num_q="SELECT ID FROM Plot_Types where IsChunked=1 && Name=\"" . $plot_parse[0] ."\";";
    }
    //echo $get_type_num_q;

    $result = $conn->query($get_type_num_q);
    //echo $result;
    //echo "<br>";
    $PlotType_ID = $result->fetch_assoc()["ID"];
    //echo $PlotType_ID;

    $permissions_q="SELECT ID FROM User_Permissions where UserName=\"" . $_SERVER['PHP_AUTH_USER']  . "\" && Plot_Type_ID=" . $PlotType_ID;
    $result = $conn->query($permissions_q);
    $Plot_Permissions_ID = $result->fetch_assoc();

    if ( count($Plot_Permissions_ID)==0)
    {
    echo "fail";
    return "fail";
    }
    $rollback=False;
    mysqli_query($conn,"START TRANSACTION"); // transaction begins

    try {
        $query_h = 'INSERT INTO Users_Plots_History (Date,User,TransactionJSON) values (NOW(),"' . $_SERVER['PHP_AUTH_USER'] .'",\'' . $_GET["Labels"] .'\');';
        //echo $query_h;
        //echo "<br>";
        $query1 = mysqli_query($conn,$query_h);

        foreach ($DATA["labels"] as $lbl)
        {
            //var_dump($lbl);
            //var_dump($lbl);//ID, Classification_Type_ID, Classification
            $get_classNum_ID_q="SELECT ID,Classification_Type_ID FROM Plot_Classifications WHERE Classification=\"" . $lbl["Label"] . "\";";
            //echo $get_classNum_ID_q;
            //echo "<br>";
            $result = $conn->query($get_classNum_ID_q);
            $Classification_info = $result->fetch_assoc();
            $Classification_ID=$Classification_info["ID"];
            $Classification_Type_ID=$Classification_info["Classification_Type_ID"];
            //echo $Classification_ID;

            $get_Plot_ID_q="SELECT ID FROM Plots WHERE Plot_Types_ID=" . $PlotType_ID . " && RunNumber=" . $lbl["RunNum"] . "&& Chunk=" . $lbl["ChunkNum"];

            if(!is_numeric($lbl["RunNum"]))
            {
                $get_Plot_ID_q="SELECT ID FROM Plots WHERE Plot_Types_ID=" . $PlotType_ID . " && Chunk=0 && RunNumber=0 && RunPeriod=\"" . $lbl["RunNum"] . "\"";
            }

            echo $get_Plot_ID_q;
            $result = $conn->query($get_Plot_ID_q);
            $Plot_ID = $result->fetch_assoc()["ID"];

            //ID, User, Plot_ID, Classification_Type_ID, Plot_Classification_ID, Comment
            //DELETE
            $del_q = "DELETE FROM Users_Plots where Plot_ID=". $Plot_ID .";";
            $query2 = mysqli_query($conn,$del_q);
            //ADD
            $add_q = "INSERT INTO Users_Plots (User, Plot_ID, Classification_Type_ID, Plot_Classification_ID) VALUES (\"". $_SERVER['PHP_AUTH_USER'] ."\",". $Plot_ID . ",". $Classification_Type_ID .",". $Classification_ID.");";
            $query3 = mysqli_query($conn,$add_q);

            echo $query1 . " | ".$query2." | ".$query3;
            //echo "<br>";

            if(!$query1 or !$query2 or !$query3)
            {
                echo "ROLLING BACK";
                $rollback=True;
                mysqli_query("ROLLBACK"); 
                break;
            }
        }
        if(!$rollback)
        {   
            mysqli_query($conn,"COMMIT");
        }
    } catch (Exception $e)
    {
        echo "ROLLING BACK ON EXCEPTION";
        mysqli_query($conn,"ROLLBACK"); //mysql_query("ROLLBACK"); // transaction rolls back
    }

        
        