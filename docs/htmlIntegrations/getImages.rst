

get_images
=============

This php file 

.. code-block:: php 

    $plot_name=$_GET["Plot"];
    $plot_parse=explode("_Chunks",$plot_name);
    //var_dump($plot_parse);
    if($_GET["Mode"]=="novel")
    {
        
        if (sizeof($plot_parse) == 1)
        {
            $sql="SELECT * FROM Plots as PL INNER JOIN Plot_Types as PT ON PT.IsChunked IS NULL && PT.Name=\"" . $plot_name . "\" && PL.ID not in (SELECT Plot_ID from Users_Plots) && PL.Plot_Types_ID in (SELECT ID FROM Plot_Types where Name=\"" . $plot_name . "\" && IsChunked is NULL) && RunNumber>=" . $_GET["RunNumMin"]." && RunNumber<=" . $_GET["RunNumMax"] ." ORDER BY RunNumber desc, Chunk desc LIMIT 100;";
            $remaining_q="SELECT COUNT(*) FROM Plots as PL INNER JOIN Plot_Types as PT ON PT.IsChunked IS NULL && PT.Name=\"" . $plot_name . "\" && PL.ID not in (SELECT Plot_ID from Users_Plots) && PL.Plot_Types_ID in (SELECT ID FROM Plot_Types where Name=\"" . $plot_name . "\" && IsChunked is NULL) && RunNumber>=" . $_GET["RunNumMin"]." && RunNumber<=" . $_GET["RunNumMax"];
        }
        else
        {
            $sql="SELECT * FROM Plots as PL INNER JOIN Plot_Types as PT ON PT.IsChunked=1 && PT.Name=\"" . $plot_parse[0] . "\" && PL.ID not in (SELECT Plot_ID from Users_Plots) && PL.Plot_Types_ID in (SELECT ID FROM Plot_Types where Name=\"" . $plot_parse[0] . "\") && RunNumber>=" . $_GET["RunNumMin"]." && RunNumber<=" . $_GET["RunNumMax"] ." ORDER BY RunNumber desc, Chunk desc LIMIT 100;";
            $remaining_q="SELECT COUNT(*) FROM Plots as PL INNER JOIN Plot_Types as PT ON PT.IsChunked=1 && PT.Name=\"" . $plot_parse[0] . "\" && PL.ID not in (SELECT Plot_ID from Users_Plots) && PL.Plot_Types_ID in (SELECT ID FROM Plot_Types where Name=\"" . $plot_parse[0] . "\") && RunNumber>=" . $_GET["RunNumMin"]." && RunNumber<=" . $_GET["RunNumMax"];
        }
        $remaining_result = $conn->query($remaining_q);
        $remaining_count= $remaining_result->fetch_assoc()["COUNT(*)"];
    }
    else
    {
        if (sizeof($plot_parse) == 1)
        {
            $sql="SELECT Plot_Types.Name, Plot_Types.FileType, Plots.RunPeriod, Plots.RunNumber,Plots.Chunk, Plot_Classifications.Classification, Plot_Types.IsChunked FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id && Plot_Types.IsChunked IS NULL left join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.name = \"" . $plot_name . "\" and ((Plots.id not in (select Users_Plots2.plot_id from Users_Plots Users_Plots2) or (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id))) && Plots.RunNumber>=" . $_GET["RunNumMin"]." && Plots.RunNumber<=" . $_GET["RunNumMax"] ." ORDER BY RunNumber desc,Chunk desc;";
            $remaining_q="SELECT COUNT(*) FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id && Plot_Types.IsChunked IS NULL left join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.name = \"" . $plot_name . "\" and ((Plots.id not in (select Users_Plots2.plot_id from Users_Plots Users_Plots2) or (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id))) && Plots.RunNumber>=" . $_GET["RunNumMin"]." && Plots.RunNumber<=" . $_GET["RunNumMax"];
        }
        else
        {
            $sql="SELECT Plot_Types.Name, Plot_Types.FileType, Plots.RunPeriod, Plots.RunNumber,Plots.Chunk, Plot_Classifications.Classification, Plot_Types.IsChunked FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id && Plot_Types.IsChunked=1 left join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.name = \"" . $plot_parse[0] . "\" and ((Plots.id not in (select Users_Plots2.plot_id from Users_Plots Users_Plots2) or (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id))) && Plots.RunNumber>=" . $_GET["RunNumMin"]." && Plots.RunNumber<=" . $_GET["RunNumMax"] ." ORDER BY RunNumber desc,Chunk desc;";
            $remaining_q="SELECT COUNT(*) FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id && Plot_Types.IsChunked=1 left join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.name = \"" . $plot_parse[0] . "\" and ((Plots.id not in (select Users_Plots2.plot_id from Users_Plots Users_Plots2) or (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id))) && Plots.RunNumber>=" . $_GET["RunNumMin"]." && Plots.RunNumber<=" . $_GET["RunNumMax"];
        }
        $remaining_result = $conn->query($remaining_q);
        $remaining_count= $remaining_result->fetch_assoc()["COUNT(*)"];
    }

    $filter_arr=[];

    if($_GET['Filters'])
    {
        $filter_arr=explode(",",$_GET['Filters']);
    }

    #echo $sql;
    #echo "<br>";
    $result = $conn->query($sql);

    $data = array();
    $data['count'] = $remaining_count;
    #echo $result->rowCount();
    #echo "<br>";
    #var_dump($result->fetch_assoc());

    if ($result->num_rows > 0) {
    // output data of each row
        while($row = $result->fetch_assoc()) {
            #echo $row;
            #echo "<br>";
            if(sizeof($filter_arr)>0 && !in_array($row['Classification'],$filter_arr) )
            {
                continue;
            }
            if($Exp=="GlueX")
            {
                $formatted_RunNumber=str_pad($row["RunNumber"],6,"0",STR_PAD_LEFT);
                $rootloc="/work/halld2/data_monitoring/";
                $imgpth=$row["RunPeriod"] . $formatted_RunNumber . "/";
                #echo $row["RunNumber"];

                #echo $row["Name"] . "<br>";
                if($row["Name"]=="BCAL_occupancy" && intval($row["RunNumber"])<=10986)
                {
                    $imgpth=$imgpth . "bcal_occupancy";
                }
                else if($row["Name"]=="RF_FDC_selftiming")
                {

                    $imgpth=$imgpth . $row["Name"];
                    $imgpth=$imgpth . "-01";
                
                }
                else if($row["Name"]=="RF_TOF_selftiming")
                {

                    $imgpth=$imgpth . $row["Name"];
                    $imgpth=$imgpth . "-02";
                
                }
                else if($row["Name"]=="RF_TAGH_selftiming")
                {

                    $imgpth=$imgpth . $row["Name"];
                    $imgpth=$imgpth . "-03";
                
                }
                else if($row["Name"]=="RF_PSC_selftiming")
                {

                    $imgpth=$imgpth . $row["Name"];
                    $imgpth=$imgpth . "-04";
                
                }
                else{
                $imgpth=$imgpth . $row["Name"];
                }
            
                if(intval($row["RunNumber"])==0)
                {
                    //console.log(returned_img_table[i]["RunPeriod"])
                    //cdc_1dead_board.png
                    $imgpth="/work/halld2/data_monitoring/simulated/". $row["RunPeriod"];
                }
            }
            else if ($Exp=="SBS")
            {
                $rootloc="";
            $imgpth=$rootloc . $row["RunPeriod"] . "/" . $row["RunNumber"] . "/";
            }
            if($row["Chunk"] != 0)
            {
                $imgpth=$imgpth . "_" . str_pad($row["Chunk"],4,"0",STR_PAD_LEFT);
            }
            $imgpth=$imgpth . "." . $row["FileType"];
            
            if($Exp=="GlueX")
            {
                if (file_exists($imgpth))
                {
                #echo "work2" . "<br>";
                    $row["rootLocation"]=$rootloc;
                }
                #echo $rootloc . "<br>";
                #echo "===========================================" . "<br>";
                $imgpth=str_replace($rootloc,"/work/halld/online_monitoring/AI/keeper/",$imgpth);
                #echo $imgpth . "<br>";
            
                #echo $imgpth . "<br>";
                #echo $imgpth . "  " . var_dump(file_exists($imgpth)) ."<br>";
                if(file_exists($imgpth))
                {
                    #echo "keeper <br>";
                    $row["rootLocation"]="/work/halld/online_monitoring/AI/keeper/";
                }
                $imgpth=str_replace("/work/halld/online_monitoring/AI/keeper/","/work/halld2/data_monitoring/simulated/",$imgpth);
                #echo "===========================================" . "<br>";
                #echo $imgpth . "<br>";
                #echo $imgpth . "  " . var_dump(file_exists($imgpth)) ."<br>";
                if(file_exists($imgpth)) 
                {
                    #echo "sim <br>";
                    $row["rootLocation"]="/work/halld2/data_monitoring/simulated/";
                }
            }
            #var_dump($row);
            #echo "<br>";
            #echo $row["rootLocation"];
            #echo "<br>";
            $data['imgs'][]=$row;
        //echo "id: " . $row["id"]. " - Run: " . $row["run"]. "<br>";
        }
    } 
